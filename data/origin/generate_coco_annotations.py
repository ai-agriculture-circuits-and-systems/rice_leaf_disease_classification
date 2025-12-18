import os
import json
import random
import time
from PIL import Image
from pathlib import Path

def generate_unique_id():
    """Generate unique ID: 7 random digits + 3 timestamp digits"""
    random_part = random.randint(1000000, 9999999)
    timestamp_part = int(time.time() * 1000) % 1000
    return int(f"{random_part}{timestamp_part:03d}")

def get_image_info(image_path):
    """Get image dimensions and file info"""
    try:
        with Image.open(image_path) as img:
            width, height = img.size
        file_size = os.path.getsize(image_path)
        return width, height, file_size
    except Exception as e:
        print(f"Error reading image {image_path}: {e}")
        return 512, 512, 0

def create_coco_annotation(image_path, category_name, supercategory_name):
    """Create COCO format annotation for a single image"""
    
    # Get image info
    width, height, file_size = get_image_info(image_path)
    
    # Generate unique IDs
    image_id = generate_unique_id()
    annotation_id = generate_unique_id()
    category_id = generate_unique_id()
    
    # Create COCO format structure
    coco_data = {
        "info": {
            "description": "data",
            "version": "1.0",
            "year": 2025,
            "contributor": "search engine",
            "source": "augmented",
            "license": {
                "name": "Creative Commons Attribution 4.0 International",
                "url": "https://creativecommons.org/licenses/by/4.0/"
            }
        },
        "images": [
            {
                "id": image_id,
                "width": width,
                "height": height,
                "file_name": os.path.basename(image_path),
                "size": file_size,
                "format": "JPEG",
                "url": "",
                "hash": "",
                "status": "success"
            }
        ],
        "annotations": [
            {
                "id": annotation_id,
                "image_id": image_id,
                "category_id": category_id,
                "segmentation": [],
                "area": width * height,
                "bbox": [0, 0, width, height]
            }
        ],
        "categories": [
            {
                "id": category_id,
                "name": category_name,
                "supercategory": supercategory_name
            }
        ]
    }
    
    return coco_data

def process_dataset(root_dir):
    """Process all images in the dataset and create individual JSON files"""
    
    root_path = Path(root_dir)
    
    # Get all subdirectories (main categories)
    subdirs = [d for d in root_path.iterdir() if d.is_dir()]
    
    total_processed = 0
    
    for subdir in subdirs:
        supercategory_name = subdir.name
        category_name = subdir.name
        
        print(f"Processing directory: {supercategory_name}")
        
        # Get all image files in the subdirectory
        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff'}
        image_files = [f for f in subdir.iterdir() 
                      if f.is_file() and f.suffix.lower() in image_extensions]
        
        for image_file in image_files:
            try:
                # Create COCO annotation for this image
                coco_data = create_coco_annotation(
                    str(image_file), 
                    category_name, 
                    supercategory_name
                )
                
                # Create JSON filename (same name as image but with .json extension)
                json_filename = image_file.stem + '.json'
                json_path = image_file.parent / json_filename
                
                # Save JSON file
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(coco_data, f, indent=2, ensure_ascii=False)
                
                total_processed += 1
                print(f"  Created: {json_filename}")
                
            except Exception as e:
                print(f"Error processing {image_file}: {e}")
    
    print(f"\nTotal images processed: {total_processed}")

if __name__ == "__main__":
    # Process the current directory
    current_dir = "."
    process_dataset(current_dir) 