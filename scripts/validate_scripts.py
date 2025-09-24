#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Validation script to check if release scripts are working correctly.

This script performs basic validation of the release and test scripts
without actually performing a release.
"""

import sys
import subprocess
import os


def run_cmd(cmd, check=True):
    """Run command with proper error handling."""
    print("🔧 {}".format(cmd))

    # Use Popen for compatibility with older Python versions
    process = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()

    # Convert bytes to string for Python 2/3 compatibility
    if hasattr(stdout, "decode"):
        stdout = stdout.decode("utf-8")
        stderr = stderr.decode("utf-8")

    # Create a simple result object
    class Result:
        def __init__(self, returncode, stdout, stderr):
            self.returncode = returncode
            self.stdout = stdout
            self.stderr = stderr

    result = Result(process.returncode, stdout, stderr)

    if check and result.returncode != 0:
        print("❌ Command failed: {}".format(cmd))
        print("stdout: {}".format(result.stdout))
        print("stderr: {}".format(result.stderr))
        return result

    return result


def check_file_exists(filepath):
    """Check if file exists and is readable."""
    if not os.path.exists(filepath):
        print("❌ File not found: {}".format(filepath))
        return False

    if not os.path.isfile(filepath):
        print("❌ Not a file: {}".format(filepath))
        return False

    print("✅ File exists: {}".format(filepath))
    return True


def check_script_syntax(script_path):
    """Check if Python script has valid syntax."""
    print("🧪 Checking syntax: {}".format(script_path))
    result = run_cmd("python -m py_compile {}".format(script_path), check=False)

    if result.returncode == 0:
        print("✅ Syntax OK: {}".format(script_path))
        return True
    else:
        print("❌ Syntax error in {}:".format(script_path))
        print(result.stderr)
        return False


def check_script_help(script_path):
    """Check if script can show help without errors."""
    print("🧪 Testing help: {}".format(script_path))
    result = run_cmd("python {} --help".format(script_path), check=False)

    if result.returncode == 0 and "usage:" in result.stdout.lower():
        print("✅ Help works: {}".format(script_path))
        return True
    else:
        print("❌ Help failed for {}".format(script_path))
        if result.stdout:
            print("stdout: {}...".format(result.stdout[:200]))
        if result.stderr:
            print("stderr: {}...".format(result.stderr[:200]))
        return False


def check_dependencies():
    """Check if required dependencies are available."""
    print("🧪 Checking dependencies...")

    dependencies = [
        ("python", "python --version"),
        ("git", "git --version"),
        ("uv", "uv --version"),
    ]

    all_ok = True
    for name, cmd in dependencies:
        result = run_cmd(cmd, check=False)
        if result.returncode == 0:
            version = result.stdout.strip().split("\n")[0]
            print("✅ {}: {}".format(name, version))
        else:
            print("❌ {}: not found or not working".format(name))
            all_ok = False

    # Check Python packages
    python_packages = ["requests"]
    for package in python_packages:
        result = run_cmd(
            "python -c 'import {}; print(\"{} imported successfully\")'".format(
                package, package
            ),
            check=False,
        )
        if result.returncode == 0:
            print("✅ Python package: {}".format(package))
        else:
            print("❌ Python package missing: {}".format(package))
            all_ok = False

    return all_ok


def check_project_structure():
    """Check if project has the expected structure."""
    print("🧪 Checking project structure...")

    required_files = [
        "pyproject.toml",
        "tarko_agent_ui/__init__.py",
        "scripts/build_assets.py",
        "examples/fastapi_server.py",
    ]

    all_ok = True
    for filepath in required_files:
        if not check_file_exists(filepath):
            all_ok = False

    return all_ok


def check_version_consistency():
    """Check if version info can be read correctly."""
    print("🧪 Checking version consistency...")

    try:
        # Check pyproject.toml version
        with open("pyproject.toml", "r") as f:
            pyproject_content = f.read()

        import re

        version_match = re.search(r'version = "([^"]+)"', pyproject_content)
        if not version_match:
            print("❌ Could not find version in pyproject.toml")
            return False

        pyproject_version = version_match.group(1)
        print("✅ pyproject.toml version: {}".format(pyproject_version))

        # Check __init__.py version
        with open("tarko_agent_ui/__init__.py", "r") as f:
            init_content = f.read()

        version_match = re.search(r'__version__ = "([^"]+)"', init_content)
        if not version_match:
            print("❌ Could not find __version__ in __init__.py")
            return False

        init_version = version_match.group(1)
        print("✅ __init__.py version: {}".format(init_version))

        # Check npm version
        npm_match = re.search(r'__npm_version__ = "([^"]+)"', init_content)
        if not npm_match:
            print("❌ Could not find __npm_version__ in __init__.py")
            return False

        npm_version = npm_match.group(1)
        print("✅ npm version: {}".format(npm_version))

        # Check version consistency
        if pyproject_version != init_version:
            print(
                "⚠️  Version mismatch: pyproject.toml={}, __init__.py={}".format(
                    pyproject_version, init_version
                )
            )
            return False

        print("✅ Version consistency check passed")
        return True

    except Exception as e:
        print("❌ Version check failed: {}".format(e))
        return False


def test_dry_run():
    """Test auto_release.py in dry-run mode."""
    print("🧪 Testing auto_release.py dry-run...")

    # This should not make any changes
    result = run_cmd(
        "python scripts/auto_release.py --dry-run --npm-version '0.3.0-beta.12'",
        check=False,
    )

    if result.returncode == 0:
        if "DRY RUN" in result.stdout and "No changes will be made" in result.stdout:
            print("✅ Dry-run test passed")
            return True
        else:
            print("❌ Dry-run output unexpected")
            print("stdout: {}...".format(result.stdout[:500]))
            return False
    else:
        print("❌ Dry-run test failed")
        print("stderr: {}...".format(result.stderr[:500]))
        return False


def main():
    """Run all validation checks."""
    print("🚀 Validating release scripts...\n")

    checks = [
        ("Project Structure", check_project_structure),
        ("Dependencies", check_dependencies),
        ("Version Consistency", check_version_consistency),
        (
            "auto_release.py Syntax",
            lambda: check_script_syntax("scripts/auto_release.py"),
        ),
        (
            "test_release.py Syntax",
            lambda: check_script_syntax("scripts/test_release.py"),
        ),
        ("auto_release.py Help", lambda: check_script_help("scripts/auto_release.py")),
        ("test_release.py Help", lambda: check_script_help("scripts/test_release.py")),
        ("Dry-run Test", test_dry_run),
    ]

    passed = 0
    total = len(checks)

    for name, check_func in checks:
        print("\n" + "=" * 50)
        print("📋 {}".format(name))
        print("=" * 50)

        try:
            if check_func():
                passed += 1
                print("✅ {}: PASSED".format(name))
            else:
                print("❌ {}: FAILED".format(name))
        except Exception as e:
            print("❌ {}: ERROR - {}".format(name, e))

    print("\n" + "=" * 50)
    print("📊 VALIDATION RESULTS")
    print("=" * 50)
    print("Passed: {}/{}".format(passed, total))

    if passed == total:
        print("\n🎉 All validation checks passed!")
        print("✅ Release scripts are ready to use.")
        print("\n💡 Next steps:")
        print("   1. Run: python scripts/auto_release.py --dry-run")
        print("   2. Run: python scripts/auto_release.py")
        print("   3. Run: python scripts/test_release.py")
        sys.exit(0)
    else:
        print("\n❌ {} validation checks failed!".format(total - passed))
        print("🔧 Please fix the issues above before using the release scripts.")
        sys.exit(1)


if __name__ == "__main__":
    main()
