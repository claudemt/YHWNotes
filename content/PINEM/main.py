"""Build and validate the textbook project from its root directory.

Usage:
    python main.py build
    python main.py check
    python main.py figure comb_measurement
"""
import argparse
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent


def run(argv):
    subprocess.run(argv, check=True, cwd=ROOT)


def main():
    parser = argparse.ArgumentParser(description="PINEM textbook build and numerical QA")
    parser.add_argument("command", choices=("build", "check", "figure"))
    parser.add_argument("name", nargs="?", help="figure script stem for the figure command")
    args = parser.parse_args()
    if args.command == "build":
        run(["latexmk", "-xelatex", "-interaction=nonstopmode", "-halt-on-error", "main.tex"])
    elif args.command == "check":
        run([sys.executable, "check_reproducibility.py"])
    else:
        if not args.name or not args.name.replace("_", "").replace("-", "").isalnum():
            parser.error("supply a valid figure stem")
        script = ROOT / "figures" / (args.name + ".py")
        if not script.is_file():
            parser.error(f"unknown figure: {args.name}")
        run([sys.executable, str(script)])


if __name__ == "__main__":
    main()
