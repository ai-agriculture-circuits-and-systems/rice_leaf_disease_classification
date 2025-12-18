#!/usr/bin/env python3
"""
Create dataset split files (train/val/test) for Rice Leaf Disease Classification dataset.
"""

import os
import random
from pathlib import Path

def create_splits(root_dir='.', train_ratio=0.7, val_ratio=0.15, test_ratio=0.15, seed=42):
    """Create train/val/test split files"""
    root = Path(root_dir)
    sets_dir = root / 'rice_leaves' / 'sets'
    sets_dir.mkdir(parents=True, exist_ok=True)
    
    categories = ['healthy_rice_leaf', 'bacterial_leaf_blight', 'brown_spot', 
                 'leaf_blast', 'leaf_scald', 'sheath_blight']
    
    random.seed(seed)
    
    all_images = []
    train_images = []
    val_images = []
    test_images = []
    
    for category in categories:
        images_dir = root / 'rice_leaves' / category / 'images'
        
        if not images_dir.exists():
            print(f"Warning: {images_dir} does not exist, skipping {category}")
            continue
        
        # Get all image files
        image_files = []
        for ext in ['.jpg', '.jpeg', '.png', '.bmp']:
            image_files.extend(images_dir.glob(f'*{ext}'))
        
        # Remove duplicates and get stems
        image_stems = sorted(list(set([f.stem for f in image_files])))
        
        print(f"{category}: {len(image_stems)} images")
        
        # Shuffle
        random.shuffle(image_stems)
        
        # Calculate split sizes
        n_total = len(image_stems)
        n_train = int(n_total * train_ratio)
        n_val = int(n_total * val_ratio)
        n_test = n_total - n_train - n_val
        
        # Split
        category_train = image_stems[:n_train]
        category_val = image_stems[n_train:n_train+n_val]
        category_test = image_stems[n_train+n_val:]
        
        # Add to global lists (with category prefix)
        for stem in category_train:
            train_images.append(f"{category}/{stem}")
            all_images.append(f"{category}/{stem}")
        
        for stem in category_val:
            val_images.append(f"{category}/{stem}")
            all_images.append(f"{category}/{stem}")
        
        for stem in category_test:
            test_images.append(f"{category}/{stem}")
            all_images.append(f"{category}/{stem}")
        
        print(f"  Train: {len(category_train)}, Val: {len(category_val)}, Test: {len(category_test)}")
    
    # Write split files
    def write_split_file(filename, images):
        filepath = sets_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            for img in sorted(images):
                f.write(f"{img}\n")
        print(f"Created {filepath}: {len(images)} images")
    
    write_split_file('train.txt', train_images)
    write_split_file('val.txt', val_images)
    write_split_file('test.txt', test_images)
    write_split_file('all.txt', all_images)
    
    # Create train_val.txt
    train_val_images = train_images + val_images
    write_split_file('train_val.txt', train_val_images)
    
    print(f"\nTotal: {len(all_images)} images")
    print(f"Train: {len(train_images)} ({len(train_images)/len(all_images)*100:.1f}%)")
    print(f"Val: {len(val_images)} ({len(val_images)/len(all_images)*100:.1f}%)")
    print(f"Test: {len(test_images)} ({len(test_images)/len(all_images)*100:.1f}%)")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Create dataset split files')
    parser.add_argument('--root', type=str, default='.', help='Dataset root directory')
    parser.add_argument('--train', type=float, default=0.7, help='Training set ratio')
    parser.add_argument('--val', type=float, default=0.15, help='Validation set ratio')
    parser.add_argument('--test', type=float, default=0.15, help='Test set ratio')
    parser.add_argument('--seed', type=int, default=42, help='Random seed')
    
    args = parser.parse_args()
    
    # Normalize ratios
    total = args.train + args.val + args.test
    args.train /= total
    args.val /= total
    args.test /= total
    
    create_splits(args.root, args.train, args.val, args.test, args.seed)





