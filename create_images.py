from PIL import Image, ImageDraw, ImageFont
import os

def create_placeholder_image(text, filename, color_bg='#1f2937', color_text='#fbbf24', width=400, height=300):
    """Create a placeholder image with text"""
    # Create image
    img = Image.new('RGB', (width, height), color_bg)
    draw = ImageDraw.Draw(img)
    
    # Try to use a better font, fallback to default
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()
    
    # Get text bounding box
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Center text
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    
    # Draw text
    draw.text((x, y), text, fill=color_text, font=font)
    
    # Save image
    img.save(filename)
    print(f"Created: {filename}")

# Create directories
os.makedirs('static/images', exist_ok=True)
os.makedirs('static/images/bikes', exist_ok=True)

print("🎨 Creating placeholder images...")
print()

# Create car images
car_images = [
    ('Swift Dzire', 'static/images/swift.jpg'),
    ('Honda Amaze', 'static/images/amaze.jpg'), 
    ('Maruti Ertiga', 'static/images/ertiga.jpg'),
    ('Innova Crysta', 'static/images/innova.jpg'),
    ('Tempo Traveller', 'static/images/tempo.jpg')
]

print("🚗 Creating car images:")
for name, path in car_images:
    create_placeholder_image(name, path, '#1f2937', '#fbbf24')

print()

# Create bike images
bike_images = [
    ('Royal Enfield\nClassic 350', 'static/images/bikes/royal_enfield_classic.jpg'),
    ('Bajaj Pulsar\nNS200', 'static/images/bikes/bajaj_pulsar.jpg'),
    ('Hero Splendor\nPlus', 'static/images/bikes/hero_splendor.jpg'),
    ('Honda Activa\n6G', 'static/images/bikes/honda_activa.jpg'),
    ('Yamaha FZ-S\nFi V3', 'static/images/bikes/yamaha_fz.jpg'),
    ('KTM Duke\n200', 'static/images/bikes/ktm_duke.jpg'),
    ('Honda Shine\n125', 'static/images/bikes/honda_shine.jpg'),
    ('TVS Apache\nRTR 160', 'static/images/bikes/tvs_apache.jpg'),
    ('Bajaj Avenger\nStreet 220', 'static/images/bikes/bajaj_avenger.jpg'),
    ('Suzuki Gixxer\n155', 'static/images/bikes/suzuki_gixxer.jpg'),
    ('Honda CB\nHornet 160R', 'static/images/bikes/honda_hornet.jpg'),
    ('TVS Jupiter\n125', 'static/images/bikes/tvs_jupiter.jpg'),
    ('Hero Xtreme\n160R', 'static/images/bikes/hero_xtreme.jpg'),
    ('Bajaj CT\n110', 'static/images/bikes/bajaj_ct.jpg'),
    ('Yamaha R15\nV4', 'static/images/bikes/yamaha_r15.jpg')
]

print("🏍️ Creating bike images:")
for name, path in bike_images:
    create_placeholder_image(name, path, '#111827', '#f59e0b')

print()
print("✅ All placeholder images created successfully!")
print("🚀 Ready to run the rental system!")