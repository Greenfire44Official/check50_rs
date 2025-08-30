"""
Based on check50's C extension https://github.com/cs50/check50/blob/main/check50/c.py
"""

# import contextlib
import re
from pathlib import Path
from check50 import run, log, Failure

#: Default compiler for :func:`check50_rs.compile`
CC = "cargo"

#: Default CFLAGS for :func:`check50_rs.compile`
CFLAGS = {}


def compile(*files, exe_name=None, cc=CC, max_log_lines=50, timeout=60, **cflags):
    """
    Based on check50's C extension compile function
    Compiles Rust source files.

    :param files: filenames to be compiled
    :param exe_name: name of resulting executable. Optional
    :param cc: compiler to use. Default: cargo
    :param max_log_lines: maximum lines to be logged when compilation fails. Default: 50
    :param timeout: maximum allowed compilation time. Default: 60
    :param cflags: additional flags to pass to the compiler
    :raises check50.Failure: if compilation failed (i.e., if the compiler returns a non-zero exit status).
    :raises RuntimeError: if no filenames are specified

    If cc is "cargo" (default) the compilation will ignore the provided 
    `files` and `exe_name` since cargo takes care of that through Cargo.toml
    
    If `exe_name` is None, this function will attempt to find the executable name from the provided files.
    (.rs or Cargo.toml)

        check50_rs.compile("foo.rs") # cargo build

    Additional CFLAGS may be passed as keyword arguments like so::

        check50_rs.compile("foo.rs", baz=True) # cargo build -baz
        
    Compiler can be changed like so::
        check50_rs.compile("foo.rs", exe_name="foo", cc="rustc", baz="bar") # rustc -o foo foo.rs -baz=bar
    """

    if not files:
        raise RuntimeError(_("compile requires at least one file"))  # type: ignore

    if exe_name is None:
        rs_file = next((f for f in files if f.endswith(".rs")), None)
        cargo = next((f for f in files if f == "Cargo.toml"), None)
        if rs_file:
            exe_name = Path(rs_file).stem
        elif cargo:
            content = Path(cargo).read_text()
            match = re.search(
                r'^\s*\[package\][^\[]*?\s*name\s*=\s*["\']([^"\']+)["\']',
                content,
                re.MULTILINE | re.DOTALL,
            )
            if match:
                exe_name = match.group(1)
            else:
                raise RuntimeError(
                    """Could not determine executable name.
                    No exe_name provided and could not find .rs and could not parse Cargo.toml"""
                )
        else:
            raise RuntimeError(
                """Could not determine executable name.
                No exe_name provided and could not find .rs file nor Cargo.toml"""
            )

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
        process = run(f"{cc} build{flags}")
    else:
        process = run(f"{cc} {files}{out_flag}{flags}")

    # Strip out ANSI codes
    stdout = re.sub(r"\x1B\[[0-?]*[ -/]*[@-~]", "", process.stdout(timeout=timeout))  # type: ignore

    # Log max_log_lines lines of output in case compilation fails
    if process.exitcode != 0:
        lines = stdout.splitlines()

        if len(lines) > max_log_lines:
            lines = lines[: max_log_lines // 2] + lines[-(max_log_lines // 2) :]

        for line in lines:
            log(line)

        raise Failure("code failed to compile")


def run_and_wait(
    cmd,
    timeout=2,
    log_message="checking that program did not exit...",
    failure_message="Program exited when it should have waited for input.",
):
    """
    Runs a command and checks that it does NOT exit within the specified timeout.
    
    Useful for checking if a program is waiting for input when first running the program.
    
    Logs a custom message instead of the default hardcoded message 'checking that input was rejected' from check50.reject().
    
    Works similarly to check50.reject(), but with custom log messages.

    :param cmd: command to run
    :param timeout: time to wait for program to NOT exit.
    :param log_message: message to be logged before command is run
    :param failure_message: check50.Failure message if program exits before the timeout.
    
    :raises check50.Failure: with a custom failure message if the program exits.
    """
    process = run(cmd)
    log(log_message)
    try:
        process.exit(timeout=timeout)
        raise Failure(failure_message)
    except Exception:
        # If a timeout occurs, this is expected (program did not exit)
        pass
