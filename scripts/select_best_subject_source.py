#!/usr/bin/env python3
"""Build a split-safe subject-level blend from prediction CSVs.

Each source is scored by per-subject mean CER on the given split. For every
subject in the anchor source, the script selects the available source with the
lowest CER, writes those rows to a blended prediction CSV, and writes a compact
JSON summary with provenance.

For held-out audits, pass --fixed-summary from a validation run. In that mode the
script applies the frozen Subject -> source mapping and never selects by test
metrics.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path


def parse_source(raw: str) -> tuple[str, Path]:
    if "=" not in raw:
        raise ValueError(f"source must be label=path, got {raw!r}")
    label, path = raw.split("=", 1)
    label = label.strip()
    if not label:
        raise ValueError("source label cannot be empty")
    return label, Path(path)


def load_fixed_mapping(path: Path) -> dict[str, str]:
    summary = json.loads(path.read_text())
    per_subject = summary.get("per_subject")
    if not isinstance(per_subject, list):
        raise ValueError(f"{path} missing per_subject list")
    mapping: dict[str, str] = {}
    for item in per_subject:
        if not isinstance(item, dict):
            raise ValueError(f"{path} has non-object per_subject item: {item!r}")
        subject = str(item.get("Subject", "")).strip()
        source = str(item.get("source", "")).strip()
        if not subject or not source:
            raise ValueError(f"{path} has incomplete fixed mapping item: {item!r}")
        mapping[subject] = source
    if not mapping:
        raise ValueError(f"{path} produced empty fixed mapping")
    return mapping


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError(f"{path} has no rows")
    required = {"Subject", "Sentence_UID", "CER", "WER"}
    missing = required - set(rows[0])
    if missing:
        raise ValueError(f"{path} missing columns: {sorted(missing)}")
    return rows


def group_by_subject(rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row["Subject"]].append(row)
    return dict(grouped)


def mean_metric(rows: list[dict[str, str]], key: str) -> float:
    return sum(float(row[key]) for row in rows) / len(rows)


def source_is_compatible(
    candidate_rows: list[dict[str, str]],
    anchor_rows: list[dict[str, str]],
) -> bool:
    return sorted(row["Sentence_UID"] for row in candidate_rows) == sorted(
        row["Sentence_UID"] for row in anchor_rows
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source",
        action="append",
        required=True,
        help="label=prediction_csv; first source is the subject anchor",
    )
    parser.add_argument("--output", required=True, help="blended prediction CSV")
    parser.add_argument("--summary", required=True, help="JSON summary path")
    parser.add_argument(
        "--fixed-summary",
        help="validation summary JSON whose per_subject source mapping is applied",
    )
    parser.add_argument("--split", default="val")
    args = parser.parse_args()

    source_items = [parse_source(raw) for raw in args.source]
    source_labels = {label for label, _path in source_items}
    fixed_mapping = load_fixed_mapping(Path(args.fixed_summary)) if args.fixed_summary else None
    if fixed_mapping:
        unknown = sorted(set(fixed_mapping.values()) - source_labels)
        if unknown:
            raise ValueError(
                "fixed summary references missing source labels: " + ", ".join(unknown)
            )
    loaded = {label: load_rows(path) for label, path in source_items}
    by_subject = {label: group_by_subject(rows) for label, rows in loaded.items()}
    anchor_label = source_items[0][0]
    anchor_subjects = by_subject[anchor_label]

    output_rows: list[dict[str, str]] = []
    per_subject: list[dict[str, object]] = []
    selected_sources: Counter[str] = Counter()
    all_fieldnames: list[str] = []

    def remember_fields(row: dict[str, str]) -> None:
        for key in row:
            if key not in all_fieldnames:
                all_fieldnames.append(key)

    for subject in sorted(anchor_subjects, key=lambda value: (len(value), value)):
        anchor_rows = anchor_subjects[subject]
        candidates: list[tuple[float, str, list[dict[str, str]]]] = []
        for label, _path in source_items:
            rows = by_subject[label].get(subject)
            if not rows:
                continue
            if not source_is_compatible(rows, anchor_rows):
                continue
            candidates.append((mean_metric(rows, "CER"), label, rows))
        if not candidates:
            raise ValueError(f"no compatible rows found for subject {subject}")

        if fixed_mapping is None:
            cer, label, rows = min(candidates, key=lambda item: (item[0], item[1]))
        else:
            if subject not in fixed_mapping:
                raise ValueError(f"fixed summary missing subject {subject}")
            label = fixed_mapping[subject]
            matching = [item for item in candidates if item[1] == label]
            if not matching:
                raise ValueError(
                    f"fixed source {label!r} unavailable or incompatible for subject {subject}"
                )
            cer, label, rows = matching[0]
        selected_sources[label] += 1
        selected = sorted(rows, key=lambda row: row["Sentence_UID"])
        for row in selected:
            copied = dict(row)
            copied["Blend Source"] = label
            remember_fields(copied)
            output_rows.append(copied)
        per_subject.append(
            {
                "Subject": subject,
                "source": label,
                "CER": cer,
                "WER": mean_metric(rows, "WER"),
                "n_rows": len(rows),
                "candidates": {
                    cand_label: {
                        "CER": cand_cer,
                        "WER": mean_metric(cand_rows, "WER"),
                    }
                    for cand_cer, cand_label, cand_rows in sorted(candidates)
                },
            }
        )

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if "Blend Source" not in all_fieldnames:
        all_fieldnames.append("Blend Source")
    with output_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=all_fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(output_rows)

    subject_mean_cer = sum(float(row["CER"]) for row in per_subject) / len(per_subject)
    subject_mean_wer = sum(float(row["WER"]) for row in per_subject) / len(per_subject)
    row_mean_cer = mean_metric(output_rows, "CER")
    row_mean_wer = mean_metric(output_rows, "WER")
    summary = {
        "split": args.split,
        "test_touched": args.split == "test",
        "selection_source": (
            "fixed_validation_summary"
            if fixed_mapping is not None
            else "validation_per_subject_min_cer"
        ),
        "fixed_summary": args.fixed_summary,
        "rows": len(output_rows),
        "subjects": len(per_subject),
        "subject_mean_CER": subject_mean_cer,
        "subject_mean_WER": subject_mean_wer,
        "row_mean_CER": row_mean_cer,
        "row_mean_WER": row_mean_wer,
        "selected_sources": dict(selected_sources),
        "per_subject": per_subject,
    }
    summary_path = Path(args.summary)
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
