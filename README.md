# Employee Activity Attendance and Monitoring System

## 📋 Overview

An AI-powered face recognition-based attendance system that automates employee attendance tracking using computer vision and deep learning. The system provides contactless, accurate, and real-time attendance monitoring with automatic working hours calculation.

## ✨ Key Features

### Core Functionality
- **Face Recognition Based Attendance**: Contactless attendance marking using AI
- **Automatic Time Tracking**: 
  - First detection → In-time marking
  - Second detection (after 1+ hour) → Out-time marking
  - Automatic working hours calculation
- **Multi-Angle Face Enrollment**: Capture 5-6 face images from different angles for better accuracy
- **Real-Time Recognition**: Live camera feed with instant face recognition
- **Proxy Prevention**: Only registered faces are recognized
- **Duplicate Entry Prevention**: Smart logic to prevent multiple check-ins

### Dashboard & Reports
- **Real-Time Dashboard**: View today's attendance and system statistics
- **Attendance Reports**: Filter by date range or employee
- **PDF Export**: Download professional PDF reports
- **Employee Management**: View and manage enrolled employees

## 🏗️ Technical Architecture

### Backend (FastAPI + Python)
- **Framework**: FastAPI 0.110.1
- **Face Detection**: OpenCV Haar Cascade Classifier
- **Face Recognition**: OpenCV LBPH (Local Binary Patterns Histograms)
- **Database**: MongoDB (Motor async driver)
- **PDF Generation**: ReportLab
- **Image Processing**: OpenCV, Pillow, NumPy

### Frontend (React)
- **Framework**: React 19.0.0
- **Routing**: React Router DOM 7.5.1
- **UI Components**: Radix UI with Tailwind CSS
- **HTTP Client**: Axios
- **Webcam**: Browser MediaDevices API

### Face Recognition Approach
The system uses a hybrid approach combining multiple computer vision techniques:
1. **Face Detection**: Haar Cascade for real-time face detection
2. **Face Extraction**: Normalized 200x200 grayscale face images
3. **Face Comparison**: 
   - Template Matching (TM_CCOEFF_NORMED)
   - Histogram Comparison (HISTCMP_CORREL)
   - Combined weighted score for accuracy

## 📁 Project Structure

```
/app/
├── backend/
│   ├── server.py              # Main FastAPI application
│   ├── requirements.txt       # Python dependencies
│   └── .env                   # Environment variables
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Dashboard.js           # Main dashboard
│   │   │   ├── EnrollEmployee.js      # Employee enrollment
│   │   │   ├── LiveAttendance.js      # Live attendance marking
│   │   │   ├── AttendanceReport.js    # Reports page
│   │   │   └── EmployeeManagement.js  # Employee management
│   │   ├── components/
│   │   │   ├── Navigation.js          # Navigation bar
│   │   │   └── ui/                    # Reusable UI components
│   │   ├── App.js                     # Main App component
│   │   └── index.js                   # Entry point
│   ├── package.json
│   └── .env                   # Frontend environment variables
└── README.md
```

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Node.js 20+
- MongoDB
- Webcam/Camera access

### Installation

1. **Backend Setup**
```bash
cd /app/backend
pip install -r requirements.txt
```

2. **Frontend Setup**
```bash
cd /app/frontend
yarn install
```

### Running the Application

The application uses supervisor to manage services:

```bash
# Start all services
sudo supervisorctl start all

# Check status
sudo supervisorctl status

# Restart individual services
sudo supervisorctl restart backend
sudo supervisorctl restart frontend
```

### Access the Application

- **Frontend**: https://task-manager-461.preview.emergentagent.com
- **Backend API**: https://task-manager-461.preview.emergentagent.com/api
- **API Documentation**: https://task-manager-461.preview.emergentagent.com/api/docs

## 📖 Usage Guide

### 1. Enroll Employees

1. Navigate to **"Enroll Employee"** page
2. Enter Employee ID and Full Name
3. Click **"Start Camera"**
4. Capture **5-6 face images** from different angles:
   - Front view
   - Left side (30° angle)
   - Right side (30° angle)
   - Slightly up
   - Slightly down
5. Review captured images
6. Click **"Enroll Employee"** to complete registration

**Note**: At least 3 clear face images are required for enrollment.

### 2. Mark Attendance

1. Navigate to **"Mark Attendance"** page
2. Click **"Start Camera"**
3. Position your face in front of the camera
4. Click **"Recognize & Mark Attendance"**
5. System will:
   - Detect and recognize your face
   - Mark **In-Time** (first detection of the day)
   - Mark **Out-Time** (second detection after 1+ hour)
   - Calculate working hours automatically

### 3. View Dashboard

- Real-time attendance statistics
- Today's attendance records
- System status

### 4. Generate Reports

1. Navigate to **"Reports"** page
2. Apply filters (optional):
   - Start Date
   - End Date
   - Employee ID
