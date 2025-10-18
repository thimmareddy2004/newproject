from flask import Flask, redirect, render_template, request, jsonify, url_for, flash, send_from_directory
import os

# Complete Flask app with proper static file serving
app = Flask(__name__, static_folder='static', static_url_path='/static')
app.secret_key = 'your_secret_key_here'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<page>.html')
def render_template_page(page):
    """Render a template that lives in the templates folder when requested as '/name.html'."""
    try:
        return render_template(f"{page}.html")
    except Exception:
        return redirect('/auth')

@app.route('/auth')
def auth():
    return render_template('auth.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/fuel-calculator')
def fuel_calculator():
    return render_template('fuel_calculator.html')

@app.route('/rentals')
def rentals():
    return render_template('rentals.html')

@app.route('/taxi-rental')
def taxi_rental():
    return render_template('taxi_rental.html')

@app.route('/home')
def home():
    return render_template('home.html')

# Static file serving (for images)
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

# Simplified auth routes (no database)
@app.route('/signup', methods=['POST'])
def signup():
    flash("Account created successfully! Please sign in.", "success")
    return redirect(url_for('auth'))

@app.route('/signin', methods=['POST'])
def signin():
    return redirect(url_for('home'))

if __name__ == '__main__':
    print("🚀 GoAround - Complete Cars & Bikes Rental System")
    print("=" * 50)
    print("✅ Features Integrated:")
    print("   🚗 Car Rentals - 5 vehicles")
    print("   🏍️ Bike Rentals - 15 popular Indian bikes")
    print("   🎨 Paradise Tours styling (Dark theme + Yellow accents)")
    print("   📱 WhatsApp booking integration")
    print("   🔄 Smooth toggle between Cars & Bikes")
    print("   📋 Complete booking forms")
    print("   🖼️ Custom generated vehicle images")
    print("   📱 Mobile responsive design")
    print()
    print("🏍️ Indian Bikes Available:")
    bikes = [
        "Royal Enfield Classic 350", "Bajaj Pulsar NS200", "Hero Splendor Plus",
        "Honda Activa 6G", "Yamaha FZ-S Fi V3", "KTM Duke 200", "Honda Shine 125",
        "TVS Apache RTR 160", "Bajaj Avenger Street 220", "Suzuki Gixxer 155",
        "Honda CB Hornet 160R", "TVS Jupiter 125", "Hero Xtreme 160R", 
        "Bajaj CT 110", "Yamaha R15 V4"
    ]
    for i, bike in enumerate(bikes, 1):
        print(f"   {i:2d}. {bike}")
    
    print()
    print("🚗 Cars Available:")
    cars = ["Swift Dzire", "Honda Amaze", "Maruti Ertiga", "Innova Crysta", "Tempo Traveller"]
    for i, car in enumerate(cars, 1):
        print(f"   {i}. {car}")
    
    print()
    print("🌐 Server starting at: http://localhost:5000")
    print("📝 Navigation:")
    print("   • Home → Auth → Sign In → Home Page")
    print("   • Click 'Rentals' → Toggle Cars/Bikes → Book Now")
    print("   • Complete booking form → WhatsApp integration")
    print()
    print("🎯 Direct URLs:")
    print("   • Vehicle Fleet: http://localhost:5000/rentals")
    print("   • Booking Page: http://localhost:5000/taxi-rental")
    print("=" * 50)
    
    app.run(debug=True, port=5000, host='127.0.0.1')