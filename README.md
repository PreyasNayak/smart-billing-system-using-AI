# Smart Billing System Using AI 🛒💡

An intelligent billing system that combines computer vision and IoT hardware to automatically detect products, measure their weight, and generate invoice bills in real-time.

## 🌟 Features

- **Object Detection**: Uses YOLO (You Only Look Once) machine learning model to identify products
- **Weight Measurement**: Integrates HX711 load cell sensor for accurate weight readings
- **Automated Billing**: Generates detailed invoice bills automatically
- **Real-time Processing**: Simultaneous object detection and weight measurement
- **Cost-effective**: Reduces manual billing errors and speeds up checkout process

## 📋 Table of Contents

- [Hardware Requirements](#hardware-requirements)
- [Software Requirements](#software-requirements)
- [Installation](#installation)
- [Hardware Setup](#hardware-setup)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## 🔧 Hardware Requirements

- **Raspberry Pi** (3B+ or higher recommended) or any compatible SBC
- **Camera Module**: 
  - Raspberry Pi Camera Module V2 or
  - USB Webcam (720p or higher)
- **HX711 Load Cell Amplifier**
- **Load Cell Sensor** (suitable weight capacity for your use case)
- **Display** (for showing results, optional)
- **Power Supply**: 5V 3A adapter for Raspberry Pi
- **Breadboard and Jumper Wires**

### Hardware Connections

#### HX711 Load Cell Wiring:
```
HX711 Module    →    Raspberry Pi
VCC             →    5V
GND             →    GND
DT (Data)       →    GPIO 5 (Pin 29)
SCK (Clock)     →    GPIO 6 (Pin 31)
```

#### Camera Connection:
- For Pi Camera: Connect to CSI port on Raspberry Pi
- For USB Camera: Connect to any USB port

## 💻 Software Requirements

- **Operating System**: Raspberry Pi OS (Buster or later) / Ubuntu 20.04+
- **Python**: 3.7 or higher
- **Libraries**:
  - OpenCV (cv2)
  - NumPy
  - PyTorch or TensorFlow
  - Ultralytics YOLO
  - HX711 Python library
  - PIL (Pillow)
  - ReportLab (for PDF generation)

## 📥 Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/PreyasNayak/smart-billing-system-using-AI.git
cd smart-billing-system-using-AI
```

### Step 2: Set Up Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Download YOLO Model Weights

```bash
# Download YOLOv5 or YOLOv8 weights
# Option 1: YOLOv5
wget https://github.com/ultralytics/yolov5/releases/download/v7.0/yolov5s.pt -P models/

# Option 2: YOLOv8 (recommended)
# The model will be automatically downloaded on first run
```

### Step 5: Enable Camera and I2C (for Raspberry Pi)

```bash
sudo raspi-config
# Navigate to Interface Options
# Enable Camera and I2C
```

## 🔌 Hardware Setup

1. **Connect the Load Cell**:
   - Attach load cell wires to the HX711 module (Red: E+, Black: E-, White: A-, Green: A+)
   - Connect HX711 to Raspberry Pi as per wiring diagram above

2. **Connect the Camera**:
   - Insert Pi Camera into CSI port or plug in USB camera

3. **Calibrate the Load Cell**:
   ```bash
   python calibrate_scale.py
   ```
   Follow the on-screen instructions to calibrate with known weights

4. **Test Hardware**:
   ```bash
   python test_hardware.py
   ```

## 🚀 Usage

### Basic Usage

```bash
python main.py
```

### Command Line Options

```bash
python main.py --camera 0                    # Use camera index 0
python main.py --model yolov8n.pt           # Use specific YOLO model
python main.py --confidence 0.5             # Set confidence threshold
python main.py --output invoices/           # Set output directory
```

### Web Interface (if available)

```bash
python app.py
# Access at http://localhost:5000
```

## 📁 Project Structure

```
smart-billing-system-using-AI/
├── main.py                 # Main application entry point
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── LICENSE               # MIT License
├── models/               # YOLO model weights
│   └── yolov8n.pt
├── src/                  # Source code
│   ├── detector.py       # Object detection module
│   ├── scale.py          # Load cell/weight measurement
│   ├── billing.py        # Invoice generation
│   └── utils.py          # Utility functions
├── config/               # Configuration files
│   ├── products.json     # Product database
│   └── settings.json     # System settings
├── invoices/             # Generated invoices (output)
├── logs/                 # Application logs
└── tests/                # Unit tests
    ├── test_detector.py
    └── test_scale.py
```

## ⚙️ Configuration

### Product Database (`config/products.json`)

```json
{
  "apple": {
    "name": "Apple",
    "price_per_kg": 3.50,
    "category": "fruits"
  },
  "banana": {
    "name": "Banana", 
    "price_per_kg": 2.00,
    "category": "fruits"
  }
}
```

### System Settings (`config/settings.json`)

```json
{
  "camera": {
    "index": 0,
    "resolution": [640, 480],
    "fps": 30
  },
  "yolo": {
    "model": "yolov8n.pt",
    "confidence": 0.5,
    "iou_threshold": 0.45
  },
  "scale": {
    "dout_pin": 5,
    "pd_sck_pin": 6,
    "calibration_factor": 1.0
  },
  "billing": {
    "tax_rate": 0.1,
    "currency": "USD",
    "store_name": "Smart Store"
  }
}
```

## 🛠️ Troubleshooting

### Camera Issues

**Problem**: Camera not detected
```bash
# Test camera
raspistill -o test.jpg  # For Pi Camera
fswebcam test.jpg       # For USB camera

# Check camera is enabled
vcgencmd get_camera     # Should show: supported=1 detected=1
```

### Load Cell Issues

**Problem**: Incorrect or unstable readings
- Ensure proper wiring connections
- Re-calibrate the load cell
- Check for loose connections
- Use shielded cables to reduce noise

**Problem**: Import error for HX711
```bash
pip install --upgrade HX711
```

### YOLO Model Issues

**Problem**: Model not loading
- Ensure model file exists in `models/` directory
- Check PyTorch installation: `python -c "import torch; print(torch.__version__)"`
- Try downloading model again

### Permission Issues

**Problem**: GPIO permission denied
```bash
sudo usermod -a -G gpio $USER
# Logout and login again
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Test thoroughly
5. Commit your changes (`git commit -am 'Add new feature'`)
6. Push to the branch (`git push origin feature/improvement`)
7. Create a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 📝 Example Use Cases

- **Retail Stores**: Automated checkout for fruits, vegetables, and bulk items
- **Grocery Stores**: Self-service kiosks
- **Warehouses**: Inventory management and tracking
- **Markets**: Quick and accurate billing for weight-based products

## 🔮 Future Enhancements

- [ ] Multi-object detection support
- [ ] Database integration for inventory management
- [ ] Cloud connectivity for analytics
- [ ] Mobile app integration
- [ ] Receipt printer support
- [ ] Barcode/QR code scanning
- [ ] Multiple payment gateway integration

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**PREYAS S D**

## 🙏 Acknowledgments

- [Ultralytics YOLO](https://github.com/ultralytics/ultralytics) for the object detection model
- [HX711 Python Library](https://github.com/tatobari/hx711py) for load cell integration
- OpenCV community for computer vision tools

## 📧 Contact & Support

If you have questions or need support:
- Open an issue on GitHub
- Check existing issues for solutions
- Refer to the troubleshooting section above

---

⭐ If you find this project helpful, please give it a star on GitHub!
