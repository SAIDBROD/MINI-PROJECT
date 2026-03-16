import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import EnrollEmployee from './pages/EnrollEmployee';
import LiveAttendance from './pages/LiveAttendance';
import AttendanceReport from './pages/AttendanceReport';
import EmployeeManagement from './pages/EmployeeManagement';
import Navigation from './components/Navigation';
import { Toaster } from './components/ui/toaster';
import './App.css';

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-50">
        <Navigation />
        <main className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/enroll" element={<EnrollEmployee />} />
            <Route path="/attendance" element={<LiveAttendance />} />
            <Route path="/reports" element={<AttendanceReport />} />
            <Route path="/employees" element={<EmployeeManagement />} />
          </Routes>
        </main>
        <Toaster />
      </div>
    </BrowserRouter>
  );
}

export default App;