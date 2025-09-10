#!/usr/bin/env python3

"""Simple usage example of tarko_web_ui SDK.

This example shows the basic usage of the SDK for getting
static asset paths and downloading assets.
"""

from tarko_web_ui import get_static_path, get_static_version


def main():
    """Demonstrate basic SDK usage."""
    print("🔧 Tarko Web UI SDK Example")
    print("=" * 30)
    
    # Get version information
    version_info = get_static_version()
    print(f"📦 Package: {version_info['package']}")
    print(f"🏷️  Static Assets Version: {version_info['version']}")
    print(f"🐍 SDK Version: {version_info['sdk_version']}")
    print()
    
    # Get static path
    try:
        static_path = get_static_path()
        print(f"✅ Static assets found at: {static_path}")
        
        # List some files
        from pathlib import Path
        static_dir = Path(static_path)
        all_files = list(static_dir.rglob("*"))
        sample_files = [f for f in all_files if f.is_file()][:10]
        
        print(f"📁 Found {len([f for f in all_files if f.is_file()])} files total")
        print("📄 Sample files:")
        for file in sample_files:
            print(f"   - {file.relative_to(static_dir)}")
                
    except FileNotFoundError as e:
        print(f"❌ {e}")
        print("💡 Run 'python scripts/build_assets.py' to build static assets")
        return
    
    print("\n🚀 Static assets are ready for use!")
    print("💡 Example integration:")
    print("   from fastapi.staticfiles import StaticFiles")
    print("   app.mount('/static', StaticFiles(directory=static_path))")


if __name__ == "__main__":
    main()
