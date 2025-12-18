#!/usr/bin/env python3
"""
Distribute split files from rice_leaves/sets/ to each subcategory's sets/ directory.
"""

from pathlib import Path

def distribute_splits(root_dir='.'):
    """Distribute split files to each subcategory directory"""
    root = Path(root_dir)
    main_sets_dir = root / 'rice_leaves' / 'sets'
    
    if not main_sets_dir.exists():
        print(f"Error: {main_sets_dir} does not exist")
        return
    
    # Subcategories
    subcategories = [
        'healthy_rice_leaf',
        'bacterial_leaf_blight',
        'brown_spot',
        'leaf_blast',
        'leaf_scald',
        'sheath_blight'
    ]
    
    # Split file names
    split_files = ['train.txt', 'val.txt', 'test.txt', 'all.txt', 'train_val.txt']
    
    # Read main split files
    main_splits = {}
    for split_file in split_files:
        split_path = main_sets_dir / split_file
        if split_path.exists():
            with open(split_path, 'r', encoding='utf-8') as f:
                lines = [line.strip() for line in f if line.strip()]
            main_splits[split_file] = lines
            print(f"Loaded {split_file}: {len(lines)} entries")
        else:
            print(f"Warning: {split_file} does not exist")
    
    # Distribute to each subcategory
    for subcategory in subcategories:
        subcategory_sets_dir = root / 'rice_leaves' / subcategory / 'sets'
        subcategory_sets_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"\nProcessing {subcategory}...")
        
        for split_file in split_files:
            if split_file not in main_splits:
                continue
            
            # Filter entries for this subcategory
            subcategory_entries = []
            for entry in main_splits[split_file]:
                # Entry format: "subcategory/image_stem" or just "image_stem"
                if entry.startswith(f"{subcategory}/"):
                    # Remove subcategory prefix, keep only image stem
                    image_stem = entry[len(f"{subcategory}/"):]
                    subcategory_entries.append(image_stem)
                elif '/' not in entry:
                    # If no prefix, check if image exists in this subcategory
                    images_dir = root / 'rice_leaves' / subcategory / 'images'
                    for ext in ['.jpg', '.jpeg', '.png', '.bmp']:
                        if (images_dir / f"{entry}{ext}").exists():
                            subcategory_entries.append(entry)
                            break
            
            # Write to subcategory sets directory
            if subcategory_entries:
                output_path = subcategory_sets_dir / split_file
                with open(output_path, 'w', encoding='utf-8') as f:
                    for entry in sorted(subcategory_entries):
                        f.write(f"{entry}\n")
                print(f"  Created {split_file}: {len(subcategory_entries)} entries")
            else:
                print(f"  Warning: No entries found for {split_file}")
    
    print("\nDistribution complete!")

if __name__ == '__main__':
    distribute_splits()





