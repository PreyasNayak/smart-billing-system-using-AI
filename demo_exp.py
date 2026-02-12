import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template_string
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import cv2
import numpy as np
import serial
import time
import threading
import base64
import re
from datetime import datetime
import json
from ultralytics import YOLO

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

class ImprovedFruitDetectionSystem:
    def __init__(self, arduino_port='COM3', baud_rate=9600, camera_index=0):
        print("\n" + "="*60)
        print("AI POWERED SMART BILLING SYSTEM")
        print("="*60 + "\n")
        
        # Initialize YOLO model
        print("Loading AI model (this may take a minute)...")
        try:
            self.model = YOLO('yolov8n.pt')
            print("✓ AI model loaded successfully!")
        except Exception as e:
            print(f"✗ Model loading failed: {e}")
            self.model = None
        
        # Initialize Arduino
        print("Connecting to Arduino...")
        try:
            self.arduino = serial.Serial(arduino_port, baud_rate, timeout=1)
            time.sleep(2)
            print("✓ Arduino connected successfully!")
        except Exception as e:
            print(f"✗ Arduino connection failed: {e}")
            print("  Weight readings will show 0.00")
            self.arduino = None
        
        # Initialize camera
        print("Connecting to camera...")
        self.cap = cv2.VideoCapture(camera_index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        
        if self.cap.isOpened():
            print("✓ Camera connected successfully!")
        else:
            print("✗ Camera connection failed!")
        
        # Shared data with thread safety
        self.frame_buffer = None
        self.frame_lock = threading.Lock()
        
        self.current_weight = 0.0
        self.weight_lock = threading.Lock()
        
        self.detected_fruit = 'none'
        self.detection_confidence = 0.0
        self.detection_lock = threading.Lock()
        
        # Fruit mapping
        self.fruit_mapping = {
            'apple': 'apple',
            'banana': 'banana',
            'orange': 'orange',
            'sandwich': 'banana',
            'hot dog': 'banana',
        }
        
        # Fruit prices (₹ per kg)
        self.fruit_prices = {
            'apple': 150,
            'banana': 60,
            'orange': 80,
            'mango': 120,
            'grape': 100,
            'pineapple': 70,
            'watermelon': 30,
            'strawberry': 200,
            'pomegranate': 180,
            'kiwi': 250,
            'pear': 140,
            'peach': 160,
            'lemon': 90,
            'none': 0
        }
        
        self.confidence_threshold = 0.3
        
        self.current_data = {
            'fruit': 'none',
            'weight': 0,
            'price': 0,
            'confidence': 0,
            'timestamp': datetime.now().isoformat()
        }
        
        self.running = False
        self.capture_thread = None
        self.weight_thread = None
        self.detection_thread = None
        self.broadcast_thread = None
        
        print("\n" + "="*60)
        print("System initialized successfully!")
        print("="*60 + "\n")
    
    def capture_frames(self):
        """Thread 1: Continuously capture frames from camera"""
        print("✓ Camera capture thread started\n")
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                with self.frame_lock:
                    self.frame_buffer = frame
            time.sleep(0.01)  # ~100 FPS capture
    
    def weight_reading_loop(self):
        """Thread 2: Continuously read weight from Arduino"""
        print("✓ Weight reading thread started\n")
        while self.running:
            weight = self._read_weight_from_arduino()
            with self.weight_lock:
                self.current_weight = weight
            time.sleep(0.15)  # Read weight ~6-7 times per second
    
    def detection_loop(self):
        """Thread 3: Continuously detect fruits from captured frames"""
        print("✓ Fruit detection thread started\n")
        while self.running:
            # Get latest frame
            with self.frame_lock:
                if self.frame_buffer is None:
                    time.sleep(0.05)
                    continue
                frame = self.frame_buffer.copy()
            
            # Detect fruit
            fruit, confidence = self._detect_fruit_from_frame(frame)
            
            # Update detection results
            with self.detection_lock:
                self.detected_fruit = fruit
                self.detection_confidence = confidence
            
            time.sleep(0.05)  # ~20 FPS detection
    
    def broadcast_loop(self):
        """Thread 4: Continuously broadcast combined data to web interface"""
        print("✓ Broadcast thread started\n")
        while self.running:
            # Gather all data (thread-safe)
            with self.weight_lock:
                weight = self.current_weight
            
            with self.detection_lock:
                fruit = self.detected_fruit
                confidence = self.detection_confidence
            
            # Calculate price
            price = self.calculate_price(fruit, weight)
            
            # Get processed frame for display
            frame_base64 = self._get_display_frame()
            
            # Update current data
            self.current_data = {
                'fruit': fruit,
                'weight': round(weight, 2),
                'price': round(price, 2),
                'confidence': round(confidence * 100, 1),
                'timestamp': datetime.now().isoformat(),
                'frame': frame_base64
            }
            
            # Broadcast to all connected clients
            socketio.emit('update_data', self.current_data)
            
            # Console output
            if fruit != "none":
                print(f"[LIVE] {fruit.upper()} | Weight: {weight:.2f}g | Price: ₹{price:.2f} | Conf: {confidence*100:.1f}%")
            else:
                print(f"[LIVE] No fruit detected | Weight: {weight:.2f}g")
            
            time.sleep(0.1)  # 10 updates per second
    
    def _read_weight_from_arduino(self):
        """Internal: Read weight from Arduino"""
        if not self.arduino or not self.arduino.is_open:
            return 0.0
            
        try:
            # Arduino streams continuously; read a line (Serial timeout=1s)
            for _ in range(2):
                response = self.arduino.readline().decode('utf-8', errors='ignore').strip()

                # Response format is "Weight: X.X g"
                if "Weight:" in response:
                    try:
                        after_label = response.split("Weight:", 1)[1]
                        match = re.search(r"[-+]?\d*\.?\d+", after_label)
                        if match:
                            return abs(float(match.group(0)))
                    except (ValueError, IndexError):
                        continue

            # No new data; keep last known weight
            with self.weight_lock:
                return self.current_weight
                
        except Exception as e:
            return 0.0
    
    def _detect_fruit_from_frame(self, frame):
        """Internal: Detect fruit from frame"""
        if self.model is None or frame is None:
            return "none", 0
        
        try:
            results = self.model(frame, conf=self.confidence_threshold, verbose=False)
            
            detected_fruit = "none"
            max_confidence = 0
            
            for result in results:
                boxes = result.boxes
                
                for box in boxes:
                    class_id = int(box.cls[0])
                    class_name = result.names[class_id].lower()
                    confidence = float(box.conf[0])
                    
                    if class_name in self.fruit_mapping:
                        fruit_name = self.fruit_mapping[class_name]
                        
                        if confidence > max_confidence:
                            max_confidence = confidence
                            detected_fruit = fruit_name
            
            return detected_fruit, max_confidence
            
        except Exception as e:
            return "none", 0
    
    def _get_display_frame(self):
        """Internal: Get processed frame with overlays for display"""
        with self.frame_lock:
            if self.frame_buffer is None:
                return ""
            frame = self.frame_buffer.copy()
        
        with self.detection_lock:
            fruit = self.detected_fruit
            confidence = self.detection_confidence
        
        with self.weight_lock:
            weight = self.current_weight
        
        # Run detection again to draw boxes
        if self.model is not None:
            try:
                results = self.model(frame, conf=self.confidence_threshold, verbose=False)
                
                for result in results:
                    boxes = result.boxes
                    
                    for box in boxes:
                        class_id = int(box.cls[0])
                        class_name = result.names[class_id].lower()
                        conf = float(box.conf[0])
                        
                        if class_name in self.fruit_mapping:
                            fruit_name = self.fruit_mapping[class_name]
                            x1, y1, x2, y2 = map(int, box.xyxy[0])
                            
                            # Color based on confidence
                            if conf > 0.7:
                                color = (0, 255, 0)
                            elif conf > 0.5:
                                color = (0, 255, 255)
                            else:
                                color = (0, 165, 255)
                            
                            # Draw box
                            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 3)
                            
                            # Draw label
                            label = f"{fruit_name.upper()} {conf:.2f}"
                            label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)
                            
                            cv2.rectangle(frame, (x1, y1 - label_size[1] - 10), 
                                        (x1 + label_size[0], y1), color, -1)
                            
                            cv2.putText(frame, label, (x1, y1 - 5),
                                      cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
            except:
                pass
        
        # Add status overlay
        cv2.putText(frame, "AI Detection Active", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Show weight on video
        cv2.putText(frame, f"Weight: {weight:.2f}g", (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        
        # Encode to base64
        _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
        frame_base64 = base64.b64encode(buffer).decode('utf-8')
        
        return frame_base64
    
    def get_weight(self):
        """Get current weight (thread-safe)"""
        with self.weight_lock:
            return self.current_weight
    
    def tare_scale(self):
        """Reset scale to zero"""
        if self.arduino and self.arduino.is_open:
            try:
                self.arduino.write(b'T')
                time.sleep(0.5)
                # Clear the weight immediately
                with self.weight_lock:
                    self.current_weight = 0.0
                return True
            except Exception as e:
                print(f"Tare error: {e}")
        return False
    
    def calculate_price(self, fruit, weight_grams):
        """Calculate price based on weight and fruit type"""
        price_per_kg = self.fruit_prices.get(fruit.lower(), 0)
        weight_kg = weight_grams / 1000.0
        return price_per_kg * weight_kg
    
    def start(self):
        """Start all threads for simultaneous operation"""
        if not self.running:
            self.running = True
            
            # Thread 1: Camera capture
            self.capture_thread = threading.Thread(target=self.capture_frames, name="CameraThread")
            self.capture_thread.daemon = True
            self.capture_thread.start()
            
            # Thread 2: Weight reading
            self.weight_thread = threading.Thread(target=self.weight_reading_loop, name="WeightThread")
            self.weight_thread.daemon = True
            self.weight_thread.start()
            
            # Thread 3: Fruit detection
            self.detection_thread = threading.Thread(target=self.detection_loop, name="DetectionThread")
            self.detection_thread.daemon = True
            self.detection_thread.start()
            
            # Thread 4: Broadcasting to web
            self.broadcast_thread = threading.Thread(target=self.broadcast_loop, name="BroadcastThread")
            self.broadcast_thread.daemon = True
            self.broadcast_thread.start()
            
            print("\n" + "="*60)
            print("ALL THREADS STARTED - SIMULTANEOUS OPERATION ACTIVE")
            print("="*60 + "\n")
    
    def stop(self):
        """Stop all threads"""
        self.running = False
        if self.capture_thread:
            self.capture_thread.join(timeout=2)
        if self.weight_thread:
            self.weight_thread.join(timeout=2)
        if self.detection_thread:
            self.detection_thread.join(timeout=2)
        if self.broadcast_thread:
            self.broadcast_thread.join(timeout=2)
    
    def cleanup(self):
        """Clean up resources"""
        self.stop()
        if self.cap:
            self.cap.release()
        if self.arduino and self.arduino.is_open:
            self.arduino.close()

# *** CONFIGURE THESE VALUES ***
ARDUINO_PORT = 'COM3'  # Change to your port!
CAMERA_INDEX = 0

detector = ImprovedFruitDetectionSystem(
    arduino_port=ARDUINO_PORT,
    baud_rate=9600,
    camera_index=CAMERA_INDEX
)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>AI Powered Smart Billing System</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script src="https://cdn.socket.io/4.5.4/socket.io.min.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', system-ui, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container { max-width: 1600px; margin: 0 auto; }
        .header {
            text-align: center;
            color: white;
            margin-bottom: 30px;
            animation: fadeIn 1s;
        }
        .header h1 { 
            font-size: 2.8em; 
            margin-bottom: 10px; 
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .ai-badge {
            display: inline-block;
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            padding: 8px 20px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: bold;
            margin-top: 10px;
            animation: pulse 2s infinite;
        }
        .dashboard {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }
        .card {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            transition: transform 0.3s;
            animation: slideUp 0.5s;
        }
        .card:hover { transform: translateY(-5px); }
        .card-title {
            font-size: 1em;
            color: #666;
            margin-bottom: 15px;
            font-weight: 600;
        }
        .card-value {
            font-size: 2.5em;
            font-weight: bold;
            text-align: center;
            margin: 15px 0;
            transition: all 0.3s;
        }
        .fruit-value { color: #e74c3c; }
        .weight-value { color: #3498db; }
        .price-value { color: #27ae60; }
        .confidence-value { color: #9b59b6; }
        .confidence-bar {
            width: 100%;
            height: 10px;
            background: #ecf0f1;
            border-radius: 5px;
            overflow: hidden;
            margin-top: 10px;
        }
        .confidence-fill {
            height: 100%;
            background: linear-gradient(90deg, #e74c3c, #f39c12, #27ae60);
            transition: width 0.3s;
            border-radius: 5px;
        }
        .video-container {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 20px;
        }
        #video-feed {
            width: 100%;
            border-radius: 10px;
            background: #000;
            min-height: 400px;
        }
        .controls {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }
        button {
            padding: 15px 25px;
            font-size: 1.1em;
            font-weight: bold;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        button:hover { transform: translateY(-2px); }
        button:active { transform: translateY(0); }
        .btn-tare { background: #3498db; color: white; }
        .btn-tare:hover { background: #2980b9; }
        .btn-save { background: #27ae60; color: white; }
        .btn-save:hover { background: #229954; }
        .history {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #eee; }
        th { background: #f8f9fa; font-weight: 600; }
        tr:hover { background: #f8f9fa; }
        .status-live { 
            background: #d4edda; 
            color: #155724;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: bold;
            animation: blink 2s infinite;
        }
        .system-status {
            background: #e3f2fd;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            text-align: center;
            color: #1565c0;
            font-weight: bold;
        }
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
        @keyframes slideUp { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: translateY(0); } }
        @keyframes pulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.05); } }
        @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0.7; } }

        @media print {
            body { background: #fff; padding: 0; }
            .container > *:not(#bill-modal) { display: none !important; }
            #bill-modal { display: block !important; position: static !important; background: none !important; }
            #bill-modal > div { box-shadow: none !important; max-width: none !important; width: 100% !important; }
            #bill-modal button { display: none !important; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 AI Powered Smart Billing System</h1>
            <div class="ai-badge">⚡ YOLO Deep Learning Model</div>
            <p style="margin-top: 10px;">Real-time simultaneous detection and weighing</p>
        </div>

        <div class="system-status">
            🔄 SIMULTANEOUS MODE: Camera + Weight Sensor + AI Detection Running in Parallel
        </div>

        <div class="dashboard">
            <div class="card">
                <div class="card-title">🍇 Detected Fruit</div>
                <div class="card-value fruit-value">
                    <span id="fruit-emoji" style="font-size: 1.5em;">❌</span>
                    <div id="fruit-display" style="font-size: 0.5em; margin-top: 10px;">None</div>
                </div>
            </div>
            <div class="card">
                <div class="card-title">⚖️ Weight (Live)</div>
                <div class="card-value weight-value" id="weight-display">0.00</div>
                <div style="text-align: center; color: #666; font-size: 0.8em;">grams</div>
            </div>
            <div class="card">
                <div class="card-title">💰 Price</div>
                <div class="card-value price-value" id="price-display">₹0.00</div>
            </div>
            <div class="card">
                <div class="card-title">🎯 AI Confidence</div>
                <div class="card-value confidence-value" id="confidence-display">0%</div>
                <div class="confidence-bar">
                    <div class="confidence-fill" id="confidence-bar" style="width: 0%"></div>
                </div>
            </div>
        </div>

        <div class="video-container">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                <div class="card-title" style="margin: 0;">📹 Live AI Detection Feed</div>
                <span class="status-live">● LIVE</span>
            </div>
            <img id="video-feed" src="" alt="Loading AI model...">
            <div class="controls">
                <button class="btn-save" onclick="saveReading()">💾 Save Reading</button>
                <button class="btn-save" onclick="generateBill()">🧾 Generate Bill</button>
            </div>
        </div>

        <div class="history">
            <div class="card-title">📊 Recent Measurements</div>
            <div style="overflow-x: auto;">
                <table>
                    <thead>
                        <tr>
                            <th>Time</th>
                            <th>Fruit</th>
                            <th>Confidence</th>
                            <th style="text-align: right;">Weight (g)</th>
                            <th style="text-align: right;">Price (₹)</th>
                        </tr>
                    </thead>
                    <tbody id="history-body">
                        <tr>
                            <td colspan="5" style="text-align: center; color: #999; padding: 40px;">
                                No measurements saved yet. Place fruit and click "Save Reading"
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <div id="bill-modal" style="display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.5); align-items: center; justify-content: center;">
            <div style="background: white; width: 90%; max-width: 700px; border-radius: 12px; padding: 20px; box-shadow: 0 20px 40px rgba(0,0,0,0.3);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <div style="font-weight: 700; font-size: 1.2em;">🧾 Bill Summary</div>
                    <div>
                        <button onclick="printBill()" style="background: #27ae60; color: white;">Download PDF / Print</button>
                        <button onclick="clearBill()" style="background: #e74c3c; color: white;">Clear Bill</button>
                        <button onclick="closeBill()" style="background: #eee; color: #333;">Close</button>
                    </div>
                </div>
                <div id="bill-content" style="max-height: 400px; overflow: auto; font-size: 0.95em;"></div>
            </div>
        </div>
    </div>

    <script>
        const socket = io();
        let history = [];
        let updateCount = 0;
        let lastUpdateTime = Date.now();
        
        const fruitEmojis = {
            'apple': '🍎', 'banana': '🍌', 'orange': '🍊', 'mango': '🥭',
            'grape': '🍇', 'watermelon': '🍉', 'strawberry': '🍓',
            'pineapple': '🍍', 'kiwi': '🥝', 'pear': '🍐',
            'peach': '🍑', 'lemon': '🍋', 'pomegranate': '🍎', 'none': '❌'
        };

        socket.on('connect', () => {
            console.log('✓ Connected to server - Simultaneous mode active');
        });

        socket.on('update_data', (data) => {
            updateCount++;
            const now = Date.now();
            const fps = 1000 / (now - lastUpdateTime);
            lastUpdateTime = now;
            
            console.log(`Update #${updateCount} | FPS: ${fps.toFixed(1)} | Fruit: ${data.fruit} | Weight: ${data.weight}g`);
            
            // Update all displays with smooth animation
            document.getElementById('fruit-emoji').textContent = fruitEmojis[data.fruit] || '🍇';
            document.getElementById('fruit-display').textContent = 
                data.fruit.charAt(0).toUpperCase() + data.fruit.slice(1);
            document.getElementById('weight-display').textContent = data.weight.toFixed(2);
            document.getElementById('price-display').textContent = '₹' + data.price.toFixed(2);
            document.getElementById('confidence-display').textContent = data.confidence + '%';
            document.getElementById('confidence-bar').style.width = data.confidence + '%';
            
            // Update video feed
            if (data.frame) {
                document.getElementById('video-feed').src = 'data:image/jpeg;base64,' + data.frame;
            }
        });

        socket.on('disconnect', () => {
            console.log('✗ Disconnected from server');
        });

        function tare() {
            if (confirm('Reset scale to zero?')) {
                fetch('/tare', { method: 'POST' })
                    .then(r => r.json())
                    .then(data => {
                        alert(data.message);
                        console.log('Tare successful');
                    })
                    .catch(err => {
                        console.error('Tare error:', err);
                        alert('Error resetting scale');
                    });
            }
        }

        function saveReading() {
            fetch('/save', { method: 'POST' })
                .then(r => r.json())
                .then(data => {
                    if (data.success) {
                        addToHistory(data.data);
                        alert('✓ Reading saved successfully!');
                    } else {
                        alert('✗ ' + data.message);
                    }
                })
                .catch(err => {
                    console.error('Save error:', err);
                    alert('Error saving reading');
                });
        }

        function addToHistory(data) {
            history.unshift(data);
            if (history.length > 10) history.pop();
            
            document.getElementById('history-body').innerHTML = history.map(entry => `
                <tr>
                    <td>${new Date(entry.timestamp).toLocaleString()}</td>
                    <td>
                        <span style="font-size: 1.3em;">${fruitEmojis[entry.fruit] || '🍇'}</span>
                        <span style="text-transform: capitalize; margin-left: 8px; font-weight: 500;">${entry.fruit}</span>
                    </td>
                    <td><span style="color: #9b59b6; font-weight: bold;">${entry.confidence}%</span></td>
                    <td style="text-align: right; font-weight: 500;">${entry.weight.toFixed(2)}</td>
                    <td style="text-align: right; color: #27ae60; font-weight: bold;">₹${entry.price.toFixed(2)}</td>
                </tr>
            `).join('');
        }

        function generateBill() {
            fetch('/bill')
                .then(r => r.json())
                .then(data => {
                    if (!data.success) {
                        alert(data.message || 'No saved readings found');
                        return;
                    }

                    const rows = data.items.map((item, idx) => `
                        <tr>
                            <td>${idx + 1}</td>
                            <td style="text-transform: capitalize;">${item.fruit}</td>
                            <td style="text-align: right;">${item.weight.toFixed(2)}</td>
                            <td style="text-align: right;">₹${item.price.toFixed(2)}</td>
                        </tr>
                    `).join('');

                    const html = `
                        <div style="margin-bottom: 10px; color: #666;">Generated: ${new Date(data.generated_at).toLocaleString()}</div>
                        <table style="width: 100%; border-collapse: collapse;">
                            <thead>
                                <tr>
                                    <th style="text-align: left;">#</th>
                                    <th style="text-align: left;">Fruit</th>
                                    <th style="text-align: right;">Weight (g)</th>
                                    <th style="text-align: right;">Price (₹)</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${rows}
                            </tbody>
                            <tfoot>
                                <tr>
                                    <td colspan="3" style="text-align: right; font-weight: 700; padding-top: 10px;">Total</td>
                                    <td style="text-align: right; font-weight: 700; padding-top: 10px;">₹${data.total.toFixed(2)}</td>
                                </tr>
                            </tfoot>
                        </table>
                    `;

                    document.getElementById('bill-content').innerHTML = html;
                    document.getElementById('bill-modal').style.display = 'flex';
                })
                .catch(err => {
                    console.error('Bill error:', err);
                    alert('Error generating bill');
                });
        }

        function closeBill() {
            document.getElementById('bill-modal').style.display = 'none';
        }

        function printBill() {
            window.print();
        }

        function clearBill() {
            if (!confirm('Clear all saved readings?')) return;
            fetch('/bill/clear', { method: 'POST' })
                .then(r => r.json())
                .then(data => {
                    if (data.success) {
                        alert('Bill cleared');
                        document.getElementById('bill-content').innerHTML = '';
                        history = [];
                        document.getElementById('history-body').innerHTML = `
                            <tr>
                                <td colspan="5" style="text-align: center; color: #999; padding: 40px;">
                                    No measurements saved yet. Place fruit and click "Save Reading"
                                </td>
                            </tr>
                        `;
                    } else {
                        alert(data.message || 'Failed to clear bill');
                    }
                })
                .catch(err => {
                    console.error('Clear bill error:', err);
                    alert('Error clearing bill');
                });
        }

        // Show connection status
        window.addEventListener('load', () => {
            console.log('🚀 Web interface loaded');
            console.log('⚡ Waiting for data stream...');
        });
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/tare', methods=['POST'])
def tare():
    success = detector.tare_scale()
    return {'success': success, 'message': '✓ Scale reset to zero' if success else '✗ Failed to reset scale'}

@app.route('/save', methods=['POST'])
def save_reading():
    data = detector.current_data.copy()
    if data['fruit'] != 'none' and data['weight'] > 0:
        try:
            with open('readings.json', 'a') as f:
                f.write(json.dumps(data) + '\n')
            return {'success': True, 'data': data}
        except Exception as e:
            return {'success': False, 'message': f'Save error: {str(e)}'}
    return {'success': False, 'message': 'No valid data (no fruit detected or zero weight)'}

@app.route('/bill', methods=['GET'])
def generate_bill():
    items = []
    try:
        with open('readings.json', 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    items.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    except FileNotFoundError:
        return {'success': False, 'message': 'No saved readings found'}

    if not items:
        return {'success': False, 'message': 'No saved readings found'}

    total = sum(item.get('price', 0) for item in items)

    return {
        'success': True,
        'items': [
            {
                'fruit': item.get('fruit', 'unknown'),
                'weight': float(item.get('weight', 0)),
                'price': float(item.get('price', 0))
            }
            for item in items
        ],
        'total': float(total),
        'generated_at': datetime.now().isoformat()
    }

@app.route('/bill/clear', methods=['POST'])
def clear_bill():
    try:
        open('readings.json', 'w').close()
        return {'success': True}
    except Exception as e:
        return {'success': False, 'message': f'Clear error: {str(e)}'}

@socketio.on('connect')
def handle_connect():
    print('✓ New client connected')
    emit('update_data', detector.current_data)

@socketio.on('disconnect')
def handle_disconnect():
    print('✗ Client disconnected')

if __name__ == '__main__':
    try:
        detector.start()
        print("\n" + "="*60)
        print("🚀 SIMULTANEOUS DETECTION SYSTEM STARTING...")
        print("="*60)
        print("\n✓ Thread 1: Camera Capture - Running")
        print("✓ Thread 2: Weight Reading - Running")
        print("✓ Thread 3: Fruit Detection - Running")
        print("✓ Thread 4: Data Broadcasting - Running")
        print("\n📱 Open your browser and go to:")
        print("\n   http://localhost:5000")
        print("\n   Or from another device on same network:")
        print("   http://YOUR-COMPUTER-IP:5000")
        print("\n" + "="*60)
        print("Press Ctrl+C to stop the server")
        print("="*60 + "\n")
        
        socketio.run(app, host='0.0.0.0', port=5000, debug=False)
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down...")
        print("Stopping all threads...")
        detector.cleanup()
        print("✓ All threads stopped")
        print("✓ Resources released")
        print("Goodbye! 👋\n")