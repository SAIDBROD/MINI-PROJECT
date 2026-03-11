from fastapi import FastAPI, APIRouter, HTTPException, File, UploadFile
from fastapi.responses import FileResponse, StreamingResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
import uuid
from datetime import datetime, timezone, timedelta
import face_recognition
import numpy as np
import base64
import io
from PIL import Image
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import tempfile

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ==================== MODELS ====================

class Employee(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    employee_id: str
    name: str
    face_encodings: List[str] = []  # Base64 encoded face encodings
    enrolled_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class EmployeeCreate(BaseModel):
    employee_id: str
    name: str


class Attendance(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    employee_id: str
    employee_name: str
    date: str  # YYYY-MM-DD format
    in_time: Optional[datetime] = None
    out_time: Optional[datetime] = None
    working_hours: Optional[float] = None
    status: str = "present"  # present, absent, incomplete


class FaceRecognitionRequest(BaseModel):
    image: str  # Base64 encoded image


class AttendanceReport(BaseModel):
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    employee_id: Optional[str] = None


# ==================== UTILITY FUNCTIONS ====================

def encode_face_to_base64(face_encoding: np.ndarray) -> str:
    """Convert numpy face encoding to base64 string"""
    return base64.b64encode(face_encoding.tobytes()).decode('utf-8')


def decode_face_from_base64(encoded_str: str) -> np.ndarray:
    """Convert base64 string back to numpy face encoding"""
    return np.frombuffer(base64.b64decode(encoded_str), dtype=np.float64)


def decode_image_from_base64(image_str: str) -> np.ndarray:
    """Decode base64 image string to numpy array"""
    try:
        # Remove data URL prefix if present
        if ',' in image_str:
            image_str = image_str.split(',')[1]
        
        image_bytes = base64.b64decode(image_str)
        image = Image.open(io.BytesIO(image_bytes))
        return np.array(image)
    except Exception as e:
        logger.error(f"Error decoding image: {e}")
        raise HTTPException(status_code=400, detail="Invalid image format")


def calculate_working_hours(in_time: datetime, out_time: datetime) -> float:
    """Calculate working hours between in_time and out_time"""
    if not in_time or not out_time:
        return 0.0
    
    duration = out_time - in_time
    hours = duration.total_seconds() / 3600
    return round(hours, 2)


def compare_faces_with_encodings(known_encodings: List[np.ndarray], face_encoding: np.ndarray, tolerance=0.6) -> bool:
    """Compare a face encoding with multiple known encodings"""
    if not known_encodings:
        return False
    
    matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=tolerance)
    return any(matches)


# ==================== EMPLOYEE ENDPOINTS ====================

@api_router.post("/employees/enroll", response_model=Employee)
async def enroll_employee(
    employee_id: str = File(...),
    name: str = File(...),
    images: List[UploadFile] = File(...)
):
    """Enroll a new employee with multiple face images"""
    try:
        # Check if employee already exists
        existing = await db.employees.find_one({"employee_id": employee_id})
        if existing:
            raise HTTPException(status_code=400, detail="Employee ID already exists")
        
        face_encodings = []
        
        # Process each uploaded image
        for image_file in images:
            image_bytes = await image_file.read()
            image = Image.open(io.BytesIO(image_bytes))
            image_np = np.array(image)
            
            # Detect and encode faces
            face_locations = face_recognition.face_locations(image_np, model="hog")
            
            if not face_locations:
                logger.warning(f"No face detected in one of the images for {employee_id}")
                continue
            
            # Get face encoding for the first detected face
            encodings = face_recognition.face_encodings(image_np, face_locations)
            if encodings:
                face_encodings.append(encode_face_to_base64(encodings[0]))
        
        if len(face_encodings) < 3:
            raise HTTPException(
                status_code=400, 
                detail=f"Need at least 3 clear face images. Only {len(face_encodings)} valid faces detected."
            )
        
        # Create employee record
        employee = Employee(
            employee_id=employee_id,
            name=name,
            face_encodings=face_encodings
        )
        
        doc = employee.model_dump()
        doc['enrolled_date'] = doc['enrolled_date'].isoformat()
        
        await db.employees.insert_one(doc)
        
        logger.info(f"Employee {name} (ID: {employee_id}) enrolled with {len(face_encodings)} face encodings")
        
        return employee
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error enrolling employee: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/employees", response_model=List[Employee])
async def get_employees():
    """Get all enrolled employees"""
    try:
        employees = await db.employees.find({}, {"_id": 0}).to_list(1000)
        
        for emp in employees:
            if isinstance(emp.get('enrolled_date'), str):
                emp['enrolled_date'] = datetime.fromisoformat(emp['enrolled_date'])
        
        return employees
    except Exception as e:
        logger.error(f"Error fetching employees: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@api_router.delete("/employees/{employee_id}")
async def delete_employee(employee_id: str):
    """Delete an employee"""
    try:
        result = await db.employees.delete_one({"employee_id": employee_id})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Employee not found")
        
        # Also delete attendance records
        await db.attendance.delete_many({"employee_id": employee_id})
        
        logger.info(f"Employee {employee_id} deleted")
        
        return {"message": "Employee deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting employee: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== ATTENDANCE ENDPOINTS ====================

@api_router.post("/attendance/recognize")
async def recognize_and_mark_attendance(request: FaceRecognitionRequest):
    """Recognize face from image and mark attendance"""
    try:
        # Decode image
        image_np = decode_image_from_base64(request.image)
        
        # Detect faces in the image
        face_locations = face_recognition.face_locations(image_np, model="hog")
        
        if not face_locations:
            return {
                "recognized": False,
                "message": "No face detected in the image"
            }
        
        # Get face encodings
        face_encodings = face_recognition.face_encodings(image_np, face_locations)
        
        if not face_encodings:
            return {
                "recognized": False,
                "message": "Could not encode the detected face"
            }
        
        detected_encoding = face_encodings[0]
        
        # Get all employees
        employees = await db.employees.find({}, {"_id": 0}).to_list(1000)
        
        # Try to match with known employees
        matched_employee = None
        
        for employee in employees:
            known_encodings = [decode_face_from_base64(enc) for enc in employee['face_encodings']]
            
            if compare_faces_with_encodings(known_encodings, detected_encoding, tolerance=0.5):
                matched_employee = employee
                break
        
        if not matched_employee:
            return {
                "recognized": False,
                "message": "Face not recognized. Please enroll first."
            }
        
        # Mark attendance
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        current_time = datetime.now(timezone.utc)
        
        # Check if attendance already exists for today
        existing_attendance = await db.attendance.find_one({
            "employee_id": matched_employee['employee_id'],
            "date": today
        })
        
        if existing_attendance:
            # Check if this is an out-time (at least 1 hour after in-time)
            if existing_attendance.get('in_time'):
                in_time = datetime.fromisoformat(existing_attendance['in_time']) if isinstance(existing_attendance['in_time'], str) else existing_attendance['in_time']
                
                time_diff = (current_time - in_time).total_seconds() / 3600  # in hours
                
                if time_diff >= 1 and not existing_attendance.get('out_time'):
                    # Mark out-time
                    out_time = current_time
                    working_hours = calculate_working_hours(in_time, out_time)
                    
                    await db.attendance.update_one(
                        {"id": existing_attendance['id']},
                        {
                            "$set": {
                                "out_time": out_time.isoformat(),
                                "working_hours": working_hours,
                                "status": "present"
                            }
                        }
                    )
                    
                    return {
                        "recognized": True,
                        "employee_id": matched_employee['employee_id'],
                        "employee_name": matched_employee['name'],
                        "action": "out",
                        "time": out_time.isoformat(),
                        "working_hours": working_hours,
                        "message": f"Goodbye {matched_employee['name']}! Out-time marked."
                    }
                else:
                    return {
                        "recognized": True,
                        "employee_id": matched_employee['employee_id'],
                        "employee_name": matched_employee['name'],
                        "action": "duplicate",
                        "message": f"Already marked attendance for today. Please wait at least 1 hour to mark out-time."
                    }
        
        # Mark in-time (new attendance record)
        attendance = Attendance(
            employee_id=matched_employee['employee_id'],
            employee_name=matched_employee['name'],
            date=today,
            in_time=current_time,
            status="incomplete"
        )
        
        doc = attendance.model_dump()
        doc['in_time'] = doc['in_time'].isoformat()
        
        await db.attendance.insert_one(doc)
        
        logger.info(f"Attendance marked for {matched_employee['name']} at {current_time}")
        
        return {
            "recognized": True,
            "employee_id": matched_employee['employee_id'],
            "employee_name": matched_employee['name'],
            "action": "in",
            "time": current_time.isoformat(),
            "message": f"Welcome {matched_employee['name']}! In-time marked."
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error recognizing face: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/attendance/today")
async def get_today_attendance():
    """Get today's attendance records"""
    try:
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        
        attendance_records = await db.attendance.find(
            {"date": today},
            {"_id": 0}
        ).to_list(1000)
        
        # Convert ISO strings to datetime for response
        for record in attendance_records:
            if isinstance(record.get('in_time'), str):
                record['in_time'] = datetime.fromisoformat(record['in_time'])
            if isinstance(record.get('out_time'), str):
                record['out_time'] = datetime.fromisoformat(record['out_time'])
        
        return {
            "date": today,
            "total_employees": len(attendance_records),
            "records": attendance_records
        }
    except Exception as e:
        logger.error(f"Error fetching today's attendance: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/attendance/report")
async def get_attendance_report(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    employee_id: Optional[str] = None
):
    """Get attendance report with optional filters"""
    try:
        query = {}
        
        if employee_id:
            query["employee_id"] = employee_id
        
        if start_date and end_date:
            query["date"] = {"$gte": start_date, "$lte": end_date}
        elif start_date:
            query["date"] = {"$gte": start_date}
        elif end_date:
            query["date"] = {"$lte": end_date}
        
        attendance_records = await db.attendance.find(
            query,
            {"_id": 0}
        ).sort("date", -1).to_list(1000)
        
        # Convert ISO strings to datetime
        for record in attendance_records:
            if isinstance(record.get('in_time'), str):
                record['in_time'] = datetime.fromisoformat(record['in_time'])
            if isinstance(record.get('out_time'), str):
                record['out_time'] = datetime.fromisoformat(record['out_time'])
        
        return {
            "total_records": len(attendance_records),
            "records": attendance_records
        }
    except Exception as e:
        logger.error(f"Error fetching attendance report: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/attendance/report/pdf")
async def download_attendance_report_pdf(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    employee_id: Optional[str] = None
):
    """Download attendance report as PDF"""
    try:
        # Get attendance data
        query = {}
        
        if employee_id:
            query["employee_id"] = employee_id
        
        if start_date and end_date:
            query["date"] = {"$gte": start_date, "$lte": end_date}
        elif start_date:
            query["date"] = {"$gte": start_date}
        elif end_date:
            query["date"] = {"$lte": end_date}
        
        attendance_records = await db.attendance.find(
            query,
            {"_id": 0}
        ).sort("date", -1).to_list(1000)
        
        # Create PDF
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []
        
        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a56db'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#374151'),
            spaceAfter=12,
            alignment=TA_LEFT
        )
        
        # Title
        title = Paragraph("Employee Attendance Report", title_style)
        elements.append(title)
        elements.append(Spacer(1, 12))
        
        # Report details
        report_info = []
        if start_date:
            report_info.append(f"From: {start_date}")
        if end_date:
            report_info.append(f"To: {end_date}")
        if employee_id:
            report_info.append(f"Employee ID: {employee_id}")
        
        if report_info:
            info_text = Paragraph(" | ".join(report_info), styles['Normal'])
            elements.append(info_text)
            elements.append(Spacer(1, 12))
        
        # Generated date
        generated_text = Paragraph(
            f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            styles['Normal']
        )
        elements.append(generated_text)
        elements.append(Spacer(1, 20))
        
        # Table data
        table_data = [
            ['Employee ID', 'Name', 'Date', 'In Time', 'Out Time', 'Hours', 'Status']
        ]
        
        for record in attendance_records:
            in_time_str = ""
            out_time_str = ""
            
            if record.get('in_time'):
                in_time = datetime.fromisoformat(record['in_time']) if isinstance(record['in_time'], str) else record['in_time']
                in_time_str = in_time.strftime('%H:%M')
            
            if record.get('out_time'):
                out_time = datetime.fromisoformat(record['out_time']) if isinstance(record['out_time'], str) else record['out_time']
                out_time_str = out_time.strftime('%H:%M')
            
            hours = str(record.get('working_hours', '-'))
            
            table_data.append([
                record['employee_id'],
                record['employee_name'],
                record['date'],
                in_time_str,
                out_time_str,
                hours,
                record['status']
            ])
        
        # Create table
        table = Table(table_data, colWidths=[1*inch, 1.5*inch, 1*inch, 0.8*inch, 0.8*inch, 0.7*inch, 0.9*inch])
        
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a56db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
        ]))
        
        elements.append(table)
        
        # Build PDF
        doc.build(elements)
        
        buffer.seek(0)
        
        filename = f"attendance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        return StreamingResponse(
            buffer,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
        
    except Exception as e:
        logger.error(f"Error generating PDF report: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/")
async def root():
    return {"message": "Employee Attendance System API"}


@api_router.get("/stats")
async def get_stats():
    """Get system statistics"""
    try:
        total_employees = await db.employees.count_documents({})
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        today_attendance = await db.attendance.count_documents({"date": today})
        
        return {
            "total_employees": total_employees,
            "today_attendance": today_attendance,
            "system_status": "operational"
        }
    except Exception as e:
        logger.error(f"Error fetching stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
