
import os
import zipfile
import shutil
from datetime import datetime

def pack_project():
    """
    Creates a deployment zip package of the current project directory.
    """
    root_dir = os.path.dirname(os.path.abspath(__file__))
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"autovideo_deploy_{timestamp}.zip"
    zip_path = os.path.join(root_dir, zip_filename)
    
    print(f"📦 Packaging project: {root_dir}")
    print(f"📍 Output file: {zip_filename}")
    
    # Exclude directories
    EXCLUDE_DIRS = {
        "__pycache__", 
        "venv", 
        ".git", 
        ".idea", 
        ".vscode", 
        "media",      # Manim temp files
        "output",     # Previous outputs
        ".gemini",    # Agent temp files
    }
    
    # Exclude specific files
    EXCLUDE_FILES = {
        zip_filename,
        ".DS_Store",
        "Thumbs.db",
        "project_packer.py",
        ".api_call_count.json"
    }
    
    file_count = 0
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(root_dir):
            if any(part in EXCLUDE_DIRS for part in root.split(os.sep)):
                # If path contains excluded directory, skip
                continue

            # Modify usage of dirs in-place to avoid recursion into excluded ones
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            
            for file in files:
                if file in EXCLUDE_FILES:
                    continue
                
                # Filter by extension
                if file.endswith(".log") or file.endswith(".zip"):
                    continue

                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, root_dir)
                
                zipf.write(abs_path, rel_path)
                file_count += 1
                if file_count % 100 == 0:
                    print(f"  Processed {file_count} files...", end="\r")

    size_mb = os.path.getsize(zip_path) / (1024 * 1024)
    print(f"\n✅ Created: {zip_filename} ({file_count} files, {size_mb:.2f} MB)")
    print("\n[Next Steps]")
    print(f"1. Upload '{zip_filename}' to your cloud server.")
    print("2. Unzip it: unzip autovideo_deploy_....zip -d autovideo")
    print("3. Run: cd autovideo && chmod +x setup_linux.sh && ./setup_linux.sh")

if __name__ == "__main__":
    pack_project()
