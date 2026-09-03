from PIL import Image
import os

print("Image sizes across regions:")
for region in ['canterbury', 'otago', 'auckland', 'christchurch']:
    files = os.listdir(f'nz_data/{region}')
    if files:
        img = Image.open(f'nz_data/{region}/{files[0]}')
        print(f'{region}: {img.size}')
