#!/usr/bin/env python3
"""
Convert JSON annotations (per-image) to CSV format for Rice Leaf Disease Classification dataset.
"""

import os
import json
import csv
from pathlib import Path

def load_labelmap(labelmap_path):
    """Load labelmap.json"""
    with open(labelmap_path, 'r', encoding='utf-8') as f:
        labelmap = json.load(f)
    return {item['object_name']: item['object_id'] for item in labelmap}

def json_to_csv(json_path, csv_path, labelmap):
    """Convert a single JSON annotation file to CSV format"""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if 'annotations' not in data or len(data['annotations']) == 0:
            return False
        
        # Get image dimensions
        width = data['images'][0]['width'] if data['images'] else 512
        height = data['images'][0]['height'] if data['images'] else 512
        
        # Get category name from JSON
        category_name = data['categories'][0]['name'] if data['categories'] else 'healthy_rice_leaf'
        
        # Map category name to label ID
        label_id = labelmap.get(category_name.lower().replace(' ', '_'), 1)
        
        # Write CSV file
        with open(csv_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['#item', 'x', 'y', 'width', 'height', 'label'])
            
            for idx, ann in enumerate(data['annotations']):
                bbox = ann.get('bbox', [0, 0, width, height])
                writer.writerow([idx, bbox[0], bbox[1], bbox[2], bbox[3], label_id])
        
        return True
    except Exception as e:
        print(f"Error converting {json_path}: {e}")
        return False

def convert_all_json_to_csv(root_dir='.'):
    """Convert all JSON annotations to CSV format"""
    root = Path(root_dir)
    labelmap_path = root / 'rice_leaves' / 'labelmap.json'
    
    if not labelmap_path.exists():
        print(f"Error: {labelmap_path} does not exist")
        return
    
    labelmap = load_labelmap(labelmap_path)
    
    categories = ['healthy_rice_leaf', 'bacterial_leaf_blight', 'brown_spot', 
                 'leaf_blast', 'leaf_scald', 'sheath_blight']
    
    total_converted = 0
    
    for category in categories:
        category_dir = root / 'rice_leaves' / category
        json_dir = category_dir / 'json'
        csv_dir = category_dir / 'csv'
        
        if not json_dir.exists():
            print(f"Warning: {json_dir} does not exist, skipping {category}")
            continue
        
        csv_dir.mkdir(parents=True, exist_ok=True)
        
        json_files = list(json_dir.glob('*.json'))
        converted = 0
        
        for json_path in json_files:
            csv_path = csv_dir / f"{json_path.stem}.csv"
            if json_to_csv(json_path, csv_path, labelmap):
                converted += 1
        
        print(f"{category}: {converted}/{len(json_files)} JSON files converted to CSV")
        total_converted += converted
    
    print(f"\nTotal: {total_converted} CSV files created")

if __name__ == '__main__':
    convert_all_json_to_csv()





