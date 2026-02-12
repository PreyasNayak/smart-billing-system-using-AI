# Hardware Setup Guide

## Components Overview

This guide provides detailed information about the hardware components and their setup.

## Required Components

### 1. Raspberry Pi Setup

**Recommended Models:**
- Raspberry Pi 4 Model B (4GB RAM) - Best performance
- Raspberry Pi 3 Model B+ - Good performance
- Raspberry Pi 400 - Integrated keyboard version

**Power Supply:**
- 5V 3A USB-C power adapter (Pi 4)
- 5V 2.5A Micro USB adapter (Pi 3)

### 2. Camera Module

**Option A: Raspberry Pi Camera Module V2**
- 8MP sensor
- 1080p video
- Direct CSI connection
- Cost: ~$25-30

**Option B: USB Webcam**
- Minimum 720p resolution
- USB 2.0 or higher
- Wide angle lens preferred
- Cost: ~$20-50

### 3. Load Cell System

**HX711 Amplifier Module:**
- 24-bit ADC
- Dual channel
- 3.3V or 5V operation
- Cost: ~$5-10

**Load Cell Sensor:**
- Capacity: Choose based on your needs
  - 1kg - For light items (fruits, vegetables)
  - 5kg - General purpose
  - 10kg+ - Heavy items
- Type: Single point load cell
- Cost: ~$5-15

**Load Cell Wire Colors (Standard):**
- Red: Excitation+ (E+)
- Black: Excitation- (E-)
- White: Signal- (A-)
- Green: Signal+ (A+)

### 4. Optional Components

- **Display**: 7" touchscreen for Raspberry Pi (~$60)
- **Case**: Protective case for Raspberry Pi (~$10)
- **Cooling**: Heatsinks and fan (~$5-10)
- **Power Bank**: For portable operation (~$20-30)

## Wiring Diagram

### HX711 to Raspberry Pi Connection

```
┌─────────────────────────────────────────┐
│         Raspberry Pi GPIO               │
│                                         │
│  Pin 2  (5V)     ●─────────────┐      │
│  Pin 6  (GND)    ●─────────┐   │      │
│  Pin 29 (GPIO 5) ●───────┐ │   │      │
│  Pin 31 (GPIO 6) ●─────┐ │ │   │      │
└────────────────────────┼─┼─┼───┼───────┘
                         │ │ │   │
                         │ │ │   │
            ┌────────────┼─┼─┼───┼────────┐
            │            │ │ │   │        │
            │  HX711     │ │ │   │        │
            │            │ │ │   │        │
            │  VCC ──────┘ │ │   │        │
            │  GND ────────┘ │   │        │
            │  DT ───────────┘   │        │
            │  SCK ──────────────┘        │
            │                             │
            │  E+  ●                      │
            │  E-  ●                      │
            │  A-  ●                      │
            │  A+  ●                      │
            └─────┼──────────────┬────────┘
                  │              │
            ┌─────┴──────────────┴────────┐
            │                             │
            │   Load Cell                 │
            │   Red    → E+               │
            │   Black  → E-               │
            │   White  → A-               │
            │   Green  → A+               │
            │                             │
            └─────────────────────────────┘
```

### Pin Reference (Raspberry Pi)

| Pin Number | Function | Connection |
|------------|----------|------------|
| 2          | 5V Power | HX711 VCC  |
| 6          | Ground   | HX711 GND  |
| 29         | GPIO 5   | HX711 DT (Data) |
| 31         | GPIO 6   | HX711 SCK (Clock) |

### Camera Connection

**For Pi Camera Module:**
```
1. Locate the CSI port (between HDMI and USB ports)
2. Gently pull up the plastic clip
3. Insert ribbon cable (blue side facing USB ports)
4. Push down the plastic clip
```

**For USB Camera:**
```
Simply plug into any available USB port
```

## Physical Assembly

### Step 1: Prepare Load Cell Platform

1. Mount load cell on a stable base
2. Attach platform on top for items
3. Ensure load cell is level
4. Secure all connections

