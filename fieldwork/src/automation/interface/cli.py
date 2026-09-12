"""Interactive, local command-line interface."""
from __future__ import annotations
import argparse
from pathlib import Path
from automation.bootstrap import build

def main() -> None:
    parser = argparse.ArgumentParser(description="Safe local document automation")
    parser.add_argument("instruction"); parser.add_argument("files", nargs="+")
    args = parser.parse_args(); workflow = build(Path.cwd())
    plan, preview = workflow.propose(args.instruction, args.files)
    print(f"\nPreview: {preview.summary}\n{preview.data['sample']}\n")
    approved = input("Create this new output file? [y/N] ").strip().lower() in {"y", "yes"}
    result = workflow.execute(plan.plan_id, approved)
    print(result.summary)
    for artifact in result.output_artifacts: print(f"Output: data/outputs/*_{artifact.display_name}")

if __name__ == "__main__": main()
