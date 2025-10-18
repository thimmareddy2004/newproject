from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <h1>GoAround Taxi Rental Demo</h1>
    <p><a href="/rentals">View Vehicle Fleet</a></p>
    <p><a href="/taxi-rental">Book a Taxi</a></p>
    '''

@app.route('/rentals')
def rentals():
    return render_template('rentals.html')

@app.route('/rentals.html')
def rentals_html():
    return render_template('rentals.html')

@app.route('/taxi-rental')
def taxi_rental():
    return render_template('taxi_rental.html')

if __name__ == '__main__':
    print("🚗 GoAround Taxi Rental System")
    print("✅ Paradise Tours style implementation complete!")
    print("📂 Files created:")
    print("   - templates/rentals.html (Updated with Paradise Tours style)")
    print("   - templates/taxi_rental.html (Complete booking system)")
    print()
    print("🎨 Features implemented:")
    print("   ✅ Dark theme with yellow accents (#fbbf24)")
    print("   ✅ Animated background grid")
    print("   ✅ Interactive vehicle cards with hover effects")
    print("   ✅ Price badges and rating system")
    print("   ✅ Responsive grid layout")
    print("   ✅ Complete booking form with validation")
    print("   ✅ WhatsApp integration")
    print("   ✅ Loading states and animations")
    print("   ✅ Trip type toggle (Local/Outstation)")
    print("   ✅ Vehicle filtering by passenger count")
    print()
    print("🚀 Starting test server at http://localhost:5000")
    print("📱 Note: WhatsApp integration uses the same number as Paradise Tours")
    
    app.run(debug=True, port=5000)