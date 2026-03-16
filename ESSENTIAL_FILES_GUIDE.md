# 🚀 ESSENTIAL FILES - Quick Download Guide

## ✅ MINIMUM FILES TO DOWNLOAD (Only what you NEED)

### Total: 20 files minimum to run locally

---

## 📥 DOWNLOAD THESE FILES

### 1. Backend (3 files)
```
backend/server.py                     ← Get from: /app/backend/server.py
backend/requirements.txt              ← Use minimal version below
backend/.env                          ← CREATE with template below
```

### 2. Frontend Core (8 files)
```
frontend/package.json                 ← Use minimal version below
frontend/tailwind.config.js           ← Get from: /app/frontend/tailwind.config.js
frontend/postcss.config.js            ← Simple config below
frontend/.env                         ← CREATE with template below
frontend/public/index.html            ← Simple HTML below
frontend/src/index.js                 ← Get from: /app/frontend/src/index.js
frontend/src/index.css                ← Get from: /app/frontend/src/index.css
frontend/src/App.js                   ← Get from: /app/frontend/src/App.js
```

### 3. Pages (5 files)
```
frontend/src/pages/Dashboard.js
frontend/src/pages/EnrollEmployee.js
frontend/src/pages/LiveAttendance.js
frontend/src/pages/AttendanceReport.js
frontend/src/pages/EmployeeManagement.js
```

### 4. Components & UI (4 files minimum)
```
frontend/src/components/Navigation.js
frontend/src/components/ui/button.jsx
frontend/src/components/ui/card.jsx
frontend/src/components/ui/input.jsx
+ Copy ALL files from /app/frontend/src/components/ui/
```

---

## 📝 FILES TO CREATE (Copy-Paste)

### backend/.env
```
MONGO_URL=mongodb://localhost:27017
DB_NAME=attendance_system
CORS_ORIGINS=http://localhost:3000
```

### backend/requirements.txt (MINIMAL)
```
fastapi==0.110.1
uvicorn==0.25.0
motor==3.3.1
pymongo==4.5.0
python-dotenv>=1.0.1
opencv-contrib-python==4.13.0.92
Pillow>=12.1.1
reportlab==4.4.10
pydantic>=2.6.4
python-multipart>=0.0.9
numpy>=2.4.2
```

### frontend/.env
```
REACT_APP_BACKEND_URL=http://localhost:8001
```

### frontend/postcss.config.js
```javascript
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
```

---

## 🚀 HOW TO RUN LOCALLY (5 Steps)

### Step 1: Download Files
Download all files listed above from /app/ directory

### Step 2: Setup Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Mac/Linux
# or: venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### Step 3: Setup Frontend
```bash
cd frontend
npm install  # or: yarn install
```

### Step 4: Start MongoDB
```bash
# Mac: brew services start mongodb-community
# Windows: Start MongoDB service
# Linux: sudo systemctl start mongodb
```

### Step 5: Run the App
**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
uvicorn server:app --reload --host 0.0.0.0 --port 8001
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

**Open:** http://localhost:3000

---

## 📂 WHERE TO GET FILES

All files are in: `/app/`

**Backend:**
- `/app/backend/server.py` (704 lines)
- `/app/backend/requirements.txt`

**Frontend:**
- `/app/frontend/src/` (all source files)
- `/app/frontend/package.json`
- `/app/frontend/tailwind.config.js`

---

## ⚡ FASTEST METHOD

### Option A: Download from Emergent
Use Emergent's "Export Project" or "Download" button

### Option B: Copy-Paste Individual Files
I can show you any file content - just ask!

### Option C: Use the file browser
Navigate to /app/ and copy files one by one

---

## 💡 NEED HELP?

Ask me:
- "Show me server.py" ← I'll display full file
- "Show me Dashboard.js" ← I'll show page content
- "Show me all UI components" ← I'll list them

---

## ✅ SUCCESS CHECKLIST

After download, verify:
- [ ] backend/server.py exists (704 lines)
- [ ] backend/.env created
- [ ] All 5 frontend pages downloaded
- [ ] frontend/.env created
- [ ] Python 3.11+ installed
- [ ] Node.js 18+ installed
- [ ] MongoDB installed

Then run: Backend → Frontend → Open browser!

