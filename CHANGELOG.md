# Changelog

All notable changes to this project will be documented in this file.

## [v1.0.0] - 2025-07-07

### Added
- Initial project setup for automated C++ unit test generation.
- Integrated a self-hosted or API-based LLM for generating unit tests from `main.cpp`.
- YAML-driven instruction pipeline:
  - `generate.yaml` for first-time test creation.
  - `refine.yaml` for improving generated tests.
  - `fix_build.yaml` for resolving build errors automatically.
- Implemented `run.py` driver script:
  - Generates, refines, builds, and fixes tests.
  - Automatically invokes Google Test.
  - Calculates test coverage via `gcov`.
- Structured folders: `src/`, `tests/`, `build_logs/`, `instructions/`.
- Build output artifacts: `test_exec`, `.gcda`, `.gcno`, `.o` files.
- Logging of all build failures for debugging.

### Fixed
- Errors due to LLM-injected Markdown/code comments in test files.
- Issues with `INT_MAX`, `INT_MIN` overflow edge cases.
- GTest macro misuse (`TEST` vs `TEST_F`).

### Known Issues
- Some edge case tests (e.g., overflow handling) still fail due to undefined behavior in C++.
- LLM might occasionally generate invalid C++ comments or annotations.
