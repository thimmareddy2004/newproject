from flask import Flask, redirect, render_template, request, jsonify, url_for, flash

# Simple Flask app without database dependencies for testing
app = Flask(__name__)
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

# Simplified auth routes (no database)
@app.route('/signup', methods=['POST'])
def signup():
    flash("Account created successfully! Please sign in.", "success")
    return redirect(url_for('auth'))

@app.route('/signin', methods=['POST'])
def signin():
    return redirect(url_for('home'))

if __name__ == '__main__':
    print("🚀 Starting GoAround Project")
    print("✅ Cars & Bikes Rental System Integrated")
    print("📱 Features Available:")
    print("   - Vehicle Fleet (Cars & Bikes)")
    print("   - Complete Booking System")
    print("   - WhatsApp Integration")
    print("   - Paradise Tours Styling")
    print("")
    print("🌐 Starting server at http://localhost:5000")
    print("📝 Note: Database features disabled for testing")
    app.run(debug=True, port=5000)