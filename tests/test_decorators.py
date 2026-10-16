import pytest
from pathlib import Path
from typing import Any

from src.decorators import log


def test_log_success_in_console(capsys: Any) -> None:
    @log()
    def add(x: int, y: int) -> int:
        return x + y

    result = add(1, 2)
    output = capsys.readouterr().out

    assert result == 3
    assert "add started" in output
    assert "add ok" in output


def test_log_error_in_console(capsys: Any) -> None:
    @log()
    def divide(x: int, y: int) -> float:
        return x / y

    with pytest.raises(ZeroDivisionError):
        divide(1, 0)

    output = capsys.readouterr().out

    assert "divide started" in output
    assert "divide error: ZeroDivisionError" in output
    assert "Inputs: (1, 0), {}" in output


def test_log_to_file(tmp_path: Path) -> None:
    log_file = tmp_path / "mylog.txt"

    @log(filename=str(log_file))
    def add(x: int, y: int) -> int:
        return x + y

    assert add(1, 2) == 3

    output = log_file.read_text(encoding="utf-8")
    assert "add started" in output
    assert "add ok" in output
