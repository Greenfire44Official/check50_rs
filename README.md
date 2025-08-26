# check50_rs: Rust extension for check50

An extension for check50 to add support for checking Rust programs.  
Created to enable automated testing of Rust solutions for CS50-style problems.

---

## About

This extension is used by [check50-rust-checks](https://github.com/Greenfire44Official/check50-rust-checks) and may be included in your own check50 tests for Rust.

---

## How to Use

> **Note:**  
> check50's remote server does **not** include Cargo or Rust.  
> This extension is intended for **local use only**.

### Prerequisites

- [Install check50](https://cs50.readthedocs.io/projects/check50/en/latest/#installation)
- [Install Rust and Cargo](https://www.rust-lang.org/tools/install)

### Installation & Usage

1. **Get some tests**
   - You can use [check50-rust-checks](https://github.com/Greenfire44Official/check50-rust-checks):
     ```bash
     git clone https://github.com/Greenfire44Official/check50-rust-checks.git
     ```
  - You can find other tests someone else has made.
  - You can make your own tests.

2. **Add the extension to the test's dependencies**
  Ensure your test's `.cs50.yaml` includes:
   ```yaml
   check50: 
     [other keys]
     dependencies:
       - git+https://github.com/Greenfire44Official/check50_rs.git
       [any other dependency your test may require]
   ```

3. **Run check50 locally with the `--dev` flag:**
   ```bash
   cs50 --dev [path to the folder of the test you want to run]
   ```
   - The path must be to the folder, **not** to `__init__.py` or `.cs50.yaml`.
   - Example for mario-more:
     ```bash
     cs50 --dev [path to check50-rust-checks]/pset1/mario/more
     ```

---

## Troubleshooting

- **ModuleNotFoundError: No module named 'check50_rs'**  
  Install the extension manually:
  ```bash
  pip install git+https://github.com/Greenfire44Official/check50_rs.git
  ```
  - On WSL, add `--break-system-packages`:
    ```bash
    pip install git+https://github.com/Greenfire44Official/check50_rs.git --break-system-packages
    ```
  - To force reinstall (in case of corrupted install):
    ```bash
    pip install --force git+https://github.com/Greenfire44Official/check50_rs.git
    ```

- **Other issues:**  
  Before opening an issue, please ensure:
  - Your issue is not described above.
  - All prerequisites are installed.
  - You've re-read [Installation & Usage](#installation--usage) and made sure you followed the instructions correctly.
  - The code you're testing compiles with `cargo build` or `cargo run`.
  - Your project (package) follows the default folder structure.

If you still have problems, you can submit an issue and I'll try my best to help, just know that I'm still learning, so I may not be able to provide advanced troubleshooting.

---

## Example Usage

See [check50-rust-checks](https://github.com/Greenfire44Official/check50-rust-checks) for example tests and usage instructions. You can clone that repository and run its tests locally to see how this extension works in practice.
