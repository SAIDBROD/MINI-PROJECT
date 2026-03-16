# 🚀 Running Employee Attendance System on VS Code (Local Setup)

## 📋 Prerequisites

Before you start, make sure you have the following installed:

### Required Software
1. **Python 3.11+** - [Download here](https://www.python.org/downloads/)
2. **Node.js 18+** - [Download here](https://nodejs.org/)
3. **MongoDB** - [Download here](https://www.mongodb.com/try/download/community)
4. **Git** - [Download here](https://git-scm.com/downloads)
5. **VS Code** - [Download here](https://code.visualstudio.com/)
6. **Yarn** (optional, can use npm) - Run: `npm install -g yarn`

### VS Code Extensions (Recommended)
- Python (by Microsoft)
- ESLint
- Prettier
- MongoDB for VS Code

---

## 📥 Step 1: Get the Project Files

### Option A: If You Have Access to the Current System

```bash
# Create a folder for your project
mkdir employee-attendance-system
cd employee-attendance-system

# Copy all files from the deployed system
# You'll need to download these files from your current deployment
```

### Option B: Create Project Structure Manually

```bash
# Create the project structure
mkdir employee-attendance-system
cd employee-attendance-system
mkdir backend frontend
```

Then copy all the files from:
- `/app/backend/` → Your local `backend/` folder
- `/app/frontend/` → Your local `frontend/` folder
- `/app/README.md` → Your local root folder

---

## 🔧 Step 2: Backend Setup (FastAPI + Python)

### 2.1 Navigate to Backend Folder
```bash
cd backend
```

### 2.2 Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 2.3 Install Dependencies

**Option 1: If you have requirements.txt**
```bash
pip install -r requirements.txt
```

**Option 2: Install manually**
```bash
pip install fastapi==0.110.1
pip install uvicorn==0.25.0
pip install motor==3.3.1
pip install pymongo==4.5.0
pip install python-dotenv>=1.0.1
pip install opencv-contrib-python
pip install Pillow
pip install reportlab
pip install pydantic>=2.6.4
pip install python-multipart>=0.0.9
```

### 2.4 Install System Dependencies (for OpenCV)

**Windows:**
- OpenCV should work out of the box with pip install

**macOS:**
```bash
brew install cmake
```

**Linux:**
```bash
sudo apt-get update
sudo apt-get install cmake build-essential
```

### 2.5 Create Backend .env File

Create a file named `.env` in the `backend/` folder:

```env
MONGO_URL=mongodb://localhost:27017
DB_NAME=attendance_system
CORS_ORIGINS=http://localhost:3000
```

---

## 🎨 Step 3: Frontend Setup (React)

### 3.1 Navigate to Frontend Folder
```bash
cd ../frontend
```

### 3.2 Install Dependencies

**Using Yarn (Recommended):**
```bash
yarn install
```

**Using NPM:**
```bash
npm install
```

### 3.3 Create Frontend .env File

Create a file named `.env` in the `frontend/` folder:

```env
REACT_APP_BACKEND_URL=http://localhost:8001
```

---

## 💾 Step 4: Setup MongoDB

### 4.1 Install MongoDB

**Windows:**
1. Download MongoDB Community Server
2. Install with default settings
3. MongoDB will start automatically as a service

**macOS:**
```bash
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

**Linux:**
```bash
sudo apt-get install mongodb
sudo systemctl start mongodb
sudo systemctl enable mongodb
```

### 4.2 Verify MongoDB is Running

```bash
# Check if MongoDB is running
mongosh

# Or check the service
# Windows: Check Services app
# macOS/Linux: 
sudo systemctl status mongodb
```

---

## 🏃‍♂️ Step 5: Running the Application

You'll need **TWO terminal windows** in VS Code.

### Terminal 1: Run Backend

```bash
# Activate virtual environment first
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

cd backend
uvicorn server:app --reload --host 0.0.0.0 --port 8001
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8001 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Application startup complete.
```

### Terminal 2: Run Frontend

```bash
cd frontend

# Using Yarn
yarn start

# Using NPM
npm start
```

You should see:
```
Compiled successfully!

You can now view frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.x.x:3000
```

---

## 🌐 Step 6: Access the Application

Open your browser and go to:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8001
- **API Docs**: http://localhost:8001/docs (Swagger UI)

---

## 📁 Project Structure in VS Code

```
employee-attendance-system/
├── backend/
│   ├── venv/                 # Virtual environment (don't commit)
│   ├── server.py            # Main FastAPI application
│   ├── requirements.txt     # Python dependencies
│   └── .env                 # Backend environment variables
├── frontend/
│   ├── node_modules/        # Node packages (don't commit)
│   ├── public/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Dashboard.js
│   │   │   ├── EnrollEmployee.js
│   │   │   ├── LiveAttendance.js
│   │   │   ├── AttendanceReport.js
│   │   │   └── EmployeeManagement.js
│   │   ├── components/
│   │   │   ├── Navigation.js
│   │   │   └── ui/
│   │   ├── App.js
│   │   └── index.js
│   ├── package.json
│   ├── .env                 # Frontend environment variables
│   └── tailwind.config.js
├── README.md
└── LOCAL_SETUP_GUIDE.md
```

---

## 🔍 Step 7: Verify Everything Works

### Test Backend
```bash
# In a new terminal
curl http://localhost:8001/api/
# Should return: {"message":"Employee Attendance System API"}

curl http://localhost:8001/api/stats
# Should return: {"total_employees":0,"today_attendance":0,"system_status":"operational"}
```

### Test Frontend
1. Open http://localhost:3000
2. You should see the Dashboard page
3. Navigation should work between all pages
4. Check browser console for any errors (F12)

---

## 🐛 Common Issues & Solutions

### Issue 1: "Port 8001 already in use"
**Solution:**
```bash
# Find and kill the process using port 8001
# Windows
netstat -ano | findstr :8001
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:8001 | xargs kill -9
```

### Issue 2: "Port 3000 already in use"
**Solution:**
```bash
# The frontend will prompt you to use a different port
# Just press 'Y' to use port 3001 instead
```

### Issue 3: MongoDB connection error
**Solution:**
```bash
# Make sure MongoDB is running
# Windows: Check Services
# macOS: brew services start mongodb-community
# Linux: sudo systemctl start mongodb

# Test connection
mongosh
```

### Issue 4: "Module not found" errors
**Solution:**
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
yarn install
# or
npm install
```

### Issue 5: OpenCV installation fails
**Solution:**
```bash
# Try installing without contrib
pip uninstall opencv-python opencv-contrib-python
pip install opencv-python

# If still fails, install system dependencies first
# macOS
brew install cmake

# Linux
sudo apt-get install cmake build-essential python3-dev
```

### Issue 6: Camera not working
**Solution:**
1. Allow browser camera permissions
2. Use HTTPS or localhost (some browsers require this)
3. Close other apps using the camera
4. Try a different browser

### Issue 7: CORS errors
**Solution:**
Make sure your backend `.env` has:
```env
CORS_ORIGINS=http://localhost:3000
```

And restart the backend server.

---

## 🔄 Development Workflow

### Making Changes

**Backend Changes:**
- Edit `server.py`
- FastAPI will auto-reload (if using `--reload` flag)
- Check terminal for any errors

**Frontend Changes:**
- Edit files in `src/`
- React will auto-reload
- Check browser console for errors

### Debugging in VS Code

**Backend Debugging:**
1. Create `.vscode/launch.json`:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": [
        "server:app",
        "--reload",
        "--host",
        "0.0.0.0",
        "--port",
        "8001"
      ],
      "jinja": true,
      "cwd": "${workspaceFolder}/backend"
    }
  ]
}
```

**Frontend Debugging:**
- Use Chrome DevTools (F12)
- React DevTools extension
- Check Console and Network tabs

---

## 📦 Building for Production

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn server:app --host 0.0.0.0 --port 8001
```

### Frontend
```bash
cd frontend
yarn build
# or
npm run build

# Serve the build folder
npx serve -s build -p 3000
```

---

## 🎯 Quick Start Commands (After Initial Setup)

### Start Development (2 terminals needed)

**Terminal 1 - Backend:**
```bash
cd backend
venv\Scripts\activate    # Windows
source venv/bin/activate # macOS/Linux
uvicorn server:app --reload --host 0.0.0.0 --port 8001
```

**Terminal 2 - Frontend:**
```bash
cd frontend
yarn start
# or
npm start
```

---

## 📝 Environment Variables Reference

### Backend (.env)
```env
MONGO_URL=mongodb://localhost:27017
DB_NAME=attendance_system
CORS_ORIGINS=http://localhost:3000
```

### Frontend (.env)
```env
REACT_APP_BACKEND_URL=http://localhost:8001
```

---

## 🎓 Using the Application Locally

1. **Enroll Employees**
   - Go to http://localhost:3000/enroll
   - Fill in Employee ID and Name
   - Click "Start Camera" (allow camera permissions)
   - Capture 5-6 face images from different angles
   - Click "Enroll Employee"

2. **Mark Attendance**
   - Go to http://localhost:3000/attendance
   - Click "Start Camera"
   - Position your face in front of camera
   - Click "Recognize & Mark Attendance"

3. **View Reports**
   - Go to http://localhost:3000/reports
   - Filter by date or employee
   - Download PDF reports

---

## 🔐 Security Note

For local development:
- The system uses HTTP (not HTTPS)
- CORS is open for localhost
- No authentication is implemented
- This is fine for development/testing
- Add proper security for production deployment

---

## 💡 Tips for VS Code

1. **Install Recommended Extensions:**
   - Python
   - ESLint
   - Prettier - Code formatter
   - MongoDB for VS Code
   - React Native Tools

2. **Use Integrated Terminal:**
   - Press `` Ctrl+` `` to open terminal
   - Split terminal for backend and frontend

3. **Use Git Integration:**
   - Initialize git: `git init`
   - Create `.gitignore`:
   ```
   # Backend
   venv/
   __pycache__/
   *.pyc
   .env

   # Frontend
   node_modules/
   build/
   .env

   # IDE
   .vscode/
   .idea/
   ```

4. **Workspace Settings:**
   Create `.vscode/settings.json`:
   ```json
   {
     "python.defaultInterpreterPath": "${workspaceFolder}/backend/venv/bin/python",
     "editor.formatOnSave": true,
     "editor.codeActionsOnSave": {
       "source.fixAll.eslint": true
     }
   }
   ```

---

## 🆘 Getting Help

If you encounter issues:

1. **Check Logs:**
   - Backend: Check terminal where uvicorn is running
   - Frontend: Check browser console (F12)
   - MongoDB: Check MongoDB logs

2. **Verify Services:**
   ```bash
   # Check if ports are listening
   # Windows
   netstat -ano | findstr "8001 3000 27017"
   
   # macOS/Linux
   lsof -i :8001
   lsof -i :3000
   lsof -i :27017
   ```

3. **Test Individually:**
   - Test backend: http://localhost:8001/api/
   - Test frontend: http://localhost:3000
   - Test MongoDB: `mongosh`

---

## ✅ Success Checklist

- [ ] Python 3.11+ installed
- [ ] Node.js 18+ installed
- [ ] MongoDB installed and running
- [ ] Backend virtual environment created
- [ ] Backend dependencies installed
- [ ] Frontend dependencies installed
- [ ] Both .env files created
- [ ] Backend running on port 8001
- [ ] Frontend running on port 3000
- [ ] Can access http://localhost:3000
- [ ] Camera permissions granted
- [ ] No errors in browser console

---

**You're all set! The Employee Attendance System should now be running on your local VS Code environment.** 🎉

For any issues or questions, refer to the troubleshooting section or check the main README.md file.
