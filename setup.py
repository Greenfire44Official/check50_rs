from setuptools import find_packages, setup

setup(
    author="Arturo Brandt",
    author_email="arturobrandt@duck.com",
    classifiers=[
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Topic :: Education",
        "Topic :: Utilities"
    ],
    description="This is check50_rs, a rust extension for check50.",
    license="GPLv3",
    install_requires=["check50>=3,<4"],
    keywords=["check50_rs", "rust"],
    name="check50_rs",
    python_requires=">= 3.6",
    url="https://github.com/Greenfire44Official/check50_rs",
    version="0.1.0",
    include_package_data=True
)