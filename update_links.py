#!/usr/bin/env python
"""
Update the symbolic link pointing to the latest version.

"""
import os
import packaging.version
import pathlib


if __name__ == "__main__":

    # A version directory is any directory starting with a "v"
    root_dir = pathlib.Path(".")
    all_versions = (packaging.version.parse(d.name)
                    for d in root_dir.iterdir()
                    if d.is_dir() and d.name.startswith("v"))

    # Make a symlink to the latest version
    latest_version = sorted(all_versions)[-1]
    major, minor, *_ = latest_version.release
    os.remove("latest")
    os.symlink(f"v{major}.{minor}", "latest")
