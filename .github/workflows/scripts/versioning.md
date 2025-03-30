# Versioning Script

This script dynamically computes a version number based on the Git repository's state, branch, and build context. It is designed for use in CI/CD pipelines to automate versioning.

---

## **Features**

- Computes versions based on the latest Git tag, branch, and build number.
- Supports development builds, feature branch builds, and release candidates (RC).
- Outputs the computed version for use in CI/CD workflows.

---

## **How It Works**

1. **Retrieve the Latest Git Tag**:
   - Fetches the most recent Git tag or falls back to a base version.

2. **Compute the Version**:
   - Adjusts the version based on the branch:
     - `main`: Promotes RCs to stable releases or increments the patch version.
     - `develop`: Appends `.dev.<BUILD_NUMBER>` to the version.
     - Feature branches: Includes the branch name in the version.

3. **Output**:
   - Prints the computed version and writes it to the `GITHUB_ENV` file for use in workflows.

---

## **Usage**

Run the script with the following arguments:
1. **`base_version`**: Fallback version if no tags exist (e.g., `1.0.0`).
2. **`github_ref`**: The branch reference (e.g., `refs/heads/main`).
3. **`build_number`**: The CI/CD build number.

### **Example**
```bash
python versioning.py 1.0.0 refs/heads/develop 42
```

---

## **Examples of Computed Versions**

- **`main`**: `1.0.1` (stable release).
- **`develop`**: `1.0.0.dev.42`.
- **Feature branch**: `1.0.0.feature-name.42`.
- **Release candidate**: `1.0.0-rc1`.

---

## **Integration**

Use this script in CI/CD workflows to dynamically compute and export the version.

### **Example Workflow Step**
```yaml
- name: Compute Version
  run: |
    python .github/workflows/scripts/versioning.py 1.0.0 ${{ github.ref }} ${{ github.run_number }}
```

---

For questions or support, contact **Niels Weistra** at **n.weistra@itlusions.nl**.