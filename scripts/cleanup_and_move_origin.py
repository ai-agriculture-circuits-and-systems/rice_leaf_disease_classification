#!/usr/bin/env python3
"""
Clean up original data: delete JSON files and move original data to data/origin.
"""

import os
import shutil
from pathlib import Path

# Original folder names
ORIGINAL_FOLDERS = [
    'Healthy Rice Leaf',
    'Bacterial Leaf Blight',
    'Brown Spot',
    'Leaf Blast',
    'Leaf scald',
    'Sheath Blight'
]

def cleanup_and_move_origin(root_dir='.'):
    """Delete JSON files from original folders and move folders to data/origin"""
    root = Path(root_dir)
    origin_dir = root / 'data' / 'origin'
    origin_dir.mkdir(parents=True, exist_ok=True)
    
    total_json_deleted = 0
    total_folders_moved = 0
    
    for folder_name in ORIGINAL_FOLDERS:
        folder_path = root / folder_name
        
        if not folder_path.exists():
            print(f"Warning: {folder_path} does not exist, skipping")
            continue
        
        # Count and delete JSON files
        json_files = list(folder_path.glob('*.json'))
        json_count = len(json_files)
        
        for json_file in json_files:
            json_file.unlink()
            total_json_deleted += 1
        
        print(f"{folder_name}: Deleted {json_count} JSON files")
        
        # Move folder to data/origin
        dest_path = origin_dir / folder_name
        if dest_path.exists():
            print(f"Warning: {dest_path} already exists, skipping move")
        else:
            shutil.move(str(folder_path), str(dest_path))
            print(f"  Moved {folder_name} -> data/origin/{folder_name}")
            total_folders_moved += 1
    
    print(f"\nSummary:")
    print(f"  JSON files deleted: {total_json_deleted}")
    print(f"  Folders moved: {total_folders_moved}")
    print(f"  Original data location: {origin_dir}")

if __name__ == '__main__':
    cleanup_and_move_origin()





