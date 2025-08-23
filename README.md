# check50_rs: a Rust extension for check50
An extension for check50 to add support for checking rust. Pretty self explanatory.

## How to use

Since check50's remote server does not come with cargo (and I doubt there's a way to add it as a requirement) it is not possible to use this extension for online checks.\
I haven't tested compiling with rustc, but if cargo is not installed on the server, I doubt rustc is either.\
In order to use this extension you have to run it locally.

### Pre-requisites
Install check50:\
https://cs50.readthedocs.io/projects/check50/en/latest/#installation 

Since you are going to be running the tests locally make sure that you have everything you need to compile your rust code and packages:\
https://www.rust-lang.org/tools/install 

Get some tests. You can either create your own or download tests some else made.\
Here are some tests I created to replicate cs50x's c problems in rust:\
https://github.com/Greenfire44Official/check50-rust-checks
`git clone https://github.com/Greenfire44Official/check50-rust-checks.git`

### Installing and using
First setup your custom checks or clone/download someone else's tests.\
Make sure that each of the tests' .cs50.yaml contains:
```yaml
check50: 
  [other keys]
  dependencies:
    - git+https://github.com/Greenfire44Official/check50_rs.git
    [any other dependency your test may require]
```
Then make sure that the tests utilize the methods implemented by check50_rs (currently only one method, the "compile" method, has been added, and tbh I doubt any other method will be added).

That's it! Your tests now use the check50_rs extension!

To actually run the tests you can follow the instructions bellow.

### Running tests

First cd into the root directory of the project/package where Cargo.toml is located **not the src folder.** and also **not the root folder of the cargo workspace** (if you are working on a cargo workspace).

By default, this extension requires that the packages are created using the default cargo folder structure.\
That is:
```bash
└── [package name]
    ├── src
    │   ├── main.rs <-- Required. Important: do not change the name of the source file. It **must** be main.rs
    ├── Cargo.lock <-- Will be included if it exists, but it's not required.
    ├── Cargo.toml <-- Required.
    └── * <-- Any other file will be excluded.
```
If your package does not follow this folder structure the check will fail.\
However, you **are** running this locally, so there's nobody stopping you from modifying the check's .cs50.yaml and \_\_init__.py to support your custom folder structure.

Now run check50 using the --dev flag. (If you run it without the --dev flag, even if you are using the --local or --offline flags, the test won't work. I haven't figured out why)\
`cs50 --dev [path to the **folder** of the test you want to run]` (the path **must** be of the folder, not to the \_\_init__.py, nor the .cs50.yaml files. It **must** be the folder.

For example, if you are using the tests I created from check50-rust-checks for mario-more (see pre-requisites) the command would look like:\
`cs50 --dev [path to check50-rust-checks's root folder]/pset1/mario/more`

The test should now run. If the test doesn't run or you encounter a different problem you can create an issue if **(and only if)**:\
+ Your issue is not described in [Basic troubleshooting](#basic-troubleshooting).
+ You've installed all the pre-requisites.
+ You're sure you followed the instructions correctly.
+ You're sure that the code you are testing compiles correctly using `cargo build` or `cargo run`.
+ Your cargo project follows the default folder file structure described in [Installing and using](#installing-and-using).

Once you've made sure of those points, if you still have problems you can submit an issue and I'll attempt to help you. Just take into consideration that I'm still learning to code and won't be able to provide advanced troubleshooting.

## Basic troubleshooting
If you get the following error: `ModuleNotFoundError: No module named 'check50_rs'` It likely means that check50 did not automatically install the check50_rs extension. You can manually install it using pip:\
`pip install git+https://github.com/Greenfire44Official/check50_rs.git` \
If you are using WSL you will likely encounter an error like: `error: externally-managed-environment` To fix this add the `--break-system-packages` flag like so:\
`pip install git+https://github.com/Greenfire44Official/check50_rs.git --break-system-packages` \
Additionally if you get a message about the package already being installed and you still get the same package not found error you can force a reinstallation of the package adding the `--force` flag.
