@echo off
echo Starting GoAround Microservices...

echo.
echo Starting Auth Service on port 5001...
start cmd /k "cd auth-service && python app.py"

timeout /t 3

echo Starting Package Service on port 5002...
start cmd /k "cd package-service && python app.py"

timeout /t 3

echo Starting Maps Service on port 5003...
start cmd /k "cd maps-service && python app.py"

timeout /t 3

echo Starting API Gateway on port 5000...
start cmd /k "cd api-gateway && python app.py"

echo.
echo All services started!
echo.
echo Services:
echo - Auth Service:     http://localhost:5001
echo - Package Service:  http://localhost:5002
echo - Maps Service:     http://localhost:5003
echo - API Gateway:      http://localhost:5000
echo.
echo Access the application at: http://localhost:5000
pause