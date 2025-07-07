import subprocess
import os
import glob

SRC_DIR = "src"
TEST_DIR = "tests"
OUTPUT_EXEC = "test_exec"

def clean_coverage_files():
    for pattern in ["*.gcda", "*.gcno", "*.gcov", f"{SRC_DIR}/*.gcda", f"{SRC_DIR}/*.gcno", f"{SRC_DIR}/*.gcov"]:
        for file in glob.glob(pattern):
            try:
                os.remove(file)
            except FileNotFoundError:
                continue

def build_and_run_tests() -> tuple[str, str]:
    try:
        clean_coverage_files()

        # Compile source files separately to ensure gcno files go in correct directories
        subprocess.run([
            "g++", "-std=c++17", "-fprofile-arcs", "-ftest-coverage", "-c",
            f"{SRC_DIR}/main.cpp", "-o", f"{SRC_DIR}/main.o"
        ], check=True)

        subprocess.run([
            "g++", "-std=c++17", "-fprofile-arcs", "-ftest-coverage", "-c",
            f"{TEST_DIR}/test_main.cpp", "-o", f"{TEST_DIR}/test_main.o"
        ], check=True)

        # Link object files to create executable
        subprocess.run([
            "g++",
            f"{SRC_DIR}/main.o", f"{TEST_DIR}/test_main.o",
            "-lgtest", "-lgtest_main", "-pthread",
            "-fprofile-arcs", "-ftest-coverage", "-lgcov",  # ✅ Add these
            "-o", OUTPUT_EXEC
        ], check=True)

        # Run tests
        result = subprocess.run([f"./{OUTPUT_EXEC}"], capture_output=True, text=True)
        return result.stdout, result.stderr

    except subprocess.CalledProcessError as e:
        return "", f"Build/Run failed:\n{e.stderr or e.stdout}"

def calculate_coverage() -> str:
    try:
        result = subprocess.run(
            ["gcov", "-b", "-c", f"{SRC_DIR}/main.cpp"],
            capture_output=True, text=True
        )
        # Output will be in 'main.cpp.gcov'
        cov_file = os.path.basename(f"{SRC_DIR}/main.cpp.gcov")
        if os.path.exists(cov_file):
            with open(cov_file, "r") as f:
                return f.read()
        return result.stdout + result.stderr
    except subprocess.CalledProcessError as e:
        return f"Error running gcov: {e.stderr or e.stdout}"
