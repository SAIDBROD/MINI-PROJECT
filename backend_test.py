#!/usr/bin/env python3

import requests
import sys
import json
from datetime import datetime

class AttendanceSystemAPITester:
    def __init__(self, base_url="https://task-manager-461.preview.emergentagent.com/api"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.session = requests.Session()
        
        # Set headers for all requests
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })

    def run_test(self, name, method, endpoint, expected_status, data=None, params=None):
        """Run a single API test"""
        url = f"{self.base_url}{endpoint}"
        
        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = self.session.get(url, params=params)
            elif method == 'POST':
                response = self.session.post(url, json=data, params=params)
            elif method == 'DELETE':
                response = self.session.delete(url)

            print(f"   Status Code: {response.status_code}")
            
            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ PASSED - Status: {response.status_code}")
                
                # Try to parse JSON response
                try:
                    json_response = response.json()
                    print(f"   Response: {json.dumps(json_response, indent=2)}")
                    return True, json_response
                except:
                    print(f"   Response (text): {response.text[:200]}...")
                    return True, response.text
            else:
                print(f"❌ FAILED - Expected {expected_status}, got {response.status_code}")
                print(f"   Response: {response.text[:200]}...")
                return False, {}

        except Exception as e:
            print(f"❌ FAILED - Error: {str(e)}")
            return False, {}

    def test_system_status(self):
        """Test basic system endpoints"""
        print("\n" + "="*50)
        print("TESTING SYSTEM STATUS ENDPOINTS")
        print("="*50)
        
        # Test root endpoint
        success, response = self.run_test(
            "Root Endpoint",
            "GET",
            "/",
            200
        )
        
        if success and isinstance(response, dict):
            expected_message = "Employee Attendance System API"
            if response.get('message') == expected_message:
                print(f"✅ Root endpoint message correct: {response.get('message')}")
            else:
                print(f"⚠️  Root endpoint message unexpected: {response.get('message')}")
        
        # Test stats endpoint
        success, response = self.run_test(
            "System Stats",
            "GET",
            "/stats",
            200
        )
        
        if success and isinstance(response, dict):
            required_fields = ['total_employees', 'today_attendance', 'system_status']
            missing_fields = [field for field in required_fields if field not in response]
            
            if not missing_fields:
                print(f"✅ Stats endpoint has all required fields")
                print(f"   Total Employees: {response.get('total_employees')}")
                print(f"   Today Attendance: {response.get('today_attendance')}")
                print(f"   System Status: {response.get('system_status')}")
            else:
                print(f"⚠️  Stats endpoint missing fields: {missing_fields}")

    def test_employee_endpoints(self):
        """Test employee management endpoints"""
        print("\n" + "="*50)
        print("TESTING EMPLOYEE ENDPOINTS")
        print("="*50)
        
        # Test get employees (should be empty initially)
        success, response = self.run_test(
            "Get All Employees",
            "GET",
            "/employees",
            200
        )
        
        if success:
            if isinstance(response, list):
                print(f"✅ Employees endpoint returns array with {len(response)} employees")
            else:
                print(f"⚠️  Employees endpoint should return array, got: {type(response)}")

    def test_attendance_endpoints(self):
        """Test attendance endpoints"""
        print("\n" + "="*50)
        print("TESTING ATTENDANCE ENDPOINTS")
        print("="*50)
        
        # Test today's attendance
        success, response = self.run_test(
            "Today's Attendance",
            "GET",
            "/attendance/today",
            200
        )
        
        if success and isinstance(response, dict):
            required_fields = ['date', 'total_employees', 'records']
            missing_fields = [field for field in required_fields if field not in response]
            
            if not missing_fields:
                print(f"✅ Today's attendance has all required fields")
                print(f"   Date: {response.get('date')}")
                print(f"   Total Employees: {response.get('total_employees')}")
                print(f"   Records Count: {len(response.get('records', []))}")
                
                # Validate date format
                try:
                    datetime.strptime(response.get('date'), '%Y-%m-%d')
                    print(f"✅ Date format is correct")
                except:
                    print(f"⚠️  Date format is incorrect: {response.get('date')}")
            else:
                print(f"⚠️  Today's attendance missing fields: {missing_fields}")
        
        # Test attendance report
        success, response = self.run_test(
            "Attendance Report",
            "GET",
            "/attendance/report",
            200
        )
        
        if success and isinstance(response, dict):
            required_fields = ['total_records', 'records']
            missing_fields = [field for field in required_fields if field not in response]
            
            if not missing_fields:
                print(f"✅ Attendance report has all required fields")
                print(f"   Total Records: {response.get('total_records')}")
                print(f"   Records Count: {len(response.get('records', []))}")
            else:
                print(f"⚠️  Attendance report missing fields: {missing_fields}")
        
        # Test attendance report with filters
        success, response = self.run_test(
            "Attendance Report with Date Filter",
            "GET",
            "/attendance/report",
            200,
            params={'start_date': '2024-01-01', 'end_date': '2024-12-31'}
        )
        
        if success:
            print(f"✅ Attendance report with filters works")

    def test_cors_headers(self):
        """Test CORS headers are present"""
        print("\n" + "="*50)
        print("TESTING CORS HEADERS")
        print("="*50)
        
        try:
            response = self.session.options(f"{self.base_url}/")
            print(f"OPTIONS request status: {response.status_code}")
            
            cors_headers = [
                'Access-Control-Allow-Origin',
                'Access-Control-Allow-Methods',
                'Access-Control-Allow-Headers'
            ]
            
            present_headers = []
            for header in cors_headers:
                if header in response.headers:
                    present_headers.append(header)
                    print(f"✅ {header}: {response.headers[header]}")
                else:
                    print(f"⚠️  Missing CORS header: {header}")
            
            if len(present_headers) >= 1:
                print(f"✅ CORS headers are configured")
            else:
                print(f"⚠️  CORS may not be properly configured")
                
        except Exception as e:
            print(f"⚠️  Could not test CORS: {str(e)}")

    def test_error_handling(self):
        """Test error handling for invalid endpoints"""
        print("\n" + "="*50)
        print("TESTING ERROR HANDLING")
        print("="*50)
        
        # Test non-existent endpoint
        success, response = self.run_test(
            "Non-existent Endpoint",
            "GET",
            "/nonexistent",
            404
        )
        
        if success:
            print(f"✅ 404 error handling works correctly")

    def run_all_tests(self):
        """Run all API tests"""
        print("🚀 Starting Employee Attendance System API Tests")
        print(f"🌐 Base URL: {self.base_url}")
        print(f"🕒 Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Run all test suites
        self.test_system_status()
        self.test_employee_endpoints()
        self.test_attendance_endpoints()
        self.test_cors_headers()
        self.test_error_handling()
        
        # Print final results
        print("\n" + "="*60)
        print("FINAL TEST RESULTS")
        print("="*60)
        print(f"📊 Tests Run: {self.tests_run}")
        print(f"✅ Tests Passed: {self.tests_passed}")
        print(f"❌ Tests Failed: {self.tests_run - self.tests_passed}")
        print(f"📈 Success Rate: {(self.tests_passed/self.tests_run)*100:.1f}%")
        
        if self.tests_passed == self.tests_run:
            print("\n🎉 ALL TESTS PASSED! Backend API is working correctly.")
            return 0
        else:
            print(f"\n⚠️  {self.tests_run - self.tests_passed} tests failed. Please check the issues above.")
            return 1

def main():
    """Main function to run tests"""
    tester = AttendanceSystemAPITester()
    return tester.run_all_tests()

if __name__ == "__main__":
    sys.exit(main())