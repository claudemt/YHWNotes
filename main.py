#!/usr/bin/env python3
"""Unified build driver for the multi-book physics notes repository.

Examples
--------
python main.py list
python main.py build FreeElectronQuantumOptics
python main.py build AdvancedPhysics --figures
python main.py build --all
"""
from __future__ import annotations
from pathlib import Path
import argparse
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content"
BUILD = ROOT / "build"
EXAMPLE = ROOT / "example"

def book_entry(book: str) -> Path:
    return CONTENT / book / f"{book}.tex"

def books() -> list[str]:
    return sorted(
        p.name for p in CONTENT.iterdir()
        if p.is_dir() and book_entry(p.name).exists()
    )

def run(cmd, cwd=ROOT):
    print("+", " ".join(map(str, cmd)))
    subprocess.run(cmd, cwd=cwd, check=True)

def generate_figures(book: str):
    book_dir = CONTENT / book
    scripts = sorted(
        p for p in book_dir.rglob("*_code.py")
        if not p.name.startswith("_") and "generated" not in p.parts
    )
    for script in scripts:
        print(f"[figure] {book}: {script.relative_to(book_dir)}")
        run([sys.executable, str(script)])

def build_one(book: str, figures: bool = False):
    if book not in books():
        raise SystemExit(f"Unknown book: {book}")

    if figures:
        generate_figures(book)

    work = BUILD / book
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True, exist_ok=True)
    EXAMPLE.mkdir(parents=True, exist_ok=True)

    entry = f"content/{book}/{book}.tex"
    tex_entry = rf"\def\BookContentFile{{{entry}}}\input{{main.tex}}"
    xelatex = [
        "xelatex", "-no-pdf", "-interaction=nonstopmode", "-halt-on-error",
        "-jobname=main", f"-output-directory={work}", tex_entry,
    ]

    run(xelatex)
    if (work / "main.bcf").exists():
        run([
            "biber",
            f"--input-directory={work}",
            f"--output-directory={work}",
            "main",
        ])
    run(xelatex)
    run(xelatex)

    xdv = work / "main.xdv"
    pdf = work / "main.pdf"
    run(["xdvipdfmx", "-E", "-o", str(pdf), str(xdv)])
    target = EXAMPLE / f"{book}.pdf"
    shutil.copy2(pdf, target)
    print(f"Built: {target}")

def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list")

    p = sub.add_parser("build")
    p.add_argument("book", nargs="?")
    p.add_argument("--all", action="store_true")
    p.add_argument("--figures", action="store_true")

    args = parser.parse_args()
    if args.command == "list":
        print("\n".join(books()))
        return

    if args.all:
        for book in books():
            build_one(book, figures=args.figures)
    elif args.book:
        build_one(args.book, figures=args.figures)
    else:
        parser.error("build requires <book> or --all")

if __name__ == "__main__":
    main()
