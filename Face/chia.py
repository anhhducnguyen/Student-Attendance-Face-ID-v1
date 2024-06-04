import os
import shutil
from sklearn.model_selection import train_test_split

def create_dataset_structure(base_dir, categories):
    for category in categories:
        train_dir = os.path.join(base_dir, 'train', category)
        val_dir = os.path.join(base_dir, 'val', category)
        os.makedirs(train_dir, exist_ok=True)
        os.makedirs(val_dir, exist_ok=True)

def split_dataset(dataset_dir, train_count=20, val_count=10):
    categories = [d for d in os.listdir(dataset_dir) if os.path.isdir(os.path.join(dataset_dir, d))]
    create_dataset_structure('dataset_split', categories)
    
    for category in categories:
        category_dir = os.path.join(dataset_dir, category)
        images = [f for f in os.listdir(category_dir) if os.path.isfile(os.path.join(category_dir, f)) and f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        # Ensure we have enough images to split
        if len(images) < (train_count + val_count):
            print(f"Not enough images in {category} to split. Skipping.")
            continue
        
        # Shuffle images to randomize the split
        train_images, val_images = train_test_split(images, train_size=train_count, test_size=val_count, random_state=42)
        
        for image in train_images:
            src = os.path.join(category_dir, image)
            dst = os.path.join('dataset_split', 'train', category, image)
            shutil.copyfile(src, dst)
        
        for image in val_images:
            src = os.path.join(category_dir, image)
            dst = os.path.join('dataset_split', 'val', category, image)
            shutil.copyfile(src, dst)
        
        print(f"Category {category}: {len(train_images)} train images, {len(val_images)} val images")

dataset_dir = 'dataset'
split_dataset(dataset_dir)
