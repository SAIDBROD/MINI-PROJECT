import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { Camera, UserCheck, AlertCircle } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { useToast } from '../hooks/use-toast';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const LiveAttendance = () => {
  const [isCapturing, setIsCapturing] = useState(false);
  const [stream, setStream] = useState(null);
  const [processing, setProcessing] = useState(false);
  const [lastRecognition, setLastRecognition] = useState(null);
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
        description: "Camera is active. Click 'Recognize & Mark Attendance' when ready."
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

  useEffect(() => {
    return () => {
      stopCamera();
    };
  }, []);

  const recognizeAndMark = async () => {
    if (!videoRef.current || !canvasRef.current) return;

    setProcessing(true);

    try {
      const canvas = canvasRef.current;
      const video = videoRef.current;
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      const ctx = canvas.getContext('2d');
      ctx.drawImage(video, 0, 0);
      const imageDataUrl = canvas.toDataURL('image/jpeg');

      const response = await axios.post(`${API}/attendance/recognize`, {
        image: imageDataUrl
      });

      const result = response.data;

      if (result.recognized) {
        setLastRecognition(result);
        
        if (result.action === 'in') {
          toast({
            title: "✅ In-Time Marked",
            description: result.message,
            className: "bg-green-50 border-green-200"
          });
        } else if (result.action === 'out') {
          toast({
            title: "✅ Out-Time Marked",
            description: `${result.message} Working hours: ${result.working_hours}`,
            className: "bg-blue-50 border-blue-200"
          });
        } else {
          toast({
            title: "ℹ️ Already Marked",
            description: result.message,
            className: "bg-yellow-50 border-yellow-200"
          });
        }
      } else {
        toast({
          title: "❌ Not Recognized",
          description: result.message,
          variant: "destructive"
        });
      }

    } catch (error) {
      toast({
        title: "Error",
        description: error.response?.data?.detail || "An error occurred during recognition",
        variant: "destructive"
      });
    } finally {
      setProcessing(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6" data-testid="live-attendance-page">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Mark Attendance</h1>
        <p className="text-gray-600 mt-2">Use face recognition to mark attendance</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle>Camera Feed</CardTitle>
            <CardDescription>Position your face in the camera for recognition</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {!isCapturing ? (
              <div className="bg-gray-100 rounded-lg p-12 text-center">
                <Camera className="h-16 w-16 mx-auto mb-4 text-gray-400" />
                <p className="text-gray-600 mb-4">Camera is not active</p>
                <Button
                  onClick={startCamera}
                  className="bg-blue-600 hover:bg-blue-700"
                  data-testid="start-camera-button"
                >
                  <Camera className="mr-2 h-4 w-4" />
                  Start Camera
                </Button>
              </div>
            ) : (
              <div className="space-y-4">
                <div className="relative bg-black rounded-lg overflow-hidden">
                  <video
                    ref={videoRef}
                    autoPlay
                    playsInline
                    muted
                    className="w-full"
                    data-testid="attendance-webcam-video"
                    style={{ minHeight: '400px' }}
                  />
                  <div className="absolute top-0 left-0 right-0 bottom-0 border-4 border-blue-500 pointer-events-none opacity-50"></div>
                </div>
                <div className="flex gap-4">
                  <Button
                    onClick={recognizeAndMark}
                    disabled={processing}
                    className="flex-1 bg-green-600 hover:bg-green-700"
                    data-testid="recognize-face-button"
                  >
                    {processing ? (
                      <>
                        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                        Processing...
                      </>
                    ) : (
                      <>
                        <UserCheck className="mr-2 h-4 w-4" />
                        Recognize & Mark Attendance
                      </>
                    )}
                  </Button>
                  <Button
                    onClick={stopCamera}
                    variant="outline"
                    data-testid="stop-camera-button"
                  >
                    Stop Camera
                  </Button>
                </div>
                <canvas ref={canvasRef} className="hidden" />
              </div>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Last Recognition</CardTitle>
            <CardDescription>Most recent attendance record</CardDescription>
          </CardHeader>
          <CardContent>
            {lastRecognition ? (
              <div className="space-y-4" data-testid="last-recognition-info">
                <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                  <div className="flex items-center mb-2">
                    <UserCheck className="h-5 w-5 text-green-600 mr-2" />
                    <span className="font-semibold text-green-900">Recognized</span>
                  </div>
                  <div className="space-y-2 text-sm">
                    <div>
                      <span className="text-gray-600">Name:</span>
                      <p className="font-medium">{lastRecognition.employee_name}</p>
                    </div>
                    <div>
                      <span className="text-gray-600">Employee ID:</span>
                      <p className="font-medium">{lastRecognition.employee_id}</p>
                    </div>
                    <div>
                      <span className="text-gray-600">Action:</span>
                      <p className="font-medium capitalize">{lastRecognition.action}</p>
                    </div>
                    <div>
                      <span className="text-gray-600">Time:</span>
                      <p className="font-medium">
                        {new Date(lastRecognition.time).toLocaleTimeString()}
                      </p>
                    </div>
                    {lastRecognition.working_hours && (
                      <div>
                        <span className="text-gray-600">Working Hours:</span>
                        <p className="font-medium">{lastRecognition.working_hours} hours</p>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ) : (
              <div className="text-center py-8 text-gray-500">
                <AlertCircle className="h-12 w-12 mx-auto mb-4 text-gray-400" />
                <p>No recognition yet</p>
                <p className="text-sm mt-2">Start camera and recognize a face</p>
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      <Card className="bg-blue-50 border-blue-200">
        <CardContent className="pt-6">
          <div className="flex items-start space-x-3">
            <AlertCircle className="h-5 w-5 text-blue-600 mt-0.5" />
            <div className="space-y-1">
              <p className="text-sm font-medium text-blue-900">Instructions</p>
              <ul className="text-sm text-blue-800 space-y-1 list-disc list-inside">
                <li>Position your face clearly in front of the camera</li>
                <li>Ensure good lighting for better recognition</li>
                <li>First detection marks in-time, second after 1 hour marks out-time</li>
                <li>Only enrolled employees will be recognized</li>
              </ul>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default LiveAttendance;