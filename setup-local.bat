@echo off
REM Employee Attendance System - Local Setup Script (Windows)

echo ========================================
echo Employee Attendance System - Local Setup
echo ========================================
echo.

echo Checking prerequisites...
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [X] Python is not installed. Please install Python 3.11+
    exit /b 1
)
echo [OK] Python found

REM Check Node
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [X] Node.js is not installed. Please install Node.js 18+
    exit /b 1
)
echo [OK] Node.js found

REM Check MongoDB
mongod --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] MongoDB not found. Please install MongoDB Community Server
    exit /b 1
)
echo [OK] MongoDB found

echo.
echo Setting up Backend...
cd backend

REM Create virtual environment
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate

REM Install dependencies
echo Installing Python dependencies...
pip install --upgrade pip
pip install -r requirements.txt

REM Create .env if not exists
if not exist ".env" (
    echo Creating backend .env file...
    (
        echo MONGO_URL=mongodb://localhost:27017
        echo DB_NAME=attendance_system
        echo CORS_ORIGINS=http://localhost:3000
    ) > .env
    echo [OK] Backend .env created
) else (
    echo [OK] Backend .env already exists
)

cd ..

echo.
echo Setting up Frontend...
cd frontend

REM Install dependencies
where yarn >nul 2>&1
if %errorlevel% equ 0 (
    echo Installing dependencies with Yarn...
    call yarn install
) else (
    echo Installing dependencies with npm...
    call npm install
)

REM Create .env if not exists
if not exist ".env" (
    echo Creating frontend .env file...
    (
        echo REACT_APP_BACKEND_URL=http://localhost:8001
    ) > .env
    echo [OK] Frontend .env created
) else (
    echo [OK] Frontend .env already exists
)

cd ..

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next Steps:
echo 1. Make sure MongoDB is running (check Services)
echo 2. Open TWO command prompts
echo.
echo Terminal 1 - Start Backend:
echo    cd backend
echo    venv\Scripts\activate
echo    uvicorn server:app --reload --host 0.0.0.0 --port 8001
echo.
echo Terminal 2 - Start Frontend:
echo    cd frontend
echo    yarn start    (or npm start)
echo.
echo Then open: http://localhost:3000
echo.
echo Happy coding!
echo.
pause
