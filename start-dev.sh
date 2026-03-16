#!/bin/bash

# Quick start script for development (macOS/Linux)
# This script starts both backend and frontend in separate terminal windows

echo "🚀 Starting Employee Attendance System..."

# Check if MongoDB is running
if ! pgrep -x "mongod" > /dev/null; then
    echo "⚠️  MongoDB is not running!"
    echo "Starting MongoDB..."
    # Try to start MongoDB
    if command -v brew &> /dev/null; then
        brew services start mongodb-community
    else
        sudo systemctl start mongodb
    fi
    sleep 2
fi

echo "✅ MongoDB is running"

# Start backend in a new terminal
echo "Starting backend..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    osascript <<EOF
    tell application "Terminal"
        do script "cd $(pwd)/backend && source venv/bin/activate && uvicorn server:app --reload --host 0.0.0.0 --port 8001"
        activate
    end tell
EOF
else
    # Linux
    gnome-terminal -- bash -c "cd $(pwd)/backend && source venv/bin/activate && uvicorn server:app --reload --host 0.0.0.0 --port 8001; exec bash"
fi

sleep 3

# Start frontend in a new terminal
echo "Starting frontend..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    osascript <<EOF
    tell application "Terminal"
        do script "cd $(pwd)/frontend && yarn start"
        activate
    end tell
EOF
else
    # Linux
    gnome-terminal -- bash -c "cd $(pwd)/frontend && yarn start; exec bash"
fi

echo ""
echo "✅ Services starting..."
echo "Backend: http://localhost:8001"
echo "Frontend: http://localhost:3000"
echo ""
echo "Please wait for both services to start (~10-30 seconds)"
echo "Then open: http://localhost:3000"
echo ""
