#!/usr/bin/env python3
"""
Convert JSON annotations (per-image) to COCO format for Rice Leaf Disease Classification dataset.
"""

import os
import json
import argparse
from pathlib import Path
from PIL import Image
import random

def load_labelmap(labelmap_path):
    """Load labelmap.json"""
    with open(labelmap_path, 'r', encoding='utf-8') as f:
        labelmap = json.load(f)
    return {item['object_id']: item['object_name'] for item in labelmap}

def parse_json_annotation(json_path):
    """Parse per-image JSON annotation file"""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"Error parsing {json_path}: {e}")
        return None

def get_image_info(image_path):
    """Get image dimensions"""
    try:
        with Image.open(image_path) as img:
            return img.size
    except Exception:
        return (512, 512)  # Default

def convert_to_coco(root_dir, output_dir, categories=None, splits=None, combined=False):
    """Convert JSON annotations (per-image) to COCO format"""
    root = Path(root_dir)
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    
    if categories is None:
        categories = ['healthy_rice_leaf', 'bacterial_leaf_blight', 'brown_spot', 
                     'leaf_blast', 'leaf_scald', 'sheath_blight']
    if splits is None:
        splits = ['train', 'val', 'test']
    
    # Load labelmap
    labelmap_path = root / 'rice_leaves' / 'labelmap.json'
    labelmap = load_labelmap(labelmap_path)
    
    # Build category list from labelmap
    coco_categories = []
    for obj_id, obj_name in sorted(labelmap.items()):
        if obj_id == 0:
            coco_categories.append({
                'id': 0,
                'name': 'background',
                'supercategory': 'background'
            })
        else:
            coco_categories.append({
                'id': obj_id,
                'name': obj_name,
                'supercategory': 'rice_leaf'
            })
    
    # Create category name mapping (from folder names to labelmap names)
    category_mapping = {
        'Healthy Rice Leaf': 'healthy_rice_leaf',
        'Bacterial Leaf Blight': 'bacterial_leaf_blight',
        'Brown Spot': 'brown_spot',
        'Leaf Blast': 'leaf_blast',
        'Leaf scald': 'leaf_scald',
        'Sheath Blight': 'sheath_blight'
    }
    
    # Process each category and split
    all_coco_data = {}
    
    for category_folder, category_name in category_mapping.items():
        if category_name not in categories:
            continue
            
        category_dir = root / 'rice_leaves' / category_name
        images_dir = category_dir / 'images'
        json_dir = category_dir / 'json'
        sets_dir = category_dir / 'sets'  # Split files are in each subcategory's sets/ directory
        
        if not images_dir.exists():
            print(f"Warning: {images_dir} does not exist, skipping {category_name}")
            continue
        
        for split in splits:
            coco_data = {
                'info': {
                    'year': 2025,
                    'version': '1.0',
                    'description': f'Rice Leaf Disease Classification {category_name} {split} split',
                    'url': ''
                },
                'images': [],
                'annotations': [],
                'categories': coco_categories,
                'licenses': []
            }
            
            # Load split file
            split_file = sets_dir / f'{split}.txt'
            split_images = set()
            if split_file.exists():
                with open(split_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            # Split file format: just image_stem (no category prefix)
                            split_images.add(line)
                print(f"Loaded {len(split_images)} images for {category_name}/{split}")
            else:
                print(f"Warning: Split file '{split_file}' does not exist, using all images")
            
            # Get images in this split
            if split_images:
                image_files = []
                for stem in split_images:
                    for ext in ['.jpg', '.png', '.jpeg', '.bmp']:
                        img_path = images_dir / f"{stem}{ext}"
                        if img_path.exists():
                            image_files.append(img_path)
                            break
                print(f"  Found {len(image_files)}/{len(split_images)} images for {category_name}/{split}")
            else:
                # If split file doesn't exist, use all images
                image_files = list(images_dir.glob('*.jpg'))
                image_files.extend(images_dir.glob('*.png'))
                image_files.extend(images_dir.glob('*.jpeg'))
                image_files.extend(images_dir.glob('*.bmp'))
                print(f"  No split file for {category_name}/{split}, using all {len(image_files)} images")
            
            # Process images
            image_id_map = {}
            annotation_id = 1
            
            for img_path in image_files:
                stem = img_path.stem
                
                # Check if in split (already filtered above, but double-check)
                if split_images and stem not in split_images:
                    continue
                
                # Get image info
                width, height = get_image_info(img_path)
                image_id = random.randint(1000000000, 9999999999)
                image_id_map[stem] = image_id
                
                coco_data['images'].append({
                    'id': image_id,
                    'file_name': f'rice_leaves/{category_name}/images/{img_path.name}',
                    'width': width,
                    'height': height
                })
                
                # Load JSON annotations
                json_path = json_dir / f'{stem}.json'
                if json_path.exists():
                    json_data = parse_json_annotation(json_path)
                    if json_data and 'annotations' in json_data:
                        for ann in json_data['annotations']:
                            # Map category_id from JSON to labelmap
                            json_category_id = ann.get('category_id', 1)
                            # Find matching category in labelmap
                            category_id = 1  # Default
                            for obj_id, obj_name in labelmap.items():
                                if obj_id == json_category_id or obj_name == category_name:
                                    category_id = obj_id
                                    break
                            
                            bbox = ann.get('bbox', [0, 0, width, height])
                            
                            coco_data['annotations'].append({
                                'id': annotation_id,
                                'image_id': image_id,
                                'category_id': category_id,
                                'bbox': bbox,
                                'area': ann.get('area', bbox[2] * bbox[3]),
                                'iscrowd': 0
                            })
                            annotation_id += 1
            
            # Save single category file
            output_file = output / f'{category_name}_instances_{split}.json'
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(coco_data, f, indent=2, ensure_ascii=False)
            print(f"Created {output_file}: {len(coco_data['images'])} images, {len(coco_data['annotations'])} annotations")
            
            if split not in all_coco_data:
                all_coco_data[split] = {
                    'info': {
                        'year': 2025,
                        'version': '1.0',
                        'description': f'Rice Leaf Disease Classification combined {split} split',
                        'url': ''
                    },
                    'images': [],
                    'annotations': [],
                    'categories': coco_categories,
                    'licenses': []
                }
            
            # Add to combined data
            all_coco_data[split]['images'].extend(coco_data['images'])
            all_coco_data[split]['annotations'].extend(coco_data['annotations'])
    
    # Create combined files if requested
    if combined:
        for split in splits:
            if split in all_coco_data:
                output_file = output / f'combined_instances_{split}.json'
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(all_coco_data[split], f, indent=2, ensure_ascii=False)
                print(f"Created {output_file}: {len(all_coco_data[split]['images'])} images, {len(all_coco_data[split]['annotations'])} annotations")

def main():
    parser = argparse.ArgumentParser(description='Convert JSON annotations to COCO format')
    parser.add_argument('--root', type=str, default='.', help='Dataset root directory')
    parser.add_argument('--out', type=str, default='annotations', help='Output directory')
    parser.add_argument('--categories', nargs='+', 
                        default=['healthy_rice_leaf', 'bacterial_leaf_blight', 'brown_spot', 
                                'leaf_blast', 'leaf_scald', 'sheath_blight'],
                        help='Categories to process')
    parser.add_argument('--splits', nargs='+', default=['train', 'val', 'test'], help='Splits to process')
    parser.add_argument('--combined', action='store_true', help='Create combined COCO files')
    
    args = parser.parse_args()
    convert_to_coco(args.root, args.out, args.categories, args.splits, args.combined)

if __name__ == '__main__':
    main()

