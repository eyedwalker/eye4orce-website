import requests
import os

# Create images directory if it doesn't exist
if not os.path.exists('static/images'):
    os.makedirs('static/images')

# List of image URLs and their filenames
image_urls = {
    'https://images.unsplash.com/photo-1523275335684-37898b6b398b': 'hero-collection.jpg',
    'https://images.unsplash.com/photo-1560448205-997153425200': 'prescription-frames.jpg',
    'https://images.unsplash.com/photo-1560448205-997153425200': 'prescription-lenses.jpg',
    'https://images.unsplash.com/photo-1560448205-997153425200': 'sunglasses.jpg',
    'https://images.unsplash.com/photo-1560448205-997153425200': 'signature-frames.jpg',
    'https://images.unsplash.com/photo-1560448205-997153425200': 'sports-eyewear.jpg',
    'https://images.unsplash.com/photo-1560448205-997153425200': 'luxury-eyewear.jpg'
}

# Download and save each image
for url, filename in image_urls.items():
    try:
        # Download the image
        response = requests.get(url)
        response.raise_for_status()
        
        # Save the image
        with open(f'static/images/{filename}', 'wb') as f:
            f.write(response.content)
        print(f'Successfully downloaded {filename}')
    except Exception as e:
        print(f'Error downloading {filename}: {str(e)}')
