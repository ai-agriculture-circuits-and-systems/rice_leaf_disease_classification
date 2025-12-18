#!/usr/bin/env python3
"""
Reorganize existing data into standard directory structure.
"""

import os
import shutil
from pathlib import Path

# Mapping from old folder names to new category names
CATEGORY_MAPPING = {
    'Healthy Rice Leaf': 'healthy_rice_leaf',
    'Bacterial Leaf Blight': 'bacterial_leaf_blight',
    'Brown Spot': 'brown_spot',
    'Leaf Blast': 'leaf_blast',
    'Leaf scald': 'leaf_scald',
    'Sheath Blight': 'sheath_blight'
}

def reorganize_data(root_dir='.'):
    """Reorganize data from old structure to new standard structure"""
    root = Path(root_dir)
    rice_leaves_dir = root / 'rice_leaves'
    
    for old_folder, new_category in CATEGORY_MAPPING.items():
        old_path = root / old_folder
        if not old_path.exists():
            print(f"Warning: {old_path} does not exist, skipping")
            continue
        
        new_category_dir = rice_leaves_dir / new_category
        images_dir = new_category_dir / 'images'
        json_dir = new_category_dir / 'json'
        
        images_dir.mkdir(parents=True, exist_ok=True)
        json_dir.mkdir(parents=True, exist_ok=True)
        
        # Move images and JSON files
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
        moved_images = 0
        moved_jsons = 0
        
        for file_path in old_path.iterdir():
            if file_path.is_file():
                if file_path.suffix.lower() in image_extensions:
                    dest = images_dir / file_path.name
                    if not dest.exists():
                        shutil.copy2(file_path, dest)
                        moved_images += 1
                    else:
                        moved_images += 1  # Count as already moved
                elif file_path.suffix.lower() == '.json':
                    dest = json_dir / file_path.name
                    if not dest.exists():
                        shutil.copy2(file_path, dest)
                        moved_jsons += 1
                    else:
                        moved_jsons += 1  # Count as already moved
        
        print(f"{old_folder} -> {new_category}: {moved_images} images, {moved_jsons} JSON files")

if __name__ == '__main__':
    reorganize_data()

