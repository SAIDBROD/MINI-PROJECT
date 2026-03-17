import React, { useState, useRef } from 'react';
import axios from 'axios';
import { Camera, Upload, CheckCircle, X } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { useToast } from '../hooks/use-toast';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const EnrollEmployee = () => {
  const [employeeId, setEmployeeId] = useState('');
  const [name, setName] = useState('');
  const [capturedImages, setCapturedImages] = useState([]);
  const [isCapturing, setIsCapturing] = useState(false);
  const [stream, setStream] = useState(null);
  const [loading, setLoading] = useState(false);
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const { toast } = useToast();

  const startCamera = async () => {
    try {
      const mediaStream = await navigator.mediaDevices.getUserMedia({
        video: { 
          width: { ideal: 1280 },
          height: { ideal: 720 },
          facingMode: "user"
        }
      });
      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream;
        // Force video to play
        try {
          await videoRef.current.play();
        } catch (playError) {
          console.log("Video play error:", playError);
        }
      }
      setStream(mediaStream);
      setIsCapturing(true);
      
      toast({
        title: "Camera Started",
        description: "Camera is now active. Position your face in the frame."
      });
    } catch (error) {
      console.error("Camera error:", error);
      toast({
        title: "Camera Error",
        description: `Unable to access camera: ${error.message}. Please check permissions.`,
        variant: "destructive"
      });
    }
  };

  const stopCamera = () => {
    if (stream) {
      stream.getTracks().forEach(track => track.stop());
      setStream(null);
      setIsCapturing(false);
    }
  };

  const captureImage = () => {
    if (videoRef.current && canvasRef.current) {
      const canvas = canvasRef.current;
      const video = videoRef.current;
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      const ctx = canvas.getContext('2d');
      ctx.drawImage(video, 0, 0);
      const imageDataUrl = canvas.toDataURL('image/jpeg');
      setCapturedImages([...capturedImages, imageDataUrl]);
      
      toast({
        title: "Image Captured",
        description: `${capturedImages.length + 1} of 5 images captured`
      });
    }
  };

  const removeImage = (index) => {
    setCapturedImages(capturedImages.filter((_, i) => i !== index));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!employeeId || !name) {
      toast({
        title: "Validation Error",
        description: "Please fill in all fields",
        variant: "destructive"
      });
      return;
    }

    if (capturedImages.length < 3) {
      toast({
        title: "Insufficient Images",
        description: "Please capture at least 3 face images from different angles",
        variant: "destructive"
      });
      return;
    }

    setLoading(true);

    try {
      const formData = new FormData();
      formData.append('employee_id', employeeId);
      formData.append('name', name);

      // Convert base64 images to blobs
      for (let i = 0; i < capturedImages.length; i++) {
        const response = await fetch(capturedImages[i]);
        const blob = await response.blob();
        formData.append('images', blob, `face_${i}.jpg`);
      }

      await axios.post(`${API}/employees/enroll`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });

      toast({
        title: "Success!",
        description: `Employee ${name} enrolled successfully`
      });

      // Reset form
      setEmployeeId('');
      setName('');
      setCapturedImages([]);
      stopCamera();

    } catch (error) {
      toast({
        title: "Enrollment Failed",
        description: error.response?.data?.detail || "An error occurred during enrollment",
        variant: "destructive"
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6" data-testid="enroll-employee-page">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Enroll New Employee</h1>
        <p className="text-gray-600 mt-2">Register a new employee with face recognition</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Employee Information</CardTitle>
          <CardDescription>Provide employee details and capture face images</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="employeeId">Employee ID</Label>
                <Input
                  id="employeeId"
                  data-testid="employee-id-input"
                  placeholder="Enter employee ID"
                  value={employeeId}
                  onChange={(e) => setEmployeeId(e.target.value)}
                  required
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="name">Full Name</Label>
                <Input
                  id="name"
                  data-testid="employee-name-input"
                  placeholder="Enter full name"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  required
                />
              </div>
            </div>

            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <Label>Face Images ({capturedImages.length}/5)</Label>
                {!isCapturing ? (
                  <Button
                    type="button"
                    onClick={startCamera}
                    data-testid="start-camera-button"
                    className="bg-blue-600 hover:bg-blue-700"
                  >
                    <Camera className="mr-2 h-4 w-4" />
                    Start Camera
                  </Button>
                ) : (
                  <Button
                    type="button"
                    onClick={stopCamera}
                    variant="outline"
                    data-testid="stop-camera-button"
                  >
                    Stop Camera
                  </Button>
                )}
              </div>

              {isCapturing && (
                <div className="space-y-4">
                  <div className="relative bg-black rounded-lg overflow-hidden">
                    <video
                      ref={videoRef}
                      autoPlay
                      playsInline
                      muted
                      className="w-full"
                      data-testid="webcam-video"
                      style={{ minHeight: '400px' }}
                    />
                  </div>
                  <Button
                    type="button"
                    onClick={captureImage}
                    className="w-full"
                    data-testid="capture-image-button"
                    disabled={capturedImages.length >= 5}
                  >
                    <Camera className="mr-2 h-4 w-4" />
                    Capture Image ({capturedImages.length}/5)
                  </Button>
                  <canvas ref={canvasRef} className="hidden" />
                </div>
              )}

              {capturedImages.length > 0 && (
                <div>
                  <Label className="mb-2 block">Captured Images</Label>
                  <div className="grid grid-cols-3 md:grid-cols-5 gap-4">
                    {capturedImages.map((img, index) => (
                      <div key={index} className="relative group" data-testid={`captured-image-${index}`}>
                        <img
                          src={img}
                          alt={`Captured ${index + 1}`}
                          className="w-full h-32 object-cover rounded-lg border-2 border-gray-300"
                        />
                        <button
                          type="button"
                          onClick={() => removeImage(index)}
                          className="absolute top-1 right-1 bg-red-500 text-white rounded-full p-1 opacity-0 group-hover:opacity-100 transition-opacity"
                          data-testid={`remove-image-${index}`}
                        >
                          <X className="h-4 w-4" />
                        </button>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>

            <div className="flex gap-4">
              <Button
                type="submit"
                className="flex-1 bg-green-600 hover:bg-green-700"
                disabled={loading || capturedImages.length < 3}
                data-testid="enroll-submit-button"
              >
                {loading ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                    Enrolling...
                  </>
                ) : (
                  <>
                    <CheckCircle className="mr-2 h-4 w-4" />
                    Enroll Employee
                  </>
                )}
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
};

export default EnrollEmployee;