"""Run with python tools/test_judge.py; requires the configured g++."""

from contextlib import redirect_stdout
import io
from pathlib import Path
import tempfile

import judge


def main():
    assert judge.normalize(b"1 2 \r\n\n") == judge.normalize(b"1 2\n")
    assert judge.normalize(b" 1 2") != judge.normalize(b"1 2")
    assert judge.normalize(b"1  2") != judge.normalize(b"1 2")
    assert judge.normalize(b"1\n2") != judge.normalize(b"1 2")
    cxx = judge.compiler()
    with tempfile.TemporaryDirectory(prefix="judge-selftest-") as tmp:
        root = Path(tmp)
        (root / "progress.md").write_text("当前题目：problems/example\n", encoding="utf-8")
        assert judge.current_problem(root) == root / "problems/example"
        (root / "tests").mkdir()
        for i in range(1, 9):
            (root / f"tests/{i:02}.in").write_text(f"{i}\n", encoding="utf-8")
            (root / f"tests/{i:02}.out").write_text(f"{i}\n", encoding="utf-8")
        source = root / "main.cpp"
        source.write_text('#include <iostream>\nint main(){int n; std::cin>>n; std::cout<<n<<"\\n";}\n', encoding="utf-8")
        before = source.read_bytes()
        with redirect_stdout(io.StringIO()) as output:
            assert judge.judge(root, cxx, 2) == "Accepted"
        assert "8 / 8 Passed" in output.getvalue()
        assert source.read_bytes() == before
        source.write_text('''#include <iostream>
#include <thread>
#include <chrono>
int main(){int n; std::cin>>n;
if(n==3){std::cout<<0; return 0;}
if(n==4) return 1;
if(n==5) std::this_thread::sleep_for(std::chrono::seconds(2));
std::cout<<n;}
''', encoding="utf-8")
        before = source.read_bytes()
        with redirect_stdout(io.StringIO()) as output:
            assert judge.judge(root, cxx, 0.5) == "未通过（5/8）"
        for text in ("Test 03: WRONG ANSWER", "Test 04: RUNTIME ERROR", "Test 05: TIME LIMIT", "Test 08: PASS", "Expected:", "Actual:"):
            assert text in output.getvalue(), output.getvalue()
        assert source.read_bytes() == before
        source.write_text("int main( {", encoding="utf-8")
        with redirect_stdout(io.StringIO()) as output:
            assert judge.judge(root, cxx, 2) == "Compile Error"
        assert "Compile Error" in output.getvalue()
        (root / "tests/08.out").unlink()
        try:
            judge.test_pairs(root)
        except ValueError:
            pass
        else:
            raise AssertionError("Missing expected output must fail")
    print("Judge self-check: PASS (AC, WA, RE, TLE, CE, source preservation, test validation)")


if __name__ == "__main__":
    main()
