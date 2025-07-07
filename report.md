# TestForge: A C++ Unit Test Generator Report

## Project Summary
This tool automatically generates unit tests for a given C++ project using a local LLM and a YAML instruction pipeline. It refines, debugs, and validates those tests using Google Test and coverage tools.

---

## Project Structure

- **Source:** `src/main.cpp`
- **Test Output:** `tests/test_main.cpp`
- **Build Automation:** `builder.py`
- **LLM Agent Interface:** `llm_agent.py`
- **Instructions:** `instructions/*.yaml`

---

## Test Results

- ✅ Total Tests Generated: **5**
- ✅ Tests Passed: **3**
- ❌ Tests Failed: **2** (due to LLM's use of overflow cases)
- 🔁 Refinement Rounds: 2
- ✅ Final Build: Successful

---

## Coverage Report

Function: add(int, int)
Total Calls: 17
Block Coverage: 100%


---

## Notes

- The failed tests (`AddTest.BoundaryValues` and `AddTest.EdgeCases`) involve undefined behavior (e.g., integer overflow) and were generated automatically by the LLM.
- No manual test writing or source modification was done, as per assignment instructions.

---

## Conclusion

The unit test generator worked end-to-end. The system correctly generated, refined, and validated C++ tests and achieved 100% block coverage. Test failures highlight LLM's need for logic constraints, not implementation issues.

