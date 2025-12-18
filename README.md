# Rice Leaf Disease Classification Dataset

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/your-repo/rice-leaf-disease-classification)

A comprehensive dataset of rice leaf images for disease classification tasks, designed for agricultural computer vision applications focusing on rice plant health monitoring and disease detection.

**Project page**: `https://www.kaggle.com/datasets/anshuhlm257/rice-disease-dataset/data`

## TL;DR

- **Task**: Image Classification, Object Detection
- **Modality**: RGB
- **Platform**: Ground/Field
- **Real/Synthetic**: Real
- **Images**: ~3,829 rice leaf images across 6 disease/health categories
- **Resolution**: Variable (typically 512×512 to 1600×1200 pixels)
- **Annotations**: JSON (per-image), COCO JSON (generated)
- **Categories**: 6 classes (healthy_rice_leaf, bacterial_leaf_blight, brown_spot, leaf_blast, leaf_scald, sheath_blight) plus background
- **License**: CC BY 4.0
- **Citation**: see below

## Table of Contents

- [Download](#download)
- [Dataset Structure](#dataset-structure)
- [Sample Images](#sample-images)
- [Annotation Schema](#annotation-schema)
- [Stats and Splits](#stats-and-splits)
- [Quick Start](#quick-start)
- [Evaluation and Baselines](#evaluation-and-baselines)
- [Datasheet (Data Card)](#datasheet-data-card)
- [Known Issues and Caveats](#known-issues-and-caveats)
- [License](#license)
- [Citation](#citation)
- [Changelog](#changelog)
- [Contact](#contact)

## Download

**Original dataset**: `https://www.kaggle.com/datasets/anshuhlm257/rice-disease-dataset/data`

This repo hosts structure and conversion scripts only; place the downloaded folders under this directory.

**Local license file**: See `LICENSE` in the root directory.

## Dataset Structure

```
rice_leaf_disease_classification/
├── rice_leaves/                          # Main category directory
│   ├── healthy_rice_leaf/                # Healthy rice leaf subcategory
│   │   ├── csv/                           # CSV annotation files (per-image, optional)
│   │   ├── json/                          # JSON annotation files (per-image)
│   │   ├── images/                        # Image files
│   │   └── sets/                          # Dataset split files (optional)
│   ├── bacterial_leaf_blight/             # Bacterial leaf blight subcategory
│   │   └── ... (same structure)
│   ├── brown_spot/                        # Brown spot subcategory
│   │   └── ... (same structure)
│   ├── leaf_blast/                        # Leaf blast subcategory
│   │   └── ... (same structure)
│   ├── leaf_scald/                        # Leaf scald subcategory
│   │   └── ... (same structure)
│   ├── sheath_blight/                     # Sheath blight subcategory
│   │   └── ... (same structure)
│   ├── labelmap.json                      # Label mapping file
│   └── sets/                              # Dataset split files (shared across subcategories)
│       ├── train.txt                      # Training set image list
│       ├── val.txt                        # Validation set image list
│       ├── test.txt                       # Test set image list
│       ├── all.txt                        # All images list
│       └── train_val.txt                  # Train+val images list (optional)
│
├── annotations/                           # COCO format JSON files (generated)
│   ├── healthy_rice_leaf_instances_train.json
│   ├── healthy_rice_leaf_instances_val.json
│   ├── healthy_rice_leaf_instances_test.json
│   ├── ... (other categories)
│   └── combined_instances_{split}.json   # Combined COCO files (if --combined flag used)
│
├── scripts/                               # Utility scripts
│   ├── convert_to_coco.py                # Convert JSON to COCO format
│   └── reorganize_data.py                # Reorganize data to standard structure
│
├── LICENSE                                # License file
├── README.md                              # This file
└── requirements.txt                       # Python dependencies
```

**Splits**: Splits provided via `rice_leaves/sets/*.txt`. List image basenames (no extension). If missing, all images are used.

## Sample Images

<table>
  <tr>
    <th>Category</th>
    <th>Sample</th>
  </tr>
  <tr>
    <td><strong>Healthy Rice Leaf</strong></td>
    <td>
      <img src="rice_leaves/healthy_rice_leaf/images/20231006_163255.jpg" alt="Healthy rice leaf" width="260"/>
      <div align="center"><code>rice_leaves/healthy_rice_leaf/images/20231006_163255.jpg</code></div>
    </td>
  </tr>
  <tr>
    <td><strong>Bacterial Leaf Blight</strong></td>
    <td>
      <img src="rice_leaves/bacterial_leaf_blight/images/20231006_164208.jpg" alt="Bacterial leaf blight" width="260"/>
      <div align="center"><code>rice_leaves/bacterial_leaf_blight/images/20231006_164208.jpg</code></div>
    </td>
  </tr>
  <tr>
    <td><strong>Brown Spot</strong></td>
    <td>
      <img src="rice_leaves/brown_spot/images/sample.jpg" alt="Brown spot" width="260"/>
      <div align="center"><code>rice_leaves/brown_spot/images/sample.jpg</code></div>
    </td>
  </tr>
</table>

## Annotation Schema

### JSON Format (Per-Image)

Each image has a corresponding JSON annotation file in `rice_leaves/{subcategory}/json/{image_name}.json`:

```json
{
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
      "id": 3993181174,
      "width": 1600,
      "height": 1200,
      "file_name": "20231006_163255.jpg",
      "size": 635901,
      "format": "JPEG",
      "url": "",
      "hash": "",
      "status": "success"
    }
  ],
  "annotations": [
    {
      "id": 4020410174,
      "image_id": 3993181174,
      "category_id": 5238355174,
      "segmentation": [],
      "area": 1920000,
      "bbox": [0, 0, 1600, 1200]
    }
  ],
  "categories": [
    {
      "id": 5238355174,
      "name": "Healthy Rice Leaf",
      "supercategory": "Healthy Rice Leaf"
    }
  ]
}
```

**Note**: For classification tasks, each image typically has a single annotation covering the entire image (`bbox: [0, 0, width, height]`), where the category ID indicates the image's class.

### Label Map

The `rice_leaves/labelmap.json` file defines all categories:

```json
[
  {
    "object_id": 0,
    "label_id": 0,
    "keyboard_shortcut": "0",
    "object_name": "background"
  },
  {
    "object_id": 1,
    "label_id": 1,
    "keyboard_shortcut": "1",
    "object_name": "healthy_rice_leaf"
  },
  {
    "object_id": 2,
    "label_id": 2,
    "keyboard_shortcut": "2",
    "object_name": "bacterial_leaf_blight"
  },
  {
    "object_id": 3,
    "label_id": 3,
    "keyboard_shortcut": "3",
    "object_name": "brown_spot"
  },
  {
    "object_id": 4,
    "label_id": 4,
    "keyboard_shortcut": "4",
    "object_name": "leaf_blast"
  },
  {
    "object_id": 5,
    "label_id": 5,
    "keyboard_shortcut": "5",
    "object_name": "leaf_scald"
  },
  {
    "object_id": 6,
    "label_id": 6,
    "keyboard_shortcut": "6",
    "object_name": "sheath_blight"
  }
]
```

### COCO Format

COCO format JSON files are generated in the `annotations/` directory. Example structure:

```json
{
  "info": {
    "year": 2025,
    "version": "1.0",
    "description": "Rice Leaf Disease Classification healthy_rice_leaf train split",
    "url": ""
  },
  "images": [
    {
      "id": 1234567890,
      "file_name": "rice_leaves/healthy_rice_leaf/images/20231006_163255.jpg",
      "width": 1600,
      "height": 1200
    }
  ],
  "annotations": [
    {
      "id": 1,
      "image_id": 1234567890,
      "category_id": 1,
      "bbox": [0, 0, 1600, 1200],
      "area": 1920000,
      "iscrowd": 0
    }
  ],
  "categories": [
    {
      "id": 1,
      "name": "healthy_rice_leaf",
      "supercategory": "rice_leaf"
    }
  ],
  "licenses": []
}
```

## Stats and Splits

### Image Statistics

| Category | Images |
|----------|--------|
| Healthy Rice Leaf | 653 |
| Bacterial Leaf Blight | 636 |
| Brown Spot | 646 |
| Leaf Blast | 634 |
| Leaf Scald | 628 |
| Sheath Blight | 632 |
| **Total** | **~3,829** |

### Dataset Splits

Splits provided via `rice_leaves/sets/*.txt`. You may define your own splits by editing those files.

**Split Format**: Each line contains an image basename (without extension), optionally prefixed with category name:
```
healthy_rice_leaf/20231006_163255
bacterial_leaf_blight/20231006_164208
...
```

Or simply:
```
20231006_163255
20231006_164208
...
```

## Quick Start

### 1. Reorganize Data (if needed)

If you have data in the old structure, reorganize it first:

```bash
python scripts/reorganize_data.py
```

### 2. Convert to COCO Format

Convert JSON annotations to COCO format:

```bash
python scripts/convert_to_coco.py --root . --out annotations \
    --categories healthy_rice_leaf bacterial_leaf_blight brown_spot \
                 leaf_blast leaf_scald sheath_blight \
    --splits train val test --combined
```

### 3. Load with COCO API

```python
from pycocotools.coco import COCO
import matplotlib.pyplot as plt

# Load COCO annotation file
coco = COCO('annotations/combined_instances_train.json')

# Get all image IDs
img_ids = coco.getImgIds()
print(f"Total images: {len(img_ids)}")

# Get all category IDs
cat_ids = coco.getCatIds()
print(f"Categories: {coco.loadCats(cat_ids)}")

# Load a specific image
img_id = img_ids[0]
img_info = coco.loadImgs(img_id)[0]
ann_ids = coco.getAnnIds(imgIds=img_id)
anns = coco.loadAnns(ann_ids)

print(f"Image: {img_info['file_name']}")
print(f"Annotations: {len(anns)}")
```

### Dependencies

**Required**:
- Pillow>=9.5

**Optional** (for COCO API):
- pycocotools>=2.0.7

Install with:
```bash
pip install -r requirements.txt
```

## Evaluation and Baselines

### Metrics

For classification tasks, common evaluation metrics include:
- **Accuracy**: Overall classification accuracy
- **Precision/Recall/F1-Score**: Per-class and macro-averaged metrics
- **Confusion Matrix**: Class-wise classification performance

### Baseline Results

(To be added based on experimental results)

## Datasheet (Data Card)

### Motivation

This dataset was created to support research and development in automated rice disease detection and classification systems, enabling early disease identification and precision agriculture applications.

### Composition

- **Image Types**: RGB images of rice leaves in various conditions
- **Categories**: 6 disease/health categories
- **Annotation Format**: Per-image JSON files with full-image bounding boxes for classification
- **Image Sources**: Field-collected images, some augmented

### Collection Process

Images were collected from rice fields and organized by disease type. Each image is annotated with its disease category using a full-image bounding box annotation.

### Preprocessing

- Images are stored in their original resolution
- Annotations are provided in both per-image JSON format and COCO format (generated)

### Distribution

The dataset is distributed under CC BY 4.0 license. Original source: `https://www.kaggle.com/datasets/anshuhlm257/rice-disease-dataset/data`

### Maintenance

This repository maintains the standardized structure and conversion scripts. For original data updates, refer to the Kaggle dataset page.

## Known Issues and Caveats

1. **Image Resolution**: Images have variable resolutions (from 512×512 to 1600×1200 pixels)
2. **Annotation Format**: Each image has a full-image bounding box annotation for classification purposes
3. **Category Mapping**: Original folder names are mapped to standardized category names (see `scripts/reorganize_data.py`)
4. **Split Files**: Split files need to be created manually or generated based on your requirements

## License

This dataset is licensed under the **Creative Commons Attribution 4.0 International (CC BY 4.0)** license.

See `LICENSE` file for full license text.

**Summary**: You are free to:
- Share — copy and redistribute the material in any medium or format
- Adapt — remix, transform, and build upon the material for any purpose, even commercially

Under the following terms:
- **Attribution** — You must give appropriate credit, provide a link to the license, and indicate if changes were made

Check the original dataset terms and cite appropriately.

## Citation

If you use this dataset, please cite:

```bibtex
@dataset{rice_leaf_disease_classification_2025,
  title={Rice Leaf Disease Classification Dataset},
  author={Dataset Contributors},
  year={2025},
  url={https://www.kaggle.com/datasets/anshuhlm257/rice-disease-dataset/data},
  license={CC BY 4.0}
}
```

## Changelog

- **V1.0.0** (2025): Initial standardized structure and COCO conversion utility

## Contact

- **Maintainers**: Dataset maintainers
- **Original Authors**: See Kaggle dataset page
- **Source**: `https://www.kaggle.com/datasets/anshuhlm257/rice-disease-dataset/data`
