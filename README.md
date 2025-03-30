# ITL Demo Python Module

This repository demonstrates a Python package with a fully automated CI/CD pipeline using **GitHub Actions**. The pipeline handles building, versioning, tagging, and releasing the package. The version is dynamically computed during the pipeline and passed to the setup.py file via an environment variable.

Additionally, the concepts and workflows described here can be adapted to other CI/CD tools such as **Azure DevOps**, **Tekton**, **Jenkins**, and **TeamCity**, enabling similar automation and dynamic versioning capabilities across different platforms.

---

## **Features**

- **Dynamic Versioning**:
  - Automatically computes the version based on the branch and build context.
  - Increments the patch version for releases on the `main` branch.
  - Appends `.dev` for development builds on the `develop` branch.
  - Includes the branch name for feature branch builds.

- **Automated CI/CD**:
  - Builds the package on every push or pull request.
  - Publishes the package to GitHub Packages (or PyPI if configured).
  - Pushes a Git tag with the computed version for every release.

- **Python Package Structure**:
  - Includes a simple Python module with example functions.

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

2. **`setup.py`**:
   - Dynamically fetches the version from the `PACKAGE_VERSION` environment variable set by the CI/CD pipeline.
   - Defines the Python package metadata.

3. **`.github/workflows/build-and-publish.yaml`**:
   - Defines the GitHub Actions workflow for CI/CD.
   - Handles building, versioning, tagging, and releasing the package.

---

## **Versioning Logic**

The version number is dynamically computed during the `release` job based on the branch and build context:

1. **`main` Branch**:
   - The patch version is incremented for every release.
   - Example: `1.0.0` → `1.0.1`.

2. **`develop` Branch**:
   - Appends `.dev.<BUILD_NUMBER>` to the last tag.
   - Example: `1.0.0.dev.42`.

3. **Feature Branches**:
   - Includes the branch name and build number in the version.
   - Example: `1.0.0.feature-name.42`.

4. **Other Branches**:
   - Uses the last tag with the build number.
   - Example: `1.0.0.42`.

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
   - Builds the package and verifies the build output.

2. **`release` Job**:
   - Computes the version dynamically.
   - Builds and publishes the package.
   - Pushes a Git tag with the computed version.

---

## **Key Steps in the Workflow**

### **1. Compute Version**
The version is dynamically computed using the following logic:
```bash
git fetch --tags || true
LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "1.0.0")
BUILD_NUMBER=${{ github.run_number }}

# Extract major, minor, and patch versions
MAJOR=$(echo $LAST_TAG | cut -d'.' -f1)
MINOR=$(echo $LAST_TAG | cut -d'.' -f2)
PATCH=$(echo $LAST_TAG | cut -d'.' -f3)

if [[ "${{ github.ref }}" == 'refs/heads/main' ]]; then
  # Increment the patch version for releases on main
  PATCH=$((PATCH + 1))
  FULL_VERSION="${MAJOR}.${MINOR}.${PATCH}"
elif [[ "${{ github.ref }}" == 'refs/heads/develop' ]]; then
  # Use a development version for develop
  FULL_VERSION="${LAST_TAG}.dev.${BUILD_NUMBER}"
elif [[ "${{ github.ref }}" == refs/heads/feature/* ]]; then
  # Include the branch name for feature branches
  BRANCH_NAME=$(echo "${{ github.ref }}" | cut -d'/' -f4)
  FULL_VERSION="${LAST_TAG}.${BRANCH_NAME}.${BUILD_NUMBER}"
else
  # Default version for other branches
  FULL_VERSION="${LAST_TAG}.${BUILD_NUMBER}"
fi

echo "Computed version: $FULL_VERSION"
echo "PACKAGE_VERSION=$FULL_VERSION" >> $GITHUB_ENV
```

### **2. Push Git Tag**
After computing the version, the workflow creates and pushes a Git tag:
```bash
git config --global user.email "info@itlusions.nl"
git config --global user.name "ActionsBot"
git tag -a $PACKAGE_VERSION -m "Release $PACKAGE_VERSION"
git push origin $PACKAGE_VERSION
```

---

## **How setup.py Uses the Version**

The setup.py file dynamically fetches the version from the `PACKAGE_VERSION` environment variable set by the pipeline. Here’s how it works:

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

### **Key Points**
1. **Dynamic Versioning**:
   - The `version` is fetched from the `PACKAGE_VERSION` environment variable.
   - If the variable is not set (e.g., during local development), it defaults to `1.0.0`.

2. **Integration with the Workflow**:
   - The pipeline computes the version and sets the `PACKAGE_VERSION` variable before running setup.py.

3. **Reproducibility**:
   - Ensures that the version in the package matches the version in the Git tag and release.

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

## **Next Steps: Enhancing Version Control**
To improve versioning, consider implementing the following:

1. **Manual Control of Major and Minor Versions**:
    - Use environment variables to store the current major and minor versions.
    - Update these variables manually when incrementing major or minor versions.

2. **Automated Workflow Integration**:
    - Modify the CI/CD workflow to read the environment variables for base versioning.
    - Dynamically compute the patch version and build metadata.

3. **Automating Major and Minor Updates**:
    - Create a script to increment the major or minor version based on input.
    - Update the environment variables automatically using the script.


These steps provide flexibility for managing breaking changes (major versions) and new features (minor versions) while maintaining automation for patch and build versions.

---

## **Contact**

For questions or support, contact **Niels Weistra** at **info@itlusions.nl**.

