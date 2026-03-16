# 🎯 Quick Start Guide - VS Code Setup

This guide will help you run the Employee Attendance System on your local machine using VS Code.

## 📦 What You'll Get

After following this guide, you'll have:
- ✅ Backend API running on http://localhost:8001
- ✅ Frontend app running on http://localhost:3000  
- ✅ MongoDB database running locally
- ✅ Full face recognition attendance system working on your machine

---

## 🚀 Method 1: Automated Setup (Easiest)

### For Windows:

1. **Download all project files** to a folder (e.g., `C:\employee-attendance-system\`)

2. **Run the setup script:**
   - Double-click `setup-local.bat`
   - OR open Command Prompt and run:
     ```cmd
     cd C:\employee-attendance-system
     setup-local.bat
     ```

3. **Start the application:**
   - Open **TWO Command Prompt** windows
   
   **Window 1 - Backend:**
   ```cmd
   cd backend
   venv\Scripts\activate
   uvicorn server:app --reload --host 0.0.0.0 --port 8001
   ```
   
   **Window 2 - Frontend:**
   ```cmd
   cd frontend
   yarn start
   ```
   (or `npm start` if you don't have yarn)

4. **Open browser:** http://localhost:3000

---

### For macOS/Linux:

1. **Download all project files** to a folder (e.g., `~/employee-attendance-system/`)

2. **Run the setup script:**
   ```bash
   cd ~/employee-attendance-system
   chmod +x setup-local.sh
   ./setup-local.sh
   ```

3. **Start the application:**
   ```bash
   # This will open two terminal windows automatically
   chmod +x start-dev.sh
   ./start-dev.sh
   ```

4. **Open browser:** http://localhost:3000

---

## 🔧 Method 2: Manual Setup (Step by Step)

### Prerequisites Installation

1. **Python 3.11+**
   - Download: https://www.python.org/downloads/
   - Verify: `python --version` or `python3 --version`

2. **Node.js 18+**
   - Download: https://nodejs.org/
   - Verify: `node --version`

3. **MongoDB Community Edition**
   - Download: https://www.mongodb.com/try/download/community
   - Windows: Install as a service (it will auto-start)
   - macOS: `brew install mongodb-community && brew services start mongodb-community`
   - Linux: `sudo apt-get install mongodb && sudo systemctl start mongodb`

4. **VS Code** (optional but recommended)
   - Download: https://code.visualstudio.com/

---

### Backend Setup

```bash
# Navigate to backend folder
cd backend

# Create virtual environment
# Windows:
python -m venv venv
venv\Scripts\activate

# macOS/Linux:
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
# Copy this content into backend/.env:
MONGO_URL=mongodb://localhost:27017
DB_NAME=attendance_system
CORS_ORIGINS=http://localhost:3000

# Start backend
uvicorn server:app --reload --host 0.0.0.0 --port 8001
```

---

### Frontend Setup

```bash
# Open a NEW terminal
# Navigate to frontend folder
cd frontend

# Install dependencies
yarn install
# OR
npm install

# Create .env file
# Copy this content into frontend/.env:
REACT_APP_BACKEND_URL=http://localhost:8001

# Start frontend
yarn start
# OR
npm start
```

---

## 📂 How to Get the Files

### Option 1: Download from Deployment

If you have access to the deployed system, download these files:

**Backend files:**
- `/app/backend/server.py`
- `/app/backend/requirements.txt`
- `/app/backend/.env` (create with the content above)

**Frontend files:**
- Everything in `/app/frontend/` folder
- `/app/frontend/.env` (create with the content above)

**Root files:**
- `/app/README.md`
- `/app/LOCAL_SETUP_GUIDE.md`
- `/app/setup-local.sh` (macOS/Linux)
- `/app/setup-local.bat` (Windows)
- `/app/.gitignore`

### Option 2: Use Git (if connected)

```bash
# If your system has git initialized
git clone <your-repository-url>
cd employee-attendance-system
```

---

## 🎮 Using the Application

### 1️⃣ Enroll an Employee

1. Go to http://localhost:3000/enroll
2. Fill in:
   - Employee ID: `EMP001`
   - Name: `Your Name`
3. Click "Start Camera"
4. Allow camera permissions
5. Capture 5-6 face images from different angles:
   - Front view
   - Turn head left slightly
   - Turn head right slightly
   - Look up slightly
   - Look down slightly
6. Click "Enroll Employee"

### 2️⃣ Mark Attendance

1. Go to http://localhost:3000/attendance
2. Click "Start Camera"
3. Position your face in front of the camera
4. Click "Recognize & Mark Attendance"
5. System will mark your In-Time
6. Wait 1+ hour and repeat to mark Out-Time

### 3️⃣ View Reports

1. Go to http://localhost:3000/reports
2. Filter by dates or employee ID
3. Click "Download PDF" to get a report

---

## 🔍 Verify Everything Works

### Check Backend
```bash
# Open a browser or use curl
curl http://localhost:8001/api/
# Should return: {"message":"Employee Attendance System API"}

# Check stats
curl http://localhost:8001/api/stats
# Should return: {"total_employees":0,"today_attendance":0,"system_status":"operational"}
```

### Check Frontend
1. Open http://localhost:3000
2. You should see the Dashboard
3. Navigate between pages using the top navigation
4. No errors in browser console (press F12)

### Check MongoDB
```bash
# Open MongoDB shell
mongosh

# Check databases
show dbs

# Use the attendance database
use attendance_system

# Check collections (after enrolling an employee)
show collections
db.employees.find()
```

---

## 🐛 Common Issues

### ❌ "Port already in use"
**Solution:**
```bash
# Kill process on port 8001 or 3000
# Windows:
netstat -ano | findstr :8001
taskkill /PID <PID> /F

# macOS/Linux:
lsof -ti:8001 | xargs kill -9
```

### ❌ "MongoDB connection error"
**Solution:**
```bash
# Windows: Check Services app, start MongoDB
# macOS: brew services start mongodb-community
# Linux: sudo systemctl start mongodb
```

### ❌ Camera not working
**Solution:**
1. Allow browser camera permissions
2. Close other apps using camera (Zoom, Teams, etc.)
3. Use Chrome or Edge (best support)
4. Use http://localhost (not HTTPS)

### ❌ "Module not found" errors
**Solution:**
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
rm -rf node_modules
yarn install
```

---

## 🎓 VS Code Tips

### Recommended Extensions:
1. **Python** (by Microsoft)
2. **ESLint**
3. **Prettier - Code formatter**
4. **MongoDB for VS Code**

### Using Integrated Terminal:
1. Press `` Ctrl+` `` (or `` Cmd+` `` on Mac)
2. Click the "+" to open new terminal
3. Run backend in one, frontend in another

