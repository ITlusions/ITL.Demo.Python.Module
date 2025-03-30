import os
from setuptools import setup, find_packages

# Define the base version
BASE_VERSION = "1.3"

# Get the full version from the environment variable or use the base version
version = os.getenv('PACKAGE_VERSION', BASE_VERSION)

setup(
    name="itl-demo-python-module",
    version=version,  # Use the dynamically computed version
    author="Niels Weistra @ ITlusions",
    description="A demo Python package for GitHub Actions CI/CD.",
    package_dir={"": "itl.demo.python.module/src"},  # Point to the correct 'src' directory
    packages=find_packages(where="itl.demo.python.module/src"),  # Correct path to find the packages
    install_requires=[],
    include_package_data=True,
)