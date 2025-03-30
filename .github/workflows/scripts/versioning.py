import os
import re
import sys
from git import Repo, GitCommandError

def get_last_tag():
    try:
        repo = Repo(".")
        tags = sorted(repo.tags, key=lambda t: t.commit.committed_datetime, reverse=True)
        return str(tags[0]) if tags else ""
    except GitCommandError:
        return ""

def compute_version(base_version, github_ref, build_number):
    last_tag = get_last_tag() or base_version
    major, minor, patch = map(int, re.match(r"(\d+)\.(\d+)\.(\d+)", last_tag).groups())
    is_rc = re.search(r"rc\d+", last_tag)

    if "refs/heads/develop" in github_ref:
        if is_rc:
            return f"{major}.{minor}.{patch}.dev.{build_number}"
        else:
            patch += 1
            return f"{major}.{minor}.{patch}.dev.{build_number}"
    elif "refs/heads/main" in github_ref:
        if is_rc:
            return f"{major}.{minor}.{patch}"
        else:
            patch += 1
            return f"{major}.{minor}.{patch}"
    elif "refs/heads/feature/" in github_ref:
        branch_name = github_ref.split("/")[-1]
        return f"{major}.{minor}.{patch}.{branch_name}.{build_number}"
    else:
        return f"{major}.{minor}.{patch}.{build_number}"

if __name__ == "__main__":
    base_version = sys.argv[1]
    github_ref = sys.argv[2]
    build_number = sys.argv[3]

    full_version = compute_version(base_version, github_ref, build_number)
    print(f"Computed version: {full_version}")
    with open(os.getenv("GITHUB_ENV"), "a") as env_file:
        env_file.write(f"PACKAGE_VERSION={full_version}\n")
