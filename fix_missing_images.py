import requests
import os
from PIL import Image
import io

def download_and_save_image(url, filename, max_size=(400, 300)):
    """Download image from URL and save it with proper sizing"""
    try:
        print(f"Downloading: {filename}")
        
        # Download image
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Open and process image
        img = Image.open(io.BytesIO(response.content))
        
        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize to fit our requirements
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Save image
        img.save(filename, 'JPEG', quality=85)
        print(f"✅ Saved: {filename}")
        
    except Exception as e:
        print(f"❌ Failed to download {filename}: {str(e)}")
        return False
    
    return True

print("🔧 Downloading missing vehicle images...")
print()

# Better URLs for missing images
missing_images = [
    {
        'name': 'Honda Amaze',
        'url': 'https://images.unsplash.com/photo-1549924231-f129b911e442?w=400&h=300&fit=crop&crop=center',
        'filename': 'static/images/amaze.jpg'
    },
    {
        'name': 'Royal Enfield Classic 350',
        'url': 'https://images.unsplash.com/photo-1571068316344-75bc76f77890?w=400&h=300&fit=crop&crop=center',
        'filename': 'static/images/bikes/royal_enfield_classic.jpg'
    },
    {
        'name': 'Hero Splendor Plus',
        'url': 'https://images.unsplash.com/photo-1568772585407-9361f9bf3a87?w=400&h=300&fit=crop&crop=center',
        'filename': 'static/images/bikes/hero_splendor.jpg'
    },
    {
        'name': 'Bajaj Avenger Street 220',
        'url': 'https://images.unsplash.com/photo-1609630875171-b1321377ee65?w=400&h=300&fit=crop&crop=center',
        'filename': 'static/images/bikes/bajaj_avenger.jpg'
    },
    {
        'name': 'Bajaj CT 110',
        'url': 'https://images.unsplash.com/photo-1449426468159-d96dbf08f19f?w=400&h=300&fit=crop&crop=center',
        'filename': 'static/images/bikes/bajaj_ct.jpg'
    }
]

# Download missing images
for img in missing_images:
    if not os.path.exists(img['filename']) or os.path.getsize(img['filename']) < 1000:
        download_and_save_image(img['url'], img['filename'])
    else:
        print(f"✅ Already exists: {img['filename']}")

print()
print("🎉 All missing images have been filled!")
print("✅ Your rental system now has complete vehicle photos!")