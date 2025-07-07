![Version](https://img.shields.io/badge/version-v1.0.0-blue)

# TestForge: A C++ Unit Test Generator using LLM

This project automatically generates, refines, builds, and evaluates unit tests for a given C++ source file using a Groq (Model: llama3-70b-8192), you can also use a self-hosted LLM (e.g., LLaMA or Ollama). I didn't used self hosted LLM because of lack of hardware resources. My PC wasn't able to handle model, So, I used Groq API here. It follows a defined pipeline controlled by YAML instruction files and integrates with Google Test for building and test coverage analysis.



## Features

1. Uses Groq LLM model(llama3-70b-8192) or you can also use self-hosted LLM (like LLaMA/Ollama) to generate unit tests
2. Refines tests based on build feedback and code coverage
3. Integrates with Google Test
4. Automatically fixes build errors using LLM and YAML prompts
5. Measures and reports code coverage
6. Final test suite is formatted, optimized, and free of duplication


## Technologies Used

- C++17
- Google Test
- Python
- Groq API
- YAML
- gcov for coverage
- Linux
- VS Code

## Prerequisites

1. Python 3.10+
2. g++ with gcov
3.  Google Test
4. Self-hosted LLM backend (e.g., Ollama, LM Studio, or via API)


## How to setup this project:

1. Setup environment for C++ Source Code:

```bash
sudo apt install build-essential cmake g++ libgtest-dev lcov
```

2. Install Google Test for testing:

```bash
cd /usr/src/googletest
sudo mkdir build
cd build
sudo cmake .
sudo make
sudo cp lib/*.a /usr/lib

```

3. Setup your directory

### Directory Structure

```bash
TestForge/
├── builder.py                 # Build project, calculate coverage
│
├── build_logs                 # Build failure logs
│   └── final_build_error.txt
│
├── generator.py               # Generate & refine tests using YAML
│
│               
├── instructions               # YAML instruction files
│   ├── fix_build.yaml
│   ├── generate.yaml
│   └── refine.yaml
│
│
├── llm_agent.py                 # Interface to Groq
├── main.cpp.gcov                # Code coverage report
├── Readme.MD                    # Usage instructions
├── report.md                    # Final Converage and summary report
├── run.py                       # Main driver script
│
├── src
│   └── main.cpp                 # Original C++ code
│
├── test_exec
└── tests
│    └── test_main.cpp           # Generated and refined unit tests
│
└── .env                        # Groq API
│
└── .gitignore                   # Git exclusion rules
```
4. Activate your environment
```bash
# I am using uv to create Python Virtual Enviroment

uv venv                            # Create Virtual Environment
source .venv/bin/activate          # Activating Venv

# You can use pip to create virtual environment also
```

5. Using Groq: Install Groq Python SDK

```bash
pip install groq
```
6. Use .env file for Groq API, to use .env install:

```bash

uv pip install python-dotenv # when using uv

#or

pip install python-dotenv   # when using pip directly
```

7. Setup API in .env at root of the directory:

```bash
GROQ_API_KEY=PASTE_YOUR_API_KEY_HERE
```
8. Run the main pipeline
```python
python3 run.py
```

### Check results

    tests/test_main.cpp: Generated tests

    build_logs/: Logs for failed builds (if any)

    main.cpp.gcov: Coverage output

    report.md: Final summary

## Architecture of the project

```bash

                ┌────────────────────────────┐
                │      C++ Source Code       │
                └────────────┬───────────────┘
                             │
                             ▼
                ┌────────────────────────────┐
                │   Test Generator (LLM)     │ ◄──┐
                └────────────┬───────────────┘    │
                             │                    │
                             ▼                    │
                 ┌──────────────────────────┐     │
                 │  Generated Unit Tests    │     │
                 └────────────┬─────────────┘     │
                              │                   │
                              ▼                   │
             ┌─────────────────────────────┐      │
             │  Build & Run Test Suite     │──────┘
             └────────────┬────────────────┘
                          │
                          ▼
        ┌────────────────────────────────────────┐
        │ Collect Build/Runtime Feedback & Logs │
        └────────────────────────────────────────┘
                          │
                          ▼
      ┌──────────────────────────────────────────┐
      │   LLM Analyzes Failures & Refines Tests │
      └──────────────────────────────────────────┘

```
## How It Works

1. Initial Test Generation:
- Sends src/main.cpp with instructions/generate.yaml to the LLM to create initial unit tests.

2. Test Refinement:
- If tests fail to build, it sends refine.yaml and build output back to the LLM.

3. Final Fix (if needed):
- If still failing, fix_build.yaml guides the LLM to repair the test file.

4. Test Execution:
- Runs the tests using g++, and collects pass/fail results and coverage metrics.

## Note
- The source file (main.cpp) is not modified at any step.
- Only tests/test_main.cpp is regenerated and refined.
- Can be extended to support multiple .cpp files or full C++ projects.