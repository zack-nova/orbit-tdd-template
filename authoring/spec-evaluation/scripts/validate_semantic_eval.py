#!/usr/bin/env python3

import argparse
import json
from pathlib import Path


VERIFICATION_LABELS = {
    "strong_probe": "强 + probe",
    "strong": "强",
    "medium": "中",
    "weak": "弱",
}

WRITE_SURFACE_KEYS = [
    "entry_brief",
    "rules_workflow",
    "implementation_code",
    "tests_checks",
    "evidence_records",
    "specs_plans",
    "qa_release_review",
]

RECOVERY_LABELS = {
    "complete": "完整",
    "recoverable": "可恢复",
    "basic": "基础",
    "fragile": "脆弱",
}


def parse_args():
    parser = argparse.ArgumentParser(
        description="Validate an agent-produced semantic README metrics JSON file."
    )
    parser.add_argument(
        "--eval-file",
        required=True,
        help="Path to the semantic evaluation JSON file.",
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Root directory used to resolve repo-relative evidence paths.",
    )
    return parser.parse_args()


def read_json(path):
    return json.loads(Path(path).read_text())


def assert_true(condition, message):
    if not condition:
        raise SystemExit(message)


def write_boundary_display(writable_count, total_count):
    ratio = 0.0 if total_count == 0 else writable_count / total_count
    if ratio <= 0.30:
        return f"窄 ({writable_count}/{total_count})"
    if ratio <= 0.60:
        return f"中 ({writable_count}/{total_count})"
    return f"宽 ({writable_count}/{total_count})"


def validate_evidence_items(root, evidence, context):
    assert_true(isinstance(evidence, list) and evidence, f"{context}: evidence must be a non-empty list")
    for index, item in enumerate(evidence):
        assert_true("file" in item, f"{context}: evidence[{index}] missing file")
        assert_true("must_contain" in item, f"{context}: evidence[{index}] missing must_contain")
        path = root / item["file"]
        assert_true(path.exists(), f"{context}: evidence file not found: {item['file']}")
        content = path.read_text()
        assert_true(
            item["must_contain"] in content,
            f"{context}: evidence snippet not found in {item['file']}: {item['must_contain']!r}",
        )


def main():
    args = parse_args()
    root = Path(args.root).resolve()
    data = read_json(args.eval_file)

    assert_true("spec_display" in data and data["spec_display"], "spec_display is required")
    assert_true("use_case_display" in data and data["use_case_display"], "use_case_display is required")
    validate_evidence_items(root, data.get("use_case_evidence", []), "use_case_evidence")

    startup = data["startup"]
    phases = startup["phases"]
    assert_true(isinstance(phases, list) and phases, "startup.phases must be a non-empty list")
    unique_files = set()
    for index, phase in enumerate(phases):
        files = phase.get("files", [])
        assert_true(files, f"startup phase {index + 1} must list files")
        for relpath in files:
            path = root / relpath
            assert_true(path.exists(), f"startup phase {index + 1}: file not found: {relpath}")
            unique_files.add(relpath)
        validate_evidence_items(root, phase.get("evidence", []), f"startup phase {index + 1}")
    startup_depth = len(phases)
    startup_required_file_count = len(unique_files)

    verification = data["verification"]
    verification_label = verification["label"]
    assert_true(
        verification_label in VERIFICATION_LABELS,
        f"verification.label must be one of {sorted(VERIFICATION_LABELS)}",
    )
    actions = verification["actions"]
    assert_true(isinstance(actions, list) and actions, "verification.actions must be a non-empty list")
    for index, action in enumerate(actions):
        assert_true(action.get("id"), f"verification action {index + 1} missing id")
        assert_true(action.get("kind"), f"verification action {index + 1} missing kind")
        validate_evidence_items(root, action.get("evidence", []), f"verification action {action['id']}")
    action_count = len(actions)
    has_probe = bool(verification.get("has_probe"))
    cheap_probe = verification.get("cheap_probe")
    if has_probe:
        assert_true(isinstance(cheap_probe, dict), "verification.cheap_probe is required when has_probe=true")
        probe_path = cheap_probe.get("path")
        assert_true(probe_path, "verification.cheap_probe.path is required when has_probe=true")
        assert_true((root / probe_path).exists(), f"verification cheap probe path not found: {probe_path}")
        validate_evidence_items(root, cheap_probe.get("evidence", []), "verification cheap_probe")

    write_boundary = data["write_boundary"]
    surfaces = write_boundary["surfaces"]
    assert_true(
        isinstance(surfaces, list) and len(surfaces) == len(WRITE_SURFACE_KEYS),
        f"write_boundary.surfaces must contain exactly {len(WRITE_SURFACE_KEYS)} items",
    )
    seen_keys = set()
    writable_surface_count = 0
    for surface in surfaces:
        key = surface.get("key")
        assert_true(key in WRITE_SURFACE_KEYS, f"write_boundary surface key is invalid: {key!r}")
        assert_true(key not in seen_keys, f"write_boundary surface key is duplicated: {key}")
        seen_keys.add(key)
        assert_true(
            isinstance(surface.get("writable"), bool),
            f"write_boundary surface {key}: writable must be boolean",
        )
        if surface["writable"]:
            writable_surface_count += 1
        validate_evidence_items(root, surface.get("evidence", []), f"write_boundary surface {key}")

    recovery = data["recovery"]
    recovery_label = recovery["label"]
    assert_true(
        recovery_label in RECOVERY_LABELS,
        f"recovery.label must be one of {sorted(RECOVERY_LABELS)}",
    )
    non_success_states = recovery["non_success_states"]
    assert_true(
        isinstance(non_success_states, list) and non_success_states,
        "recovery.non_success_states must be a non-empty list",
    )
    validate_evidence_items(root, recovery.get("evidence", []), "recovery")

    result = {
        "valid": True,
        "spec_display": data["spec_display"],
        "use_case_display": data["use_case_display"],
        "startup": {
            "depth": startup_depth,
            "required_file_count": startup_required_file_count,
            "display": f"D{startup_depth}/R{startup_required_file_count}",
        },
        "verification": {
            "label": verification_label,
            "display": VERIFICATION_LABELS[verification_label],
            "action_count": action_count,
            "has_probe": has_probe,
        },
        "write_boundary": {
            "writable_surface_count": writable_surface_count,
            "surface_count": len(WRITE_SURFACE_KEYS),
            "display": write_boundary_display(writable_surface_count, len(WRITE_SURFACE_KEYS)),
        },
        "recovery": {
            "label": recovery_label,
            "display": f"{RECOVERY_LABELS[recovery_label]} ({len(non_success_states)}态)",
            "non_success_state_count": len(non_success_states),
        },
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
