from generator import generate_tests, refine_tests, fix_tests
from builder import build_and_run_tests, calculate_coverage
import os, re, pathlib

# ---------- helpers ----------
def load_text(path: str) -> str:
    with open(path, "r") as f:
        return f.read()

def save_text(path: str, data: str):
    pathlib.Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        f.write(data)

# ---------- very strict cleaner ----------
MARKDOWN_FENCES   = re.compile(r"^```.*$")                 # ``` or ```cpp
CLI_COMMANDS      = re.compile(r"^\s*(g\+\+|clang\+\+).*$")# build commands
LLM_CHAT_NOISE    = re.compile(r"^\s*(I\s+|Changes made:|Fixed|Explanation:).*")
THREAD_HEADERS    = re.compile(r'#include\s*<.*(thread|mutex|condition_variable).*?>')
SOURCE_INCLUDES   = re.compile(r'#include\s*"(main\.cpp|main\.h)"')
ASTERISK_COMMENTS = re.compile(r"^\s*\*.*$")


def clean_llm_output(raw: str) -> str:
    """Remove markdown / chat narration / cli commands / forbidden includes."""
    lines = []
    for line in raw.splitlines():
        if (MARKDOWN_FENCES.match(line) or
            CLI_COMMANDS.match(line)   or
            LLM_CHAT_NOISE.match(line) or
            THREAD_HEADERS.search(line)or
            SOURCE_INCLUDES.search(line)or
            ASTERISK_COMMENTS.match(line)):
            continue
        lines.append(line)

    # drop everything before first #include
    while lines and not lines[0].lstrip().startswith("#include"):
        lines.pop(0)

    code = "\n".join(lines).strip() + "\n"

    # ---------- auto‑patch missing pieces ----------
    need_climits = ("INT_MAX" in code or "INT_MIN" in code) and "#include <climits>" not in code
    need_add_decl = ("add(" in code) and "extern int add" not in code

    patched = []
    inserted_header = False
    for ln in code.splitlines():
        patched.append(ln)
        if not inserted_header and ln.lstrip().startswith("#include") and need_climits:
            patched.append("#include <climits>")
            inserted_header = True
    code = "\n".join(patched) if patched else code

    if need_add_decl:
        lines = code.splitlines()
        ix = max(i for i, l in enumerate(lines) if l.lstrip().startswith("#include"))
        lines.insert(ix + 1, "extern int add(int, int);")
        code = "\n".join(lines)

    return code + "\n"

def save_tests(content: str, path="tests/test_main.cpp"):
    save_text(path, clean_llm_output(content))

def log_error(msg: str, name="build_logs/build_error.txt"):
    save_text(name, msg)

# ---------- main driver ----------
def main():
    cpp_code       = load_text("src/main.cpp")
    generate_yaml  = load_text("instructions/generate.yaml")
    refine_yaml    = load_text("instructions/refine.yaml")
    fix_build_yaml = load_text("instructions/fix_build.yaml")

    print("🧪 Generating unit tests...")
    test_code = generate_tests(cpp_code, generate_yaml)
    test_code = clean_llm_output(test_code)
    save_tests(test_code)

    print("🔨 Building and testing...")
    output, errors = build_and_run_tests()

    for i in range(3):
        if not errors:
            break
        print(f"🔧 Refinement round {i+1} (build failed)…")
        test_code = refine_tests(cpp_code, test_code, refine_yaml)
        test_code = clean_llm_output(test_code)
        save_tests(test_code)
        output, errors = build_and_run_tests()

    if errors:
        print("🛠  Final fix attempt with fix_build.yaml …")
        test_code = fix_tests(cpp_code, test_code, fix_build_yaml, errors)
        test_code = clean_llm_output(test_code)
        save_tests(test_code)
        output, errors = build_and_run_tests()

    if errors:
        print("❌  Build still failing – see build_logs/final_build_error.txt")
        log_error(errors, "build_logs/final_build_error.txt")
    else:
        print("✅  Tests passed!\n", output)
        print("📊  Coverage:\n", calculate_coverage())

if __name__ == "__main__":
    main()