### Step 2: Position Camera

1. Mount camera with clear view of platform
2. Angle: 30-45 degrees above platform
3. Distance: 20-40cm from platform
4. Ensure good lighting

### Step 3: Wire Connections

1. Connect load cell to HX711 (match wire colors)
2. Connect HX711 to Raspberry Pi GPIO
3. Connect camera (CSI or USB)
4. Double-check all connections

### Step 4: Power Up

1. Connect power supply to Raspberry Pi
2. Wait for system to boot
3. Check LED indicators on HX711

## Testing Hardware

### Test Camera

```bash
# For Pi Camera
raspistill -o test.jpg
# Check if test.jpg is created

# For USB Camera  
ls /dev/video*
# Should show /dev/video0 or similar
```

### Test Load Cell

```bash
# Run basic test (you'll need to create this script)
python test_loadcell.py
```

Expected output:
```
Reading from load cell...
Raw value: 8388608
Stable connection: Yes
```

## Calibration Process

### Load Cell Calibration Steps

1. **Tare (Zero) Reading**
   ```bash
   python calibrate_scale.py --tare
   ```
   - Remove all items from scale
   - Note the offset value

2. **Calibration Weight**
   ```bash
   python calibrate_scale.py --calibrate 100
   ```
   - Place known 100g weight
   - Record calibration factor

3. **Verify**
   ```bash
   python calibrate_scale.py --verify
   ```
   - Test with multiple known weights
   - Ensure accuracy within ±2%

### Camera Calibration

1. **Adjust Exposure**
   - Test under your lighting conditions
   - Adjust camera settings if needed

2. **Test Detection**
   ```bash
   python test_detection.py
   ```
   - Place test items
   - Verify detection accuracy

## Troubleshooting Hardware

### Load Cell Issues

**Problem**: No readings from load cell

**Solutions:**
- Check wire connections (especially color matching)
- Verify GPIO pins in configuration
- Test with multimeter (E+ to E- should be ~1000Ω)
- Ensure HX711 has power (LED should be on)

**Problem**: Unstable readings

**Solutions:**
- Check for loose wires
- Ensure load cell is on stable surface
- Add shielded cable if electrical noise present
- Recalibrate

### Camera Issues

**Problem**: Camera not detected

**Solutions:**
- Check ribbon cable connection
- Enable camera in `raspi-config`
- Try different USB port (for USB camera)
- Update Raspberry Pi OS

**Problem**: Poor image quality

**Solutions:**
- Clean camera lens
- Adjust lighting
- Change camera angle
- Modify resolution settings

## Maintenance Tips

1. **Regular Calibration**: Recalibrate weekly for best accuracy
2. **Clean Sensors**: Keep camera lens and load cell clean
3. **Check Connections**: Periodically verify wire connections
4. **Protect from Elements**: Keep hardware away from moisture
5. **Cooling**: Ensure Raspberry Pi stays cool (add heatsink if needed)

## Safety Notes

⚠️ **Important Safety Guidelines:**

- Never exceed load cell maximum capacity
- Use proper power supply (avoid cheap adapters)
- Ensure good ventilation for Raspberry Pi
- Keep liquids away from electronics
- Disconnect power before making wiring changes

## Upgrades and Alternatives

### Performance Upgrades

- Use Raspberry Pi 4 8GB for better ML performance
- Add Google Coral USB Accelerator for faster inference
- Use higher resolution camera for better detection

### Alternative Components

- **Arduino + Raspberry Pi**: Use Arduino for sensor readings
- **ESP32**: Wireless sensor option
- **Industrial Load Cells**: For commercial applications

## Component Suppliers

- Raspberry Pi: Official distributors, Adafruit, SparkFun
- HX711 & Load Cells: Amazon, AliExpress, local electronics stores
- Cameras: Official store, Amazon

---

For software setup and configuration, see [README.md](README.md) and [QUICKSTART.md](QUICKSTART.md).