3. Click **"Apply Filter"** to view records
4. Click **"Download PDF"** to export report

### 5. Manage Employees

- Navigate to **"Employees"** page
- View all enrolled employees
- Delete employees (removes all attendance records)

## 🔧 API Endpoints

### Employee Management
- `POST /api/employees/enroll` - Enroll new employee with face images
- `GET /api/employees` - Get all employees
- `DELETE /api/employees/{employee_id}` - Delete employee

### Attendance
- `POST /api/attendance/recognize` - Recognize face and mark attendance
- `GET /api/attendance/today` - Get today's attendance records
- `GET /api/attendance/report` - Get attendance report (with filters)
- `GET /api/attendance/report/pdf` - Download PDF report

### System
- `GET /api/` - API status
- `GET /api/stats` - System statistics

## 🎯 Attendance Logic

### In-Time Marking
- First face recognition of the day
- Marks as "incomplete" status
- Records timestamp

### Out-Time Marking
- Second recognition after **minimum 1 hour** gap
- Updates status to "present"
- Calculates working hours
- Records out timestamp

### Working Hours Calculation
```
Working Hours = (Out Time - In Time) / 3600 seconds
```

## 🔒 Security Features

- No face encoding data exposed in API responses
- Input validation on all endpoints
- Unknown faces are ignored and logged
- Secure face comparison with confidence threshold

## 🎨 UI Components

Built with modern, accessible components:
- **Dashboard Cards**: Real-time statistics
- **Camera Feed**: Live video preview with overlay
- **Data Tables**: Sortable, filterable attendance records
- **Responsive Design**: Works on desktop and mobile
- **Toast Notifications**: Real-time feedback
- **Loading States**: Clear visual indicators

## 📊 Database Schema

### Employees Collection
```json
{
  "id": "uuid",
  "employee_id": "string",
  "name": "string",
  "face_encodings": ["base64_image_1", "base64_image_2", ...],
  "enrolled_date": "ISO datetime"
}
```

### Attendance Collection
```json
{
  "id": "uuid",
  "employee_id": "string",
  "employee_name": "string",
  "date": "YYYY-MM-DD",
  "in_time": "ISO datetime",
  "out_time": "ISO datetime",
  "working_hours": "float",
  "status": "present|incomplete"
}
```

## 🐛 Troubleshooting

### Camera Not Working
- Check browser permissions for camera access
- Ensure no other application is using the camera
- Try refreshing the page

### Face Not Recognized
- Ensure good lighting conditions
- Face camera directly
- Make sure you're enrolled in the system
- Try re-enrolling with better quality images

### Backend Not Responding
```bash
# Check backend logs
tail -f /var/log/supervisor/backend.*.log

# Restart backend
sudo supervisorctl restart backend
```

### Frontend Not Loading
```bash
# Check frontend logs
tail -f /var/log/supervisor/frontend.*.log

# Restart frontend
sudo supervisorctl restart frontend
```

## 📝 Environment Variables

### Backend (.env)
```env
MONGO_URL=mongodb://localhost:27017
DB_NAME=test_database
CORS_ORIGINS=*
```

### Frontend (.env)
```env
REACT_APP_BACKEND_URL=https://task-manager-461.preview.emergentagent.com
```

## 🔄 Technology Stack Summary

| Component | Technology | Version |
|-----------|-----------|---------|
| Backend Framework | FastAPI | 0.110.1 |
| Face Detection | OpenCV | 4.13.0.92 |
| Frontend | React | 19.0.0 |
| Database | MongoDB | 7.0 |
| UI Library | Radix UI | Latest |
| Styling | Tailwind CSS | 3.4.17 |
| PDF Generation | ReportLab | 4.4.10 |

## 🎓 Key Algorithms

### Face Detection
- **Algorithm**: Haar Cascade Classifier
- **Parameters**: scaleFactor=1.1, minNeighbors=5, minSize=(100,100)

### Face Recognition
- **Primary**: Template Matching (TM_CCOEFF_NORMED)
- **Secondary**: Histogram Comparison (HISTCMP_CORREL)
- **Confidence Threshold**: 0.55 (combined score)

### Working Hours
- **Minimum Gap**: 1 hour between in-time and out-time
- **Calculation**: Precise to 2 decimal places

## 🌟 Future Enhancements

- [ ] Multi-face detection in single frame
- [ ] Advanced deep learning models (FaceNet, ArcFace)
- [ ] Mobile app integration
- [ ] Email/SMS notifications
- [ ] Attendance analytics and insights
- [ ] Department-wise filtering
- [ ] Shift management
- [ ] Leave management integration

## 📄 License

This project is built for demonstration and educational purposes.

## 👥 Authors

Developed as part of the Employee Activity Attendance and Monitoring System project based on research and specifications provided.

---

**Note**: This system uses computer vision and machine learning for face recognition. Accuracy may vary based on lighting conditions, camera quality, and enrollment image quality. Always ensure proper lighting and camera positioning for best results.
