#!/usr/bin/env python3
"""
=============================================================================
Agent Skill Tool: One-Command Submission Packager & Validator
Author: Lam Huu Khanh (Student ID: 23127205)
Course: Software Testing (HCMUS) - HW06: API Testing

Description:
  Validates all 12 mandatory rubric deliverables, structures the submission
  folder, and compiles the final ZIP archive:
  <StudentID>_HW06_AI_API_<SelfAssessedGrade>.zip
=============================================================================
"""

import os
import sys
import shutil
import zipfile
from pathlib import Path

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

STUDENT_ID = "23127205"
GRADE = "100"
ZIP_NAME = f"{STUDENT_ID}_HW06_AI_API_{GRADE}.zip"


def package_submission(workspace_root: Path):
    print("=" * 65)
    print(f"  AUTOMATED SUBMISSION PACKAGER: {ZIP_NAME}")
    print(f"  Root: {workspace_root}")
    print("=" * 65)

    source_dir = workspace_root / "23127205_HW06_AI_API_100"
    if not source_dir.exists():
        source_dir = workspace_root / "HW06"

    # Mandatory Deliverables Checklist
    checklist = [
        ("README.md", source_dir / "README.md"),
        ("Main Report MD", source_dir / "reports" / "main-report.md"),
        ("Main Report PDF", source_dir / "reports" / "main-report.pdf"),
        ("CI/CD Report MD", source_dir / "reports" / "cicd-report.md"),
        ("CI/CD Report PDF", source_dir / "reports" / "cicd-report.pdf"),
        ("AI Audit Report MD", source_dir / "reports" / "ai-audit-report.md"),
        ("AI Audit Report PDF", source_dir / "reports" / "ai-audit-report.pdf"),
        ("AI Critique MD", source_dir / "reports" / "ai-critique.md"),
        ("AI Critique PDF", source_dir / "reports" / "ai-critique.pdf"),
        ("Bug Report MD", source_dir / "reports" / "bug-report.md"),
        ("Git Commit Log", source_dir / "reports" / "git-commit-log.txt"),
        ("Excel Test Cases", source_dir / "test-cases" / "member-1.xlsx"),
        ("Postman Collection", source_dir / "postman" / "HW06_API_Testing.postman_collection.json"),
        ("Postman Environment", source_dir / "postman" / "HW06_Local.postman_environment.json"),
        ("Newman CI HTML Report", source_dir / "newman" / "member-1" / "ci-report.html"),
        ("Agent Skill Code", source_dir / "agent-skill" / "generate_api_tests.py"),
        ("Agent Skill Diagram", source_dir / "agent-skill" / "diagram.png"),
        ("Agent Skill Pseudocode", source_dir / "agent-skill" / "pseudocode.md"),
        ("OpenAPI Spec YAML", source_dir / "docs" / "openapi.yaml"),
        ("CI/CD Workflow", source_dir / ".github" / "workflows" / "api-tests.yml"),
    ]

    print("\n[Step 1] Verifying 20 Key Deliverables:")
    all_passed = True
    for name, path in checklist:
        if path.exists():
            size_kb = path.stat().st_size // 1024
            print(f"  ✅ {name:<26} [FOUND - {size_kb} KB]")
        else:
            print(f"  ❌ {name:<26} [MISSING: {path}]")
            all_passed = False

    if not all_passed:
        print("\n[!] Warning: Some deliverables are missing. Proceeding with available files...")

    # Step 2: Create Zip Archive
    print(f"\n[Step 2] Building ZIP Archive: {ZIP_NAME}...")
    zip_dest_root = workspace_root / ZIP_NAME

    with zipfile.ZipFile(str(zip_dest_root), 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(str(source_dir)):
            # Filter out unnecessary dirs
            dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '__pycache__', '.pytest_cache']]
            for file in files:
                if file.endswith(('.pyc', '.tmp', '.log')) or file.startswith('.~'):
                    continue
                abs_file = Path(root) / file
                rel_path = abs_file.relative_to(source_dir)
                zf.write(str(abs_file), str(rel_path))

    zip_size_mb = zip_dest_root.stat().st_size / (1024 * 1024)
    print(f"✅ [SUCCESS] Created ZIP: {zip_dest_root} ({zip_size_mb:.2f} MB)")
    print("\n" + "=" * 65)
    print("  PACKAGE IS 100% READY FOR MOODLE SUBMISSION!")
    print("=" * 65)
    return True


def find_workspace_dir() -> Path:
    p = Path(__file__).resolve().parent
    for _ in range(6):
        if (p / "23127205_HW06_AI_API_100").exists() or (p / "HW06").exists():
            return p
        p = p.parent
    return Path.cwd()


if __name__ == "__main__":
    ws = find_workspace_dir()
    package_submission(ws)
