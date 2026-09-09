#!/usr/bin/env python3
"""Small C++17 local judge. Never writes the submitted source."""

import argparse
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def compiler():
    configured = os.environ.get("CXX")
    if configured:
        return configured
    found = shutil.which("g++")
    if found:
        return found
    local = ROOT / "tools/compiler-path.txt"
    if local.is_file():
        path = Path(local.read_text(encoding="utf-8-sig").strip())
        return str(path if path.is_absolute() else ROOT / path)
    raise ValueError("找不到 g++；请加入 PATH 或设置 CXX 为编译器完整路径。")


def current_problem(root=ROOT):
    progress = (root / "progress.md").read_text(encoding="utf-8")
    if "当前模式：模拟" in progress:
        raise ValueError("模拟期间请明确提交题目，并传入该编程题目录。")
    match = re.search(r"^当前题目：\s*(\S+)\s*$", progress, re.MULTILINE)
    if not match:
        raise ValueError("progress.md 未设置当前题目。")
    return root / match.group(1)


def normalize(data):
    # Preserve leading/internal whitespace and line structure.
    lines = [
        line.rstrip(b" \t")
        for line in data.replace(b"\r\n", b"\n").split(b"\n")
    ]
    while lines and not lines[-1]:
        lines.pop()
    return lines


def show(data):
    return data.decode("utf-8", errors="replace") if data else "(empty)"


def test_pairs(problem):
    inputs = sorted((problem / "tests").glob("*.in"))
    outputs = set((problem / "tests").glob("*.out"))
    if len(inputs) < 8:
        raise ValueError("测试集必须至少包含 8 组 .in / .out。")
    if {p.with_suffix(".out") for p in inputs} != outputs:
        raise ValueError("测试集的 .in / .out 文件不成对。")
    return [(p, p.with_suffix(".out")) for p in inputs]


def judge(problem, cxx, timeout):
    source = problem / "main.cpp"
    if not source.is_file():
        raise ValueError(f"找不到源文件：{source}")
    pairs = test_pairs(problem)
    with tempfile.TemporaryDirectory(prefix="cpp-judge-") as tmp:
        executable = Path(tmp) / ("main.exe" if os.name == "nt" else "main")
        env = os.environ.copy()
        resolved_cxx = shutil.which(cxx) or cxx
        env["PATH"] = str(Path(resolved_cxx).resolve().parent) + os.pathsep + env.get("PATH", "")
        print(f"C++ compiler: {resolved_cxx}")
        print("Build: main.cpp -> native executable (C++17, -O2, -Wall)")
        try:
            built = subprocess.run(
                [cxx, "main.cpp", "-std=c++17", "-O2", "-Wall", "-o", str(executable)],
                cwd=problem, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                timeout=30,
            )
        except subprocess.TimeoutExpired:
            print("Compile Error\n编译超过 30 秒。")
            return "Compile Error"
        if built.returncode:
            print("Compile Error")
            print("\n".join(show(built.stdout).splitlines()[:30]))
            return "Compile Error"
        if built.stdout:
            print(show(built.stdout))
        print(f"Run native executable: {executable}")
        passed = 0
        for inp, out in pairs:
            data, expected = inp.read_bytes(), out.read_bytes()
            # ponytail: capture to disk; no output quota for trusted local practice.
            # Add bounded output/process isolation if accepting untrusted submissions.
            with tempfile.TemporaryFile() as stdout, tempfile.TemporaryFile() as stderr:
                try:
                    run = subprocess.run(
                        [str(executable)], input=data, stdout=stdout, stderr=stderr,
                        cwd=tmp, env=env, timeout=timeout,
                    )
                    stdout.seek(0)
                    actual = stdout.read()
                    verdict = "RUNTIME ERROR" if run.returncode else (
                        "PASS" if normalize(actual) == normalize(expected) else "WRONG ANSWER"
                    )
                except subprocess.TimeoutExpired:
                    verdict = "TIME LIMIT"
                print(f"Test {inp.stem}: {verdict}")
                if verdict == "PASS":
                    passed += 1
                elif verdict == "WRONG ANSWER":
                    print(f"Test:\n{inp.stem}\nInput:\n{show(data)}\nExpected:\n{show(expected)}\nActual:\n{show(actual)}")
                    print("可能类别（需结合代码确认）：边界条件、下标、输入读取、状态更新/清空、并列规则、整数溢出。")
                elif verdict == "RUNTIME ERROR":
                    stderr.seek(0)
                    print(f"Exit code: {run.returncode}\n{show(stderr.read())}")
        print(f"Result: {passed} / {len(pairs)} Passed")
        if passed == len(pairs):
            print(f"Accepted\n{passed} / {len(pairs)} Passed")
            return "Accepted"
        return f"未通过（{passed}/{len(pairs)}）"


def update_progress(problem, status):
    progress = ROOT / "progress.md"
    if problem.parent != ROOT / "problems" or not progress.is_file():
        return
    number = problem.name.split("-", 1)[0]
    lines = progress.read_text(encoding="utf-8").splitlines()
    for index, line in enumerate(lines):
        cells = [cell.strip() for cell in line.split("|")]
        if len(cells) == 9 and cells[1] == number:
            cells[5] = status
            lines[index] = "| " + " | ".join(cells[1:-1]) + " |"
            progress.write_text("\n".join(lines) + "\n", encoding="utf-8")
            break


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("problem", nargs="?", help="题目目录；默认读取 progress.md")
    parser.add_argument("--timeout", type=float, default=2.0, help="每组运行秒数，默认 2")
    args = parser.parse_args()
    try:
        if not math.isfinite(args.timeout) or args.timeout <= 0:
            raise ValueError("运行时限必须是有限正数。")
        if args.problem:
            problem = Path(args.problem)
            if not problem.is_absolute() and not problem.is_dir():
                problem = ROOT / problem
        else:
            problem = current_problem()
        problem = problem.resolve()
        status = judge(problem, compiler(), args.timeout)
        update_progress(problem, status)
        return 0 if status == "Accepted" else 1
    except (OSError, ValueError) as exc:
        print(f"Judge Error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main())
