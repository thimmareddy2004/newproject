# GoAround - Travel Platform

A comprehensive travel platform built with Flask featuring fuel calculator, bike rentals, package management, and interactive maps.

## Features

- **User Authentication**: Secure login/signup system
- **Fuel Calculator**: India-specific fuel cost calculations
- **Bike Rentals**: Browse and book bikes
- **Travel Packages**: Create and manage travel packages
- **Interactive Maps**: Karnataka districts with place markers
- **Admin Dashboard**: User login tracking

## Live Demo

🚀 **Deployed Application**: [Your app will be available here after deployment]

## Quick Deploy to Railway

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/python-flask)

### 1. One-Click Railway Deployment

1. Click the "Deploy on Railway" button above
2. Connect your GitHub account
3. Fork this repository 
4. Railway will automatically deploy your app
5. Your app will be live at `https://your-app-name.up.railway.app`

### 2. Manual Railway Deployment

1. Go to [Railway.app](https://railway.app)
2. Sign up/Login with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select this repository
5. Railway will automatically:
   - Detect it's a Python app
   - Install dependencies from requirements.txt
   - Start the app with gunicorn

### 3. Environment Variables (Optional)

Set these in Railway dashboard → Variables:
- `SECRET_KEY`: A secure secret key
- `ORS_API_KEY`: OpenRouteService API key for routing
- `FLASK_ENV`: `production`

## Alternative: Deploy to Render

1. Go to [Render.com](https://render.com)
2. Click "New" → "Web Service"
3. Connect your GitHub and select this repo
4. Use these settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn wsgi:app`
   - **Python Version**: 3.9

## Local Development

```bash
# Clone the repository
git clone https://github.com/thimmareddy2004/newproject.git
cd newproject

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

Visit `http://localhost:5000`

## Docker Deployment

```bash
# Build and run with Docker
docker-compose up --build

# Or just Docker
docker build -t goaround .
docker run -p 5000:5000 goaround
```

## Project Structure

```
newproject/
├── app.py                 # Main Flask application
├── wsgi.py               # WSGI entry point
├── requirements.txt      # Python dependencies
├── Dockerfile           # Docker configuration
├── Procfile            # Heroku/Railway deployment
├── templates/          # HTML templates
├── static/            # CSS, JS, images
├── microservices/     # Fuel calculator & APIs
├── data/             # SQLite database & cached data
└── .github/workflows/ # CI/CD pipeline
```

## API Endpoints

- `GET /` - Home page
- `POST /signup` - User registration
- `POST /signin` - User login
- `GET /fuel-calculator` - Fuel cost calculator
- `GET /bike-rental` - Bike rental page
- `GET /packages` - Travel packages
- `GET /maps` - Interactive maps
- `GET /api/fuel/*` - Fuel calculator APIs

## Technologies Used

- **Backend**: Flask, SQLAlchemy
- **Frontend**: HTML, CSS, JavaScript, React components
- **Database**: SQLite (development), PostgreSQL (production ready)
- **Maps**: Leaflet.js with OpenStreetMap
- **Deployment**: Railway, Docker, GitHub Actions
- **APIs**: OpenRouteService for routing

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is open source and available under the MIT License.