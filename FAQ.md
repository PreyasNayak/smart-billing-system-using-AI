# Frequently Asked Questions (FAQ)

## General Questions

### What is this project?
A smart billing system that uses AI (YOLO object detection) and IoT sensors (HX711 load cell) to automatically identify products, measure their weight, and generate invoices.

### What can I use this for?
- Small retail stores (fruits, vegetables, bulk items)
- Self-service kiosks
- Inventory management
- Automated checkout systems
- Learning AI and IoT integration

### Is this production-ready?
This is an educational/prototype project. For production use, you may need to:
- Add error handling and validation
- Implement security features
- Add database integration
- Include payment processing
- Ensure hardware reliability

## Hardware Questions

### What hardware do I need?
- Raspberry Pi (3B+ or higher)
- Camera (Pi Camera or USB webcam)
- HX711 load cell amplifier
- Load cell sensor (appropriate capacity)
- Power supply and cables

See [HARDWARE.md](HARDWARE.md) for detailed specifications.

### Can I use a different single-board computer?
Yes! Any Linux-based SBC with GPIO pins can work:
- Raspberry Pi (all models 3+)
- NVIDIA Jetson Nano (better for AI)
- Orange Pi
- Rock Pi

You may need to adjust GPIO pin configurations.

### Can I use a laptop instead of Raspberry Pi?
Yes, but:
- You'll need a USB webcam
- Load cell requires USB-to-GPIO adapter or Arduino bridge
- Less portable solution
- May be more expensive

### What load cell capacity should I choose?
Depends on your use case:
- **1kg**: Small items, spices, tea
- **5kg**: Fruits, vegetables, general groceries
- **10kg**: Larger items, multiple products
- **20kg+**: Heavy items, commercial use

### My load cell readings are unstable, what should I do?
- Check all wire connections
- Use shielded cables
- Ensure stable mounting surface
- Keep away from electromagnetic interference
- Recalibrate regularly
- Check for mechanical stress on sensor

## Software Questions

### What YOLO version should I use?
- **YOLOv8**: Recommended, best accuracy/speed balance
- **YOLOv5**: Also good, widely supported
- **YOLOv4**: Older but stable
- **YOLO-Lite**: For Raspberry Pi 3 (slower hardware)

### Can I detect custom products?
Yes! You have two options:
1. **Use pre-trained model**: Works for common items (fruits, bottles, etc.)
2. **Train custom model**: Better accuracy for specific products
   - Collect 100-500 images per product
   - Annotate images (using LabelImg or Roboflow)
   - Train using YOLOv5/v8 training scripts

### How accurate is the object detection?
Depends on:
- Model quality (pre-trained vs custom)
- Training data
- Lighting conditions
- Camera quality
- Object visibility

Typical accuracy: 70-95% with good conditions

### How accurate is the weight measurement?
HX711 load cells typically provide:
- Resolution: ±0.1g to ±1g
- Accuracy: ±0.1% to ±0.5% of capacity
- Affected by: temperature, vibration, calibration quality

### Can I run this without a display?
Yes! You can:
- Run headless and save invoices to disk
- Access via web interface (if implemented)
- Use SSH for remote access
- Send results to database/cloud

### What operating system should I use?
Recommended:
- **Raspberry Pi OS** (Buster or later)
- **Ubuntu 20.04+** for Raspberry Pi
- **Debian-based** Linux distributions

## Implementation Questions

### How do I add new products?
Edit `config/products.json`:
```json
{
  "product_name": {
    "name": "Display Name",
    "price_per_kg": 2.50,
    "category": "category_name",
    "tax_rate": 0.05
  }
}
```

### Can I use a barcode scanner too?
Yes! You can integrate:
- USB barcode scanner
- Read barcode as keyboard input
- Combine with YOLO detection for verification

### How do I generate PDF invoices?
Use libraries like:
- ReportLab (included in requirements.txt)
- FPDF
- WeasyPrint

See billing module examples.

### Can I save transactions to a database?
Yes! Add database integration:
- SQLite (simple, local)
- MySQL/PostgreSQL (more robust)
- MongoDB (document-based)
- Cloud services (Firebase, AWS)

### How do I add a web interface?
Use Flask (included in requirements):
```python
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
```

## Performance Questions

### How fast is the detection?
Depends on hardware:
- **Raspberry Pi 4**: 5-10 FPS with YOLOv8n
- **Raspberry Pi 3**: 2-5 FPS
- **Jetson Nano**: 20-30 FPS
- **Desktop GPU**: 30-60 FPS

### Can I make it faster?
Yes:
- Use smaller YOLO model (yolov8n vs yolov8x)
- Lower camera resolution
- Reduce inference frequency
- Use hardware acceleration (Coral TPU, GPU)
- Optimize Python code

### How much RAM do I need?
Minimum:
- 2GB for basic operation
- 4GB recommended
- 8GB for comfortable development

### Does it work offline?
Yes! Once set up:
- No internet needed for operation
- Models run locally
- Only need connectivity for updates

## Troubleshooting

### "Camera not detected" error
```bash
# Enable camera
sudo raspi-config
# Navigate: Interface Options → Camera → Enable

# Test camera
raspistill -o test.jpg
```

### "GPIO permission denied" error
```bash
# Add user to GPIO group
sudo usermod -a -G gpio $USER
# Logout and login again
```

### Import errors for libraries
```bash
# Reinstall requirements
pip install --upgrade -r requirements.txt

# For specific library
pip install --upgrade library-name
```

### Poor detection accuracy
Solutions:
- Improve lighting (bright, even illumination)
- Clean camera lens
- Adjust camera angle/distance
- Use higher confidence threshold
- Train custom model for your products

### Invoice not generating
Check:
- Output directory exists (`invoices/`)
- Write permissions
- ReportLab installed
- No errors in logs

## Contributing

### How can I contribute?
See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines:
- Report bugs
- Suggest features
- Submit code improvements
- Improve documentation
- Share your implementation

### I found a bug, what should I do?
1. Check if already reported in Issues
2. Create new issue with details:
   - Description
   - Steps to reproduce
   - Environment info
   - Error messages/logs

### I want to add a feature
1. Open an issue to discuss
2. Fork the repository
3. Create feature branch
4. Implement and test
5. Submit pull request

## Licensing

### Can I use this commercially?
Yes! MIT License allows:
- Commercial use
- Modification
- Distribution
- Private use

Requirements:
- Include original license
- Include copyright notice

### Can I sell systems based on this?
Yes, under MIT License terms. However:
- Provide attribution
- No warranty provided
- Test thoroughly for commercial use

## Getting More Help

### Where can I get support?
1. Read [README.md](README.md)
2. Check this FAQ
3. Search existing [GitHub Issues](https://github.com/PreyasNayak/smart-billing-system-using-AI/issues)
4. Open new issue with details

### I want to learn more about the technologies
Resources:
- **YOLO**: [Ultralytics Documentation](https://docs.ultralytics.com/)
- **OpenCV**: [OpenCV Tutorials](https://docs.opencv.org/master/d9/df8/tutorial_root.html)
- **Raspberry Pi**: [Official Documentation](https://www.raspberrypi.org/documentation/)
- **Load Cells**: [HX711 Guide](https://learn.sparkfun.com/tutorials/load-cell-amplifier-hx711-breakout-hookup-guide)

### Can I contact the author?
- GitHub Issues: Best for technical questions
- Discussions: For general questions
- Email: Check author's GitHub profile

---

**Don't see your question?** Open an issue on GitHub and we'll add it to the FAQ!
