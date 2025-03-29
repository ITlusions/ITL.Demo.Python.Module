import os
from setuptools import setup, find_packages

# Get version from environment variable
version = os.getenv('PACKAGE_VERSION', '1.0.0')  # Default to '1.0.0' if the variable is not set

setup(
    name="itl-demo-python-module",
    version=version,  # Use version from the environment variable
    author="Niels Weistra @ ITlusions",
    description="A demo Python package for GitHub Actions CI/CD.",
    package_dir={"": "itl.demo.python.module/src"},  # Point to the correct 'src' directory
    packages=find_packages(where="itl.demo.python.module/src"),  # Correct path to find the packages
    install_requires=[],
    include_package_data=True,
)
