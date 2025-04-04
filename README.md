# ITL Demo Python Module

This repository demonstrates a Python package with a fully automated CI/CD pipeline using **GitHub Actions**. The pipeline handles building, versioning, tagging, and releasing the package. The version is dynamically computed during the pipeline and passed to the `setup.py` file via an environment variable.

Additionally, the concepts and workflows described here can be adapted to other CI/CD tools such as **Azure DevOps**, **Tekton**, **Jenkins**, and **TeamCity**, enabling similar automation and dynamic versioning capabilities across different platforms.

---

## **Features**

- **Dynamic Versioning**:
  - Automatically computes the version based on the branch and build context.
  - Increments the patch version for releases on the `main` branch.
  - Appends `.dev.<BUILD_NUMBER>` for development builds on the `develop` branch.
  - Includes the branch name for feature branch builds.
  - Handles **release candidates (RC)** by promoting them to stable releases on `main`.

- **Automated CI/CD**:
  - Builds and tests the package on every push or pull request.
  - Publishes the package to GitHub Packages or PyPI.
  - Pushes a Git tag with the computed version for every release.

- **Python Package Structure**:
  - Includes example functions:
    - `hello()`: Returns a greeting message.
    - `AddFeature()`: Returns a message about a new feature.

---

## **Versioning Logic**

The version number is dynamically computed during the pipeline based on the branch and build context:

1. **`main` Branch**:
   - Promotes release candidates (e.g., `1.0.0-rc1`) to stable releases (e.g., `1.0.0`).
   - Increments the patch version for every new release.
   - Example: `1.0.0` → `1.0.1`.

2. **`develop` Branch**:
   - Appends `.dev.<BUILD_NUMBER>` to the last tag.
   - Example: `1.0.0.dev.42`.

3. **Feature Branches**:
   - Includes the branch name and build number in the version.
   - Example: `1.0.0.feature-name.42`.

4. **Release Candidates**:
   - Tags the first release candidate for a new base version as `1.0.0-rc1`.
   - Subsequent RCs are incremented (e.g., `1.0.0-rc2`).

5. **Other Branches**:
   - Uses the last tag with the build number.
   - Example: `1.0.0.42`.

---

## **Repository Structure**

```plaintext
.
├── itl.demo.python.module/
│   ├── src/
│   │   ├── __init__.py
│   │   ├── main.py
│   └── setup.py
├── .github/
│   └── workflows/
│       └── build-and-publish.yaml
└── README.md
```

### **Key Files**
1. **`itl.demo.python.module/src/__init__.py`**:
   - Contains example functions:
     - `hello()`: Returns a greeting message.
     - `AddFeature()`: Returns a message about a new feature.

2. **`itl.demo.python.module/src/main.py`**:
   - Demonstrates the usage of the `hello()` and `AddFeature()` functions by printing their outputs when executed.

3. **`setup.py`**:
   - Dynamically fetches the version from the `PACKAGE_VERSION` environment variable set by the CI/CD pipeline.
   - Defines the Python package metadata.

4. **`.github/workflows/build-and-publish.yaml`**:
   - Defines the GitHub Actions workflow for CI/CD.
   - Handles building, versioning, tagging, and releasing the package.

---

## **How the Workflow Works**

### **Triggering Events**
The workflow is triggered by:
- **Push Events**:
  - On branches matching `feature/*`, `develop`, or `main`.
- **Pull Request Events**:
  - When a pull request targets `develop` or `main`.

### **CI/CD Workflow**
1. **`ci-build` Job**:
   - Builds and tests the package.

2. **`release` Job**:
   - Computes the version dynamically.
   - Handles release candidates and stable releases.
   - Builds, tags, and publishes the package.

---

## **Examples of Generated Versions**

1. **Push to `main`**:
   - Version: `1.0.1` (patch incremented).
   - Git tag: `1.0.1`.

2. **Push to `develop`**:
   - Version: `1.0.0.dev.42`.
   - Git tag: `1.0.0.dev.42`.

3. **Push to Feature Branch**:
   - Branch: `feature/new-feature`.
   - Version: `1.0.0.new-feature.42`.
   - Git tag: `1.0.0.new-feature.42`.

4. **Release Candidate**:
   - First RC: `1.0.0-rc1`.
   - Subsequent RC: `1.0.0-rc2`.

---

## **How setup.py Uses the Version**

The `setup.py` file dynamically fetches the version from the `PACKAGE_VERSION` environment variable set by the pipeline. Here’s how it works:

```python
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
```

---

## **Automated Releases**

### **Releasing on `main`**
1. Merge a pull request into `main`.
2. The workflow:
   - Increments the patch version.
   - Builds and publishes the package.
   - Pushes a Git tag (e.g., `1.0.1`).

### **Development Builds**
1. Push to `develop`.
2. The workflow:
   - Appends `.dev.<BUILD_NUMBER>` to the version.
   - Builds and publishes the package.

### **Feature Branch Builds**
1. Push to a `feature/*` branch.
2. The workflow:
   - Includes the branch name in the version.
   - Builds the package.

---

## **Contact**

For questions or support, contact **Niels Weistra** at **n.weistra@itlusions.nl**.