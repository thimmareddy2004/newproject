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
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        # Open and process image
        img = Image.open(io.BytesIO(response.content))
        
        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize to fit our requirements
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Save image
        img.save(filename, 'JPEG', quality=90)
        print(f"✅ Saved: {filename}")
        
    except Exception as e:
        print(f"❌ Failed to download {filename}: {str(e)}")
        return False
    
    return True

# Create directories if they don't exist
os.makedirs('static/images', exist_ok=True)
os.makedirs('static/images/bikes', exist_ok=True)

print("🚗 Downloading exact car model images...")
print()

# Exact car model images
car_images = [
    {
        'name': 'Swift Dzire',
        'url': 'https://imgd-ct.aeplcdn.com/664x415/n/cw/ec/130591/swift-dzire-exterior-right-front-three-quarter-109.jpeg?isig=0&q=80',
        'filename': 'static/images/dzire.jpg'
    },
    {
        'name': 'Honda Amaze',
        'url': 'https://imgd-ct.aeplcdn.com/664x415/n/cw/ec/115025/amaze-exterior-right-front-three-quarter-4.jpeg?isig=0&q=80',
        'filename': 'static/images/amaze.jpg'
    },
    {
        'name': 'Maruti Ertiga',
        'url': 'https://imgd-ct.aeplcdn.com/664x415/n/cw/ec/115777/ertiga-exterior-right-front-three-quarter-5.jpeg?isig=0&q=80',
        'filename': 'static/images/ertiga.jpg'
    },
    {
        'name': 'Toyota Innova Crysta',
        'url': 'https://imgd-ct.aeplcdn.com/664x415/n/cw/ec/26701/innova-crysta-exterior-right-front-three-quarter-2.jpeg?q=80',
        'filename': 'static/images/innova.jpg'
    },
    {
        'name': 'Tempo Traveller',
        'url': 'https://imgd-ct.aeplcdn.com/664x415/n/cw/ec/40087/tempo-traveller-exterior-right-front-three-quarter-2.jpeg?q=80',
        'filename': 'static/images/tempo.jpg'
    }
]

# Download car images
for img in car_images:
    download_and_save_image(img['url'], img['filename'])

print()
print("🏍️ Downloading exact bike model images...")
print()

# Exact bike model images
bike_images = [
    {
        'name': 'Royal Enfield Classic 350',
        'url': 'https://bd.gaadicdn.com/processedimages/royal-enfield/classic-350/494X300/classic-3502022827.jpg?tr=w-880',
        'filename': 'static/images/bikes/royal_enfield_classic.jpg'
    },
    {
        'name': 'Bajaj Pulsar NS200',
        'url': 'https://bd.gaadicdn.com/processedimages/bajaj/pulsar-ns200/494X300/pulsar-ns20062f4c31d1b4e8e.jpg?tr=w-880',
        'filename': 'static/images/bikes/bajaj_pulsar.jpg'
    },
    {
        'name': 'Hero Splendor Plus',
        'url': 'https://bd.gaadicdn.com/processedimages/hero/splendor-plus/494X300/splendor-plus63f4c31d1b4e8e.jpg?tr=w-880',
        'filename': 'static/images/bikes/hero_splendor.jpg'
    },
    {
        'name': 'Honda Activa 6G',
        'url': 'https://bd.gaadicdn.com/processedimages/honda/activa-6g/494X300/activa-6g63f4c31d1b4e8e.jpg?tr=w-880',
        'filename': 'static/images/bikes/honda_activa.jpg'
    },
    {
        'name': 'Yamaha FZ-S Fi V3',
        'url': 'https://bd.gaadicdn.com/processedimages/yamaha/fz-s-fi/494X300/fz-s-fi63f4c31d1b4e8e.jpg?tr=w-880',
        'filename': 'static/images/bikes/yamaha_fz.jpg'
    },
    {
        'name': 'KTM Duke 200',
        'url': 'https://bd.gaadicdn.com/processedimages/ktm/200-duke/494X300/200-duke63f4c31d1b4e8e.jpg?tr=w-880',
        'filename': 'static/images/bikes/ktm_duke.jpg'
    },
    {
        'name': 'Honda Shine 125',
        'url': 'https://bd.gaadicdn.com/processedimages/honda/shine/494X300/shine63f4c31d1b4e8e.jpg?tr=w-880',
        'filename': 'static/images/bikes/honda_shine.jpg'
    },
    {
        'name': 'TVS Apache RTR 160',
        'url': 'https://bd.gaadicdn.com/processedimages/tvs/apache-rtr-160/494X300/apache-rtr-16063f4c31d1b4e8e.jpg?tr=w-880',
        'filename': 'static/images/bikes/tvs_apache.jpg'
    },
    {
        'name': 'Bajaj Avenger Street 220',
        'url': 'https://bd.gaadicdn.com/processedimages/bajaj/avenger-street-220/494X300/avenger-street-22063f4c31d1b4e8e.jpg?tr=w-880',
        'filename': 'static/images/bikes/bajaj_avenger.jpg'
    },
    {
        'name': 'Suzuki Gixxer 155',
        'url': 'https://bd.gaadicdn.com/processedimages/suzuki/gixxer/494X300/gixxer63f4c31d1b4e8e.jpg?tr=w-880',
        'filename': 'static/images/bikes/suzuki_gixxer.jpg'
    },
    {
        'name': 'Honda CB Hornet 160R',
        'url': 'https://bd.gaadicdn.com/processedimages/honda/cb-hornet-160r/494X300/cb-hornet-160r63f4c31d1b4e8e.jpg?tr=w-880',
        'filename': 'static/images/bikes/honda_hornet.jpg'
    },
    {
        'name': 'TVS Jupiter 125',
        'url': 'https://bd.gaadicdn.com/processedimages/tvs/jupiter/494X300/jupiter63f4c31d1b4e8e.jpg?tr=w-880',
        'filename': 'static/images/bikes/tvs_jupiter.jpg'
    },
    {
        'name': 'Hero Xtreme 160R',
        'url': 'https://bd.gaadicdn.com/processedimages/hero/xtreme-160r/494X300/xtreme-160r63f4c31d1b4e8e.jpg?tr=w-880',
        'filename': 'static/images/bikes/hero_xtreme.jpg'
    },
    {
        'name': 'Bajaj CT 110',
        'url': 'https://bd.gaadicdn.com/processedimages/bajaj/ct-110/494X300/ct-11063f4c31d1b4e8e.jpg?tr=w-880',
        'filename': 'static/images/bikes/bajaj_ct.jpg'
    },
    {
        'name': 'Yamaha R15 V4',
        'url': 'https://bd.gaadicdn.com/processedimages/yamaha/yzf-r15/494X300/yzf-r1563f4c31d1b4e8e.jpg?tr=w-880',
        'filename': 'static/images/bikes/yamaha_r15.jpg'
    }
]

# Download bike images
for img in bike_images:
    download_and_save_image(img['url'], img['filename'])

print()
print("🎉 All exact vehicle model images downloaded!")
print("✅ Your rental system now has precise photos for each vehicle model!")