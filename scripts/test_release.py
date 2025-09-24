#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Release testing script to verify published package functionality.

This script validates that the released package works correctly by:
1. Installing the package from PyPI in a clean environment
2. Running basic functionality tests
3. Starting a test server and verifying it works
4. Checking version consistency
"""

import json
import os
import subprocess
import sys
import tempfile
import time
import os
import requests
from typing import Union


def run_cmd(cmd, cwd=None, check=True, capture_output=True):
    """Run command with proper error handling."""
    print("🔧 {}".format(cmd))
    if cwd:
        print("   📁 in {}".format(cwd))

    # Use Popen for compatibility
    if capture_output:
        process = subprocess.Popen(
            cmd, shell=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate()

        # Convert bytes to string for Python 2/3 compatibility
        if hasattr(stdout, "decode"):
            stdout_str: str = stdout.decode("utf-8")  # type: ignore
            stderr_str: str = stderr.decode("utf-8")  # type: ignore
        else:
            stdout_str = str(stdout)
            stderr_str = str(stderr)

        # Create a simple result object
        class Result:
            def __init__(self, returncode: int, stdout: str, stderr: str):
                self.returncode = returncode
                self.stdout = stdout
                self.stderr = stderr

        result_obj: Union[Result, "SimpleResult"] = Result(
            process.returncode, stdout_str, stderr_str
        )
    else:
        call_result = subprocess.call(cmd, shell=True, cwd=cwd)

        class SimpleResult:
            def __init__(self, returncode: int):
                self.returncode = returncode
                self.stdout = ""
                self.stderr = ""

        result_obj = SimpleResult(call_result)

    if check and result_obj.returncode != 0:
        print("❌ Command failed: {}".format(cmd))
        if capture_output:
            print("stdout: {}".format(result_obj.stdout))
            print("stderr: {}".format(result_obj.stderr))
        sys.exit(1)

    return result_obj


def get_current_version():
    """Get current version from pyproject.toml."""
    if not os.path.exists("pyproject.toml"):
        raise FileNotFoundError("pyproject.toml not found")

    with open("pyproject.toml", "r") as f:
        content = f.read()
    import re

    match = re.search(r'version = "([^"]+)"', content)
    if not match:
        raise ValueError("Could not find version in pyproject.toml")

    return match.group(1)


def wait_for_pypi_availability(package_name, version, max_wait=300):
    """Wait for package to be available on PyPI.

    Args:
        package_name: Name of the package
        version: Version to check for
        max_wait: Maximum time to wait in seconds

    Returns:
        True if package is available, False if timeout
    """
    print(
        "⏳ Waiting for {}=={} to be available on PyPI...".format(package_name, version)
    )

    start_time = time.time()
    while time.time() - start_time < max_wait:
        try:
            url = "https://pypi.org/pypi/{}/{}/json".format(package_name, version)
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(
                    "✅ Package {}=={} is available on PyPI".format(
                        package_name, version
                    )
                )
                return True
        except requests.RequestException:
            pass

        print("   ⏳ Still waiting... ({}s)".format(int(time.time() - start_time)))
        time.sleep(10)

    print("❌ Timeout waiting for package on PyPI after {}s".format(max_wait))
    return False


def create_test_environment():
    """Create a clean test environment."""
    print("🏗️  Creating clean test environment...")

    test_dir = tempfile.mkdtemp(prefix="tarko_release_test_")
    print("📁 Test directory: {}".format(test_dir))

    # Create a simple Python environment
    run_cmd("python -m venv test_env", cwd=test_dir)

    return test_dir


def get_pip_path(test_dir):
    """Get pip executable path for the test environment."""
    if sys.platform == "win32":
        return os.path.join(test_dir, "test_env", "Scripts", "pip")
    else:
        return os.path.join(test_dir, "test_env", "bin", "pip")


def get_python_path(test_dir):
    """Get python executable path for the test environment."""
    if sys.platform == "win32":
        return os.path.join(test_dir, "test_env", "Scripts", "python")
    else:
        return os.path.join(test_dir, "test_env", "bin", "python")


def install_package(test_dir, package_name, version):
    """Install package in test environment."""
    print("📦 Installing {}=={} in test environment...".format(package_name, version))

    pip_path = get_pip_path(test_dir)

    # Upgrade pip first
    run_cmd("{} install --upgrade pip".format(pip_path), cwd=test_dir)

    # Install the package
    run_cmd("{} install {}=={}".format(pip_path, package_name, version), cwd=test_dir)

    # Install additional dependencies for testing
    run_cmd("{} install fastapi uvicorn requests".format(pip_path), cwd=test_dir)

    print("✅ Installed {}=={}".format(package_name, version))


def create_test_script(test_dir):
    """Create a test script to validate package functionality."""
    test_script_content = '''
#!/usr/bin/env python3
"""Test script to validate tarko-agent-ui package functionality."""

import sys
import os
import json
from pathlib import Path

def test_imports():
    """Test that all imports work correctly."""
    print("🧪 Testing imports...")
    try:
        import tarko_agent_ui
        from tarko_agent_ui import get_static_path, get_static_version, get_agent_ui_html
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print("❌ Import failed: {}".format(e))
        return False

def test_version_info():
    """Test version information."""
    print("🧪 Testing version info...")
    try:
        import tarko_agent_ui
        version_info = tarko_agent_ui.get_static_version()
        print("📦 Package version: {}".format(tarko_agent_ui.__version__))
        print("📦 npm version: {}".format(tarko_agent_ui.__npm_version__))
        print("📦 Static assets: {}".format(version_info))
        return True
    except Exception as e:
        print("❌ Version info failed: {}".format(e))
        return False

def test_static_assets():
    """Test static assets functionality."""
    print("🧪 Testing static assets...")
    try:
        from tarko_agent_ui import get_static_path
        static_path = get_static_path()
        print("📁 Static path: {}".format(static_path))
        
        # Check if index.html exists
        index_file = os.path.join(static_path, "index.html")
        if not os.path.exists(index_file):
            print("❌ index.html not found at {}".format(index_file))
            return False
        
        print("✅ index.html found at {}".format(index_file))
        print("📏 File size: {} bytes".format(os.path.getsize(index_file)))
        return True
    except Exception as e:
        print("❌ Static assets test failed: {}".format(e))
        return False

def test_html_generation():
    """Test HTML generation with environment injection."""
    print("🧪 Testing HTML generation...")
    try:
        from tarko_agent_ui import get_agent_ui_html
        
        # Test HTML generation with environment injection.
        html_content = get_agent_ui_html(
            api_base_url="http://localhost:8000/api",
            ui_config={"title": "Test App", "test": True}
        )
        
        if not html_content or len(html_content) < 100:
            print("❌ HTML content too short: {} chars".format(len(html_content)))
            return False
        
        # Check if environment variables are injected
        if "window.AGENT_BASE_URL" not in html_content:
            print("❌ AGENT_BASE_URL not injected")
            return False
        
        if "window.AGENT_WEB_UI_CONFIG" not in html_content:
            print("❌ AGENT_WEB_UI_CONFIG not injected")
            return False
        
        print("✅ HTML generated successfully ({} chars)".format(len(html_content)))
        return True
    except Exception as e:
        print("❌ HTML generation failed: {}".format(e))
        return False

def main():
    """Run all tests."""
    print("🚀 Starting tarko-agent-ui functionality tests...")
    
    tests = [
        test_imports,
        test_version_info,
        test_static_assets,
        test_html_generation,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                print("❌ Test {} failed".format(test.__name__))
        except Exception as e:
            print("❌ Test {} crashed: {}".format(test.__name__, e))
        print()  # Empty line for readability
    
    print("📊 Test Results: {}/{} passed".format(passed, total))
    
    if passed == total:
        print("🎉 All tests passed!")
        sys.exit(0)
    else:
        print("❌ Some tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
'''

    test_script_path = os.path.join(test_dir, "test_functionality.py")
    with open(test_script_path, "w") as f:
        f.write(test_script_content)

    return test_script_path


def create_server_test_script(test_dir):
    """Create a script to test the FastAPI server."""
    server_script_content = '''
#!/usr/bin/env python3
"""Test script to validate FastAPI server functionality."""

import sys
import time
import threading
import requests
from pathlib import Path

def test_server():
    """Test that the server starts and responds correctly."""
    print("🧪 Testing FastAPI server...")
    
    try:
        from fastapi import FastAPI
        from fastapi.responses import HTMLResponse
        from fastapi.staticfiles import StaticFiles
        import uvicorn
        from tarko_agent_ui import get_agent_ui_html, get_static_path
        
        # Create a simple test app
        app = FastAPI(title="Test App")
        
        @app.get("/", response_class=HTMLResponse)
        async def root():
            return HTMLResponse(
                content=get_agent_ui_html(
                    api_base_url="http://localhost:8001/api",
                    ui_config={"title": "Test Release"}
                )
            )
        
        @app.get("/health")
        async def health():
            return {"status": "ok", "message": "Server is running"}
        
        # Mount static files
        try:
            static_path = get_static_path()
            app.mount("/static", StaticFiles(directory=static_path), name="static")
            print("✅ Static files mounted from {}".format(static_path))
        except Exception as e:
            print("⚠️  Could not mount static files: {}".format(e))
        
        # Start server in a thread
        def run_server():
            uvicorn.run(app, host="127.0.0.1", port=8001, log_level="error")
        
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        
        # Wait for server to start
        print("⏳ Waiting for server to start...")
        time.sleep(3)
        
        # Test health endpoint
        try:
            response = requests.get("http://127.0.0.1:8001/health", timeout=5)
            if response.status_code == 200:
                print("✅ Health endpoint works")
            else:
                print("❌ Health endpoint returned {}".format(response.status_code))
                return False
        except Exception as e:
            print("❌ Health endpoint failed: {}".format(e))
            return False
        
        # Test main UI endpoint
        try:
            response = requests.get("http://127.0.0.1:8001/", timeout=10)
            if response.status_code == 200:
                content = response.text
                if "window.AGENT_BASE_URL" in content and len(content) > 1000:
                    print("✅ Main UI endpoint works ({} chars)".format(len(content)))
                else:
                    print("❌ Main UI content invalid (length: {})".format(len(content)))
                    return False
            else:
                print("❌ Main UI endpoint returned {}".format(response.status_code))
                return False
        except Exception as e:
            print("❌ Main UI endpoint failed: {}".format(e))
            return False
        
        print("🎉 Server test completed successfully!")
        return True
        
    except Exception as e:
        print("❌ Server test failed: {}".format(e))
        return False

def main():
    """Run server tests."""
    print("🚀 Starting FastAPI server tests...")
    
    if test_server():
        print("🎉 All server tests passed!")
        sys.exit(0)
    else:
        print("❌ Server tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
'''

    server_script_path = os.path.join(test_dir, "test_server.py")
    with open(server_script_path, "w") as f:
        f.write(server_script_content)

    return server_script_path


def run_functionality_tests(test_dir, test_script_path):
    """Run functionality tests in the test environment."""
    print("🧪 Running functionality tests...")

    python_path = get_python_path(test_dir)
    result = run_cmd(
        "{} {}".format(python_path, test_script_path), cwd=test_dir, check=False
    )

    return result.returncode == 0


def run_server_tests(test_dir, server_script_path):
    """Run server tests in the test environment."""
    print("🧪 Running server tests...")

    python_path = get_python_path(test_dir)
    result = run_cmd(
        "{} {}".format(python_path, server_script_path), cwd=test_dir, check=False
    )

    return result.returncode == 0


def cleanup_test_environment(test_dir):
    """Clean up test environment."""
    print("🧹 Cleaning up test environment: {}".format(test_dir))
    try:
        import shutil

        shutil.rmtree(test_dir)
        print("✅ Test environment cleaned up")
    except Exception as e:
        print("⚠️  Could not clean up test environment: {}".format(e))


def main():
    """Main test workflow."""
    import argparse

    parser = argparse.ArgumentParser(description="Test released package functionality")
    parser.add_argument("--version", help="Specific version to test (default: current)")
    parser.add_argument(
        "--package-name", default="tarko-agent-ui", help="Package name to test"
    )
    parser.add_argument(
        "--skip-wait", action="store_true", help="Skip waiting for PyPI availability"
    )
    parser.add_argument(
        "--keep-env", action="store_true", help="Keep test environment after testing"
    )
    parser.add_argument(
        "--quick", action="store_true", help="Skip server tests (faster)"
    )

    args = parser.parse_args()

    try:
        # Determine version to test
        version = args.version or get_current_version()
        print("🎯 Testing {}=={}".format(args.package_name, version))

        # Wait for package availability on PyPI (unless skipped)
        if not args.skip_wait:
            if not wait_for_pypi_availability(args.package_name, version):
                print("❌ Package not available on PyPI")
                sys.exit(1)

        # Create test environment
        test_dir = create_test_environment()

        try:
            # Install package
            install_package(test_dir, args.package_name, version)

            # Create test scripts
            test_script_path = create_test_script(test_dir)
            server_script_path = create_server_test_script(test_dir)

            # Run functionality tests
            functionality_passed = run_functionality_tests(test_dir, test_script_path)

            # Run server tests (unless quick mode)
            server_passed = True
            if not args.quick:
                server_passed = run_server_tests(test_dir, server_script_path)
            else:
                print("⏩ Skipping server tests (quick mode)")

            # Report results
            print("\n" + "=" * 50)
            print("📊 RELEASE TEST RESULTS")
            print("=" * 50)
            print("📦 Package: {}=={}".format(args.package_name, version))
            print(
                "🧪 Functionality tests: {}".format(
                    "✅ PASSED" if functionality_passed else "❌ FAILED"
                )
            )

            if not args.quick:
                print(
                    "🌐 Server tests: {}".format(
                        "✅ PASSED" if server_passed else "❌ FAILED"
                    )
                )

            if functionality_passed and server_passed:
                print("\n🎉 ALL TESTS PASSED! Release is ready for use.")
                exit_code = 0
            else:
                print("\n❌ SOME TESTS FAILED! Please investigate.")
                exit_code = 1

        finally:
            # Clean up test environment (unless keeping)
            if not args.keep_env:
                cleanup_test_environment(test_dir)
            else:
                print("🔒 Keeping test environment: {}".format(test_dir))

        sys.exit(exit_code)

    except KeyboardInterrupt:
        print("\n❌ Testing interrupted by user")
        sys.exit(1)
    except Exception as e:
        print("\n❌ Testing failed: {}".format(e))
        sys.exit(1)


if __name__ == "__main__":
    main()
