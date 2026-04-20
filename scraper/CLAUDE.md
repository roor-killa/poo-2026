# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Educational repository for an L2 Computer Science OOP course (Université Antilles). Course materials are in French. The current active branch is `groupe_scp5` for student group work.

## Running Code

No build system — run Python scripts directly:

```bash
python script.py
```

For TP_Scraping dependencies (not yet installed):
```bash
pip install requests beautifulsoup4 lxml pandas python-dotenv
# Optional: pip install selenium pytest
```

## Repository Structure

```
CM_POO/         # Course lecture notes (CM1–CM9, Markdown)
CM_POO_EXO/     # Python code examples illustrating each lecture concept
TD_POO/         # Guided labs (TD1–TD4): incremental OOP exercises
TP_POO/         # Graded projects
groupe_scp5/    # Student group project directory (current branch work)
```

## Course Curriculum Progression

- **CM1**: Classes and objects
- **CM2**: Inheritance, composition, MRO (diamond problem)
- **CM3**: Polymorphism, abstraction, duck typing
- **CM4**: Design patterns (Creational, Behavioral)
- **CM5**: SOLID principles
- **CM6**: Software architecture
- **CM7**: Testing and quality
- **CM8**: DevOps / CI/CD
- **CM9**: Security

## Active Projects

**TP_POO/TP_Scraping.md** (due 2026-03-04): Web scraper targeting Caribbean websites using abstract base class + concrete scrapers. Expected patterns: Factory, Strategy, Observer. Graded on architecture, code quality, functionality, error handling, documentation (/20).

**TP_POO/Enonce_TP.md**: Cryptocurrency wallet transfer system (BKN) using sockets, JSON serialization, and threading. Two parts: local transfers (Part 1) and network transfers (Part 2).

## Coding Conventions

- Python 3.10+ with type hints required
- PEP 8 style
- AI usage is authorized in TDs/TPs but all code must be fully explainable

## Branch Strategy

`main` is the primary branch. Each student/group has their own branch (e.g., `groupe_scp1`–`groupe_scp5`, individual name branches). Work is submitted via pull requests to `main`.
