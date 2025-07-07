from llm_agent import call_llm

def generate_tests(cpp_code: str, yaml_rules: str) -> str:
    prompt = f"""Follow this YAML instruction and generate C++ unit tests using Google Test.

YAML:
{yaml_rules}

Code:
```cpp
{cpp_code}
"""
    return call_llm(prompt)

def refine_tests(cpp_code: str, current_tests: str, yaml_rules: str) -> str:
    prompt = f"""Refine the following C++ unit tests using the YAML instructions.

YAML:
{yaml_rules}

Code:
```cpp
{cpp_code}

Current Unit Tests:
{current_tests}

"""

    return call_llm(prompt)

def fix_tests(cpp_code: str, current_tests: str, yaml_rules: str, build_errors: str) -> str:
    prompt = f"""Fix the following unit tests based on the YAML rules and build errors.

YAML:
{yaml_rules}

C++ Source Code:
```cpp
{cpp_code}

Current Unit Tests:
{current_tests}

Build Errors:
{build_errors}

"""

    return call_llm(prompt)