## Problem 1
 Your have to create a Unit test generator for this C++ Application only Use this one

    Task 1: Create a unit test generator tool for C++ applications using a large language model (LLM). The tool will automatically generate unit tests based on the provided C++ code and improve them iteratively.

    Follow the architecture diagram provided and implement a workflow to:
        Generate unit tests.
        Refine the tests based on feedback.
        Handle build issues and improve test coverage.


---
Setup environment

```bash
sudo apt install build-essential cmake g++ libgtest-dev lcov
```

Install Google Test

```bash
cd /usr/src/googletest
sudo mkdir build
cd build
sudo cmake .
sudo make
sudo cp lib/*.a /usr/lib

```
Step 1 : Setup directory

2: Using Groq

Install Groq Python SDK

```bash
pip install groq
```
Use .env file for Groq API

```bash
pip install python-dotenv
```


Directory Structure
```bash

cpp-test-generator/
├── src/                       # Original C++ code
│   └── main.cpp
│
├── tests/                     # Generated and refined unit tests
│   └── test_main.cpp
│
├── instructions/              # YAML instruction files
│   ├── generate.yaml
│   ├── refine.yaml
│   └── fix_build.yaml
│
├── llm_agent.py               # Interface to Ollama
├── generator.py               # Generate & refine tests using YAML
├── builder.py                 # Build project, calculate coverage
├── run.py                     # Main pipeline runner
│
├── report.md                  # Your summary report
└── README.md                  # Usage instructions

```

Architecture

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