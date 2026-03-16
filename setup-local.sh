#!/bin/bash

# Employee Attendance System - Local Setup Script (macOS/Linux)

echo "🚀 Employee Attendance System - Local Setup"
echo "============================================"
echo ""

# Check prerequisites
echo "📋 Checking prerequisites..."

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11+"
    exit 1
fi
echo "✅ Python 3 found: $(python3 --version)"

if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+"
    exit 1
fi
echo "✅ Node.js found: $(node --version)"

if ! command -v mongod &> /dev/null; then
    echo "⚠️  MongoDB not found. Please install MongoDB"
    echo "   macOS: brew install mongodb-community"
    echo "   Linux: sudo apt-get install mongodb"
    exit 1
fi
echo "✅ MongoDB found"

echo ""
echo "🔧 Setting up Backend..."
cd backend || exit

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env if not exists
if [ ! -f ".env" ]; then
    echo "Creating backend .env file..."
    cat > .env << EOF
MONGO_URL=mongodb://localhost:27017
DB_NAME=attendance_system
CORS_ORIGINS=http://localhost:3000
EOF
    echo "✅ Backend .env created"
else
    echo "✅ Backend .env already exists"
fi

cd ..

echo ""
echo "🎨 Setting up Frontend..."
cd frontend || exit

# Install dependencies
if command -v yarn &> /dev/null; then
    echo "Installing dependencies with Yarn..."
    yarn install
else
    echo "Installing dependencies with npm..."
    npm install
fi

# Create .env if not exists
if [ ! -f ".env" ]; then
    echo "Creating frontend .env file..."
    cat > .env << EOF
REACT_APP_BACKEND_URL=http://localhost:8001
EOF
    echo "✅ Frontend .env created"
else
    echo "✅ Frontend .env already exists"
fi

cd ..

echo ""
echo "✅ Setup Complete!"
echo ""
echo "📝 Next Steps:"
echo "1. Start MongoDB: brew services start mongodb-community (macOS) or sudo systemctl start mongodb (Linux)"
echo "2. Open TWO terminal windows"
echo ""
echo "Terminal 1 - Start Backend:"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   uvicorn server:app --reload --host 0.0.0.0 --port 8001"
echo ""
echo "Terminal 2 - Start Frontend:"
echo "   cd frontend"
echo "   yarn start    (or npm start)"
echo ""
echo "Then open: http://localhost:3000"
echo ""
echo "🎉 Happy coding!"
