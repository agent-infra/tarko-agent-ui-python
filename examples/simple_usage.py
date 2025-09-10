#!/usr/bin/env python3

"""Simple usage example of tarko_web_ui SDK.

This example shows the basic usage of the SDK for getting
static asset paths and downloading assets.
"""

from tarko_web_ui import get_static_path, download_static_assets


def main():
    """Demonstrate basic SDK usage."""
    print("🔧 Tarko Web UI SDK Example")
    print("=" * 30)
    
    # Try to get static path
    try:
        static_path = get_static_path()
        print(f"✅ Static assets found at: {static_path}")
        
        # List some files
        from pathlib import Path
        static_dir = Path(static_path)
        files = list(static_dir.rglob("*"))[:10]  # First 10 files
        
        print(f"📁 Found {len(list(static_dir.rglob('*')))} files total")
        print("📄 Sample files:")
        for file in files:
            if file.is_file():
                print(f"   - {file.relative_to(static_dir)}")
                
    except FileNotFoundError:
        print("❌ Static assets not found")
        print("⬇️  Downloading static assets...")
        
        try:
            download_static_assets()
            print("✅ Assets downloaded successfully!")
            
            # Now try again
            static_path = get_static_path()
            print(f"📁 Static assets now available at: {static_path}")
            
        except Exception as e:
            print(f"❌ Failed to download assets: {e}")
            return
    
    print("\n🚀 You can now use the static path in your application!")
    print("💡 Example integration:")
    print("   from fastapi.staticfiles import StaticFiles")
    print("   app.mount('/static', StaticFiles(directory=static_path))")


if __name__ == "__main__":
    main()
