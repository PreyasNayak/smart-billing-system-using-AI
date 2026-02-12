# Quick Start Guide

This guide will help you get the Smart Billing System up and running quickly.

## Prerequisites Checklist

Before you begin, ensure you have:

- [ ] Raspberry Pi (3B+ or higher) or compatible computer
- [ ] Camera (Pi Camera Module or USB webcam)
- [ ] HX711 Load Cell module with load cell sensor
- [ ] Python 3.7+ installed
- [ ] Internet connection for downloading dependencies

## Quick Setup (5 Steps)

### Step 1: Clone and Install (5 minutes)

```bash
# Clone the repository
git clone https://github.com/PreyasNayak/smart-billing-system-using-AI.git
cd smart-billing-system-using-AI

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Hardware Connections (10 minutes)

**Connect HX711 Load Cell:**
```
HX711 VCC  → Raspberry Pi 5V (Pin 2)
HX711 GND  → Raspberry Pi GND (Pin 6)
HX711 DT   → Raspberry Pi GPIO 5 (Pin 29)
HX711 SCK  → Raspberry Pi GPIO 6 (Pin 31)
```

**Connect Camera:**
- Pi Camera: Insert into CSI port
- USB Camera: Plug into USB port

### Step 3: Configure Settings (5 minutes)

```bash
# Copy example configuration files
cp config/settings.example.json config/settings.json
cp config/products.example.json config/products.json

# Edit settings.json with your preferences
nano config/settings.json
```

Update key settings:
- Camera index
- GPIO pins (if different)
- Store information

### Step 4: Calibrate Load Cell (5 minutes)

```bash
# Run calibration script (create this based on your implementation)
python calibrate_scale.py
```

Follow the prompts:
1. Remove all items from scale
2. Place known weight (e.g., 100g)
3. Note the calibration factor

### Step 5: Run the System (2 minutes)

```bash
# Start the billing system
python main.py
```

## First Test

1. Place an item on the load cell
2. Position it in camera view
3. System should:
   - Detect the object
   - Read the weight
   - Display/generate invoice

## Troubleshooting Quick Fixes

### Camera not working?
```bash
# For Raspberry Pi Camera
raspistill -o test.jpg

# Enable camera in raspi-config
sudo raspi-config
# Interface Options → Camera → Enable
```

### Load cell not responding?
```bash
# Check GPIO permissions
sudo usermod -a -G gpio $USER
# Logout and login again
```

### Import errors?
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

## Next Steps

Once the basic system is working:

1. **Customize Products**: Edit `config/products.json` with your products
2. **Adjust Detection**: Tune confidence threshold in `config/settings.json`
3. **Train Custom Model**: Train YOLO on your specific products (optional)
4. **Add Features**: Implement additional features as needed

## Getting Help

- Check the full [README.md](README.md) for detailed documentation
- Review [Troubleshooting](README.md#troubleshooting) section
- Open an [issue](https://github.com/PreyasNayak/smart-billing-system-using-AI/issues) on GitHub

## Customization Ideas

After basic setup works, consider:

- Add more products to the database
- Implement database for transaction history
- Add a web interface
- Connect a receipt printer
- Integrate payment systems
- Add barcode scanning support

---

**Estimated Total Setup Time**: 25-30 minutes

**Ready to go deeper?** Check out the full documentation in [README.md](README.md)
