# ITL Demo Python Module

This repository demonstrates a Python package with a fully automated CI/CD pipeline using **GitHub Actions**. The pipeline handles building, versioning, tagging, and releasing the package. The version is dynamically computed during the pipeline and passed to the `setup.py` file via an environment variable.

Additionally, the concepts and workflows described here can be adapted to other CI/CD tools such as **Azure DevOps**, **Tekton**, **Jenkins**, and **TeamCity**, enabling similar automation and dynamic versioning capabilities across different platforms.

---

## **Features**

```mermaid
graph TD
    A[Push or Pull Request] -->|Trigger Workflow| B[ci-build Job]
    B -->|Build Package| C[Compute Version]
    C -->|Set PACKAGE_VERSION| D{Branch Check}
    D -->|main| E[Release to Production]
    D -->|develop| F[Release to Development]
    D -->|feature/*| G[Skip Release Job]
    E -->|Tag and Publish| H[GitHub Release]
    F -->|Tag and Publish| H[GitHub Release]
```

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

- **Dynamic Environments**:
  - Automatically assigns the correct environment based on the branch:
    - `main` → `production`
    - `develop` → `development`

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
│   └── [setup.py](./itl.demo.python.module/setup.py)
├── .github/
│   └── workflows/
│       └── [build-and-publish.yaml](./.github/workflows/build-and-publish.yaml)
└── [README.md](./README.md)
```