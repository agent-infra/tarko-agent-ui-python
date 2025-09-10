#!/usr/bin/env python3

import os
import subprocess
import sys
from setuptools import setup, find_packages
from setuptools.command.install import install


class PostInstallCommand(install):
    """Custom post-installation command to download and extract npm package."""
    
    def run(self):
        install.run(self)
        self.download_npm_package()
    
    def download_npm_package(self):
        """Download and extract @tarko/agent-ui-builder npm package."""
        import tempfile
        import tarfile
        import shutil
        import json
        from urllib.request import urlopen
        from urllib.parse import urljoin
        
        package_name = "@tarko/agent-ui-builder"
        
        try:
            # Get package info from npm registry
            registry_url = f"https://registry.npmjs.org/{package_name.replace('@', '%40')}"
            with urlopen(registry_url) as response:
                package_info = json.loads(response.read().decode())
            
            # Get latest version tarball URL
            latest_version = package_info["dist-tags"]["latest"]
            tarball_url = package_info["versions"][latest_version]["dist"]["tarball"]
            
            # Create static directory in package
            package_dir = os.path.dirname(__file__)
            static_dir = os.path.join(package_dir, "agent_sandbox", "static")
            os.makedirs(static_dir, exist_ok=True)
            
            # Download and extract tarball
            with tempfile.NamedTemporaryFile(suffix=".tgz") as tmp_file:
                with urlopen(tarball_url) as response:
                    shutil.copyfileobj(response, tmp_file)
                tmp_file.flush()
                
                # Extract static files
                with tarfile.open(tmp_file.name, "r:gz") as tar:
                    for member in tar.getmembers():
                        if member.name.startswith("package/static/"):
                            # Remove 'package/' prefix
                            member.name = member.name[8:]  # len("package/") = 8
                            if member.name:  # Skip empty names
                                tar.extract(member, static_dir)
            
            print(f"Successfully downloaded {package_name} static assets to {static_dir}")
            
        except Exception as e:
            print(f"Warning: Failed to download npm package: {e}", file=sys.stderr)
            print("You can manually download the package later using: python -c 'from agent_sandbox import download_static_assets; download_static_assets()'", file=sys.stderr)


setup(
    name="agent-sandbox",
    version="0.1.0",
    description="Python SDK for serving Tarko Agent UI Builder static assets",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.68.0",
        "uvicorn[standard]>=0.15.0",
    ],
    cmdclass={
        "install": PostInstallCommand,
    },
    python_requires=">=3.7",
    author="Tarko Team",
    author_email="team@tarko.ai",
    url="https://github.com/agent-infra/tarko-agent-ui-fastapi-example",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
