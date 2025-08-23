"""
Based on check50's c extension https://github.com/cs50/check50/blob/main/check50/c.py
"""

# import contextlib
import re
from pathlib import Path
from check50 import run, log, Failure

#: Default compiler for :func:`check50_rs.compile`
CC = "cargo"

#: Default CFLAGS for :func:`check50_rs.compile`
CFLAGS = {}


def compile(*files, exe_name=None, cc=CC, max_log_lines=50, **cflags):
    """
    Compile Rust source files.

    :param files: filenames to be compiled
    :param exe_name: name of resulting executable
    :param cc: compiler to use (:data:`check50_rs.CC` by default)
    :param cflags: additional flags to pass to the compiler
    :raises check50.Failure: if compilation failed (i.e., if the compiler returns a non-zero exit status).
    :raises RuntimeError: if no filenames are specified

    If ``exe_name`` is None, :func:`check50_rs.compile` will default to the first
    file specified sans the ``.c`` extension::


        check50_rs.compile("foo.rs", "bar.rs") # cargo build

    Additional CFLAGS may be passed as keyword arguments like so::

        check50_rs.compile("foo.rs", "bar.rs", baz=True) # cargo build -baz
    """

    if not files:
        raise RuntimeError(_("compile requires at least one file"))  # type: ignore

    if exe_name is None and files[0].endswith(".rs"):
        exe_name = Path(files[0]).stem

    files = " ".join(files)

    flags = CFLAGS.copy()
    flags.update(cflags)
    flags = " ".join(
        (f"-{flag}" + (f"={value}" if value is not True else "")).replace("_", "-")
        for flag, value in flags.items()
        if value
    )

    out_flag = f" -o {exe_name} " if exe_name is not None else " "

    if CC == "cargo":
        process_exit_code = run(f"{cc} build{flags}").exit(code=0, timeout=20)
    else:
        process_exit_code = run(f"{cc} {files}{out_flag}{flags}").exit(code=0, timeout=20)

    # Strip out ANSI codes
    stdout = re.sub(r"\x1B\[[0-?]*[ -/]*[@-~]", "", process_exit_code.stdout())  # type: ignore

    # Log max_log_lines lines of output in case compilation fails
    if process_exit_code != 0:
        lines = stdout.splitlines()

        if len(lines) > max_log_lines:
            lines = lines[: max_log_lines // 2] + lines[-(max_log_lines // 2) :]

        for line in lines:
            log(line)

        raise Failure("code failed to compile")