### Split Terminal View:
1. Click the split icon in terminal
2. Run backend in left pane
3. Run frontend in right pane

---

## 📁 Project Structure

```
employee-attendance-system/
├── backend/                    # FastAPI Backend
│   ├── venv/                  # Virtual environment
│   ├── server.py              # Main application
│   ├── requirements.txt       # Python packages
│   └── .env                   # Environment config
│
├── frontend/                  # React Frontend
│   ├── src/
│   │   ├── pages/            # All pages
│   │   ├── components/       # Reusable components
│   │   └── App.js           # Main app
│   ├── package.json          # Node packages
│   └── .env                  # Environment config
│
├── README.md                  # Main documentation
├── LOCAL_SETUP_GUIDE.md      # Detailed setup guide
├── QUICK_START.md            # This file
├── setup-local.sh            # Setup script (Mac/Linux)
├── setup-local.bat           # Setup script (Windows)
└── .gitignore                # Git ignore rules
```

---

## 🎯 Quick Commands Reference

### Backend Commands
```bash
# Activate virtual environment
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

# Install packages
pip install -r requirements.txt

# Run server
uvicorn server:app --reload --host 0.0.0.0 --port 8001

# Run with auto-reload (development)
uvicorn server:app --reload

# Deactivate virtual environment
deactivate
```

### Frontend Commands
```bash
# Install packages
yarn install
# or: npm install

# Start development server
yarn start
# or: npm start

# Build for production
yarn build
# or: npm run build
```

### MongoDB Commands
```bash
# Start MongoDB
# Windows: Check Services
# Mac: brew services start mongodb-community
# Linux: sudo systemctl start mongodb

# Open MongoDB shell
mongosh

# Show databases
show dbs

# Use database
use attendance_system

# Show collections
show collections

# Query data
db.employees.find()
db.attendance.find()
```

---

## ✅ Success Checklist

Before starting, make sure you have:
- [ ] Downloaded all project files
- [ ] Python 3.11+ installed
- [ ] Node.js 18+ installed
- [ ] MongoDB installed and running
- [ ] Created backend/.env file
- [ ] Created frontend/.env file
- [ ] Installed backend dependencies
- [ ] Installed frontend dependencies

When running:
- [ ] Backend shows "Application startup complete"
- [ ] Frontend shows "Compiled successfully"
- [ ] Can open http://localhost:3000
- [ ] Dashboard page loads
- [ ] Navigation works
- [ ] Camera button appears on enrollment page

---

## 🎉 You're Ready!

Once everything is running:
1. Go to http://localhost:3000
2. Click "Enroll Employee" in the navigation
3. Start enrolling employees and marking attendance!

For detailed information, see:
- **README.md** - Complete system documentation
- **LOCAL_SETUP_GUIDE.md** - Detailed setup instructions

---

## 📞 Need Help?

### Check Logs
- **Backend**: Look at the terminal where uvicorn is running
- **Frontend**: Check browser console (F12)
- **MongoDB**: Run `mongosh` to test connection

### Test Services
```bash
# Backend
curl http://localhost:8001/api/

# MongoDB
mongosh
```

### Restart Everything
```bash
# Stop all services (Ctrl+C in terminals)
# Start MongoDB
# Start backend
# Start frontend
```

---

**Happy Coding! 🚀**

The Employee Attendance System is now running on your local machine with full face recognition capabilities!
