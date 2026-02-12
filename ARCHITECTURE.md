# System Architecture

This document describes the architecture and data flow of the Smart Billing System.

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    Smart Billing System                         │
│                                                                 │
│  ┌──────────────┐         ┌──────────────┐                    │
│  │   Camera     │         │  Load Cell   │                    │
│  │  (Vision)    │         │  (Weight)    │                    │
│  └──────┬───────┘         └──────┬───────┘                    │
│         │                        │                             │
│         │                        │                             │
│         ▼                        ▼                             │
│  ┌──────────────┐         ┌──────────────┐                    │
│  │   YOLO ML    │         │   HX711      │                    │
│  │   Detector   │         │   Reader     │                    │
│  └──────┬───────┘         └──────┬───────┘                    │
│         │                        │                             │
│         └────────┬───────────────┘                             │
│                  │                                             │
│                  ▼                                             │
│         ┌─────────────────┐                                    │
│         │  Main Control   │                                    │
│         │     Logic       │                                    │
│         └────────┬────────┘                                    │
│                  │                                             │
│        ┌─────────┼─────────┐                                   │
│        │         │         │                                   │
│        ▼         ▼         ▼                                   │
│  ┌─────────┐ ┌────────┐ ┌─────────┐                          │
│  │Product  │ │Billing │ │Display  │                          │
│  │Database │ │Engine  │ │/Output  │                          │
│  └─────────┘ └────────┘ └─────────┘                          │
│                  │                                             │
│                  ▼                                             │
│         ┌────────────────┐                                     │
│         │    Invoice     │                                     │
│         │   Generator    │                                     │
│         └────────────────┘                                     │
└─────────────────────────────────────────────────────────────────┘
```

## Component Architecture

### 1. Input Layer

#### Camera Module
- **Purpose**: Capture visual data of products
- **Technologies**: OpenCV, Pi Camera/USB Camera
- **Output**: Image frames (BGR format)

#### Load Cell Module
- **Purpose**: Measure product weight
- **Technologies**: HX711 ADC, GPIO
- **Output**: Weight in grams/kilograms

### 2. Processing Layer

#### Object Detector
- **Purpose**: Identify products in images
- **Technologies**: YOLO (v5/v8), PyTorch
- **Input**: Image frames from camera
- **Output**: Detected objects with labels and confidence scores
- **Key Features**:
  - Real-time detection
  - Multiple object support
  - Confidence filtering

#### Weight Reader
- **Purpose**: Read and calibrate weight measurements
- **Technologies**: HX711 Python library
- **Input**: Raw ADC values
- **Output**: Calibrated weight readings
- **Key Features**:
  - Tare/zero functionality
  - Calibration support
  - Noise filtering

### 3. Business Logic Layer

#### Main Controller
- **Purpose**: Orchestrate system operations
- **Responsibilities**:
  - Initialize components
  - Coordinate data flow
  - Handle errors
  - Manage state

#### Product Database
- **Purpose**: Store product information and prices
- **Format**: JSON (or database)
- **Data**:
  - Product names
  - Prices per unit
  - Categories
  - Tax rates

#### Billing Engine
- **Purpose**: Calculate costs and generate bills
- **Calculations**:
  - Base price = price_per_kg × weight
  - Tax = base_price × tax_rate
  - Total = base_price + tax

### 4. Output Layer

#### Invoice Generator
- **Purpose**: Create formatted invoices
- **Technologies**: ReportLab, FPDF
- **Output Formats**:
  - PDF documents
  - Text files
  - Display output

## Data Flow

### Normal Operation Flow

```
1. System Initialization
   ├── Load configuration
   ├── Initialize camera
   ├── Initialize load cell
   ├── Load YOLO model
   └── Load product database

2. Main Loop (Continuous)
   ├── Capture image from camera
   ├── Detect objects using YOLO
   │   └── Filter by confidence threshold
   ├── Read weight from load cell
   │   └── Apply calibration
   ├── Match detection with product database
   ├── If match found:
   │   ├── Calculate price (weight × price_per_kg)
   │   ├── Calculate tax
   │   ├── Generate invoice
   │   └── Save/display invoice
   └── Continue monitoring

3. Shutdown
   ├── Close camera
   ├── Clean up GPIO
   └── Save logs
```

### Transaction Processing Flow

```
┌──────────────┐
│ Item Placed  │
│  on Scale    │
└──────┬───────┘
       │
       ▼
┌──────────────────┐      ┌───────────────┐
│  Camera Capture  │──────│ Load Cell     │
│  (Image Frame)   │      │ (Weight Read) │
└──────┬───────────┘      └───────┬───────┘
       │                          │
       ▼                          │
┌──────────────────┐              │
│  YOLO Detection  │              │
│  (Product ID)    │              │
└──────┬───────────┘              │
       │                          │
       ▼                          │
┌──────────────────┐              │
│ Product Lookup   │              │
│ (Price Info)     │              │
└──────┬───────────┘              │
       │                          │
       └──────────┬───────────────┘
                  │
                  ▼
       ┌──────────────────┐
       │  Calculate Price  │
       │  (Price × Weight) │
       └──────┬───────────┘
              │
              ▼
       ┌──────────────────┐
       │  Add Tax         │
       │  (Price × Rate)  │
       └──────┬───────────┘
              │
              ▼
       ┌──────────────────┐
       │ Generate Invoice │
       │  (PDF/Display)   │
       └──────────────────┘
```

## Module Dependencies

```
main.py
├── src/detector.py
│   ├── ultralytics (YOLO)
│   ├── opencv-python (cv2)
│   └── torch
├── src/scale.py
│   ├── HX711
│   └── RPi.GPIO
├── src/billing.py
│   ├── reportlab
│   └── datetime
├── src/config.py
│   └── json
└── src/utils.py
    ├── numpy
    └── PIL
```

## Configuration Flow

```
┌─────────────────────┐
│  config/            │
│  ├── settings.json  │──┐
│  └── products.json  │  │
└─────────────────────┘  │
                         │
                         ▼
                  ┌──────────────┐
                  │ Config Loader│
                  └──────┬───────┘
                         │
          ┌──────────────┼──────────────┐
          │              │              │
          ▼              ▼              ▼
    ┌─────────┐    ┌─────────┐   ┌──────────┐
    │ Camera  │    │  YOLO   │   │  Scale   │
    │ Config  │    │ Config  │   │  Config  │
    └─────────┘    └─────────┘   └──────────┘
```

## Error Handling Strategy

```
Try:
    ├── Initialize components
    ├── Main processing loop
    └── Clean shutdown
Except:
    ├── CameraError
    │   └── Log error, try fallback camera
    ├── LoadCellError
    │   └── Log error, recalibrate
    ├── DetectionError
    │   └── Log error, continue monitoring
    └── GeneralError
        └── Log error, notify user
Finally:
    └── Clean up resources
```

## Scalability Considerations

### Single Product Mode (Current)
- One item at a time
- Simple linear processing
- Suitable for small-scale operations

### Multi-Product Mode (Future)
- Multiple items simultaneously
- Parallel detection processing
- Region-of-interest segmentation
- Individual weight estimation

### Performance Optimization

```
Current:
Camera → YOLO → Weight → Billing
(Sequential, ~5-10 FPS)

Optimized:
Camera ──┬→ YOLO (Thread 1)
         └→ Weight (Thread 2)
            ↓
         Billing (Main Thread)
(Parallel, ~15-20 FPS)
```

## Hardware Integration

### GPIO Pin Mapping
```
Raspberry Pi GPIO
├── Pin 2  (5V)     → HX711 VCC
├── Pin 6  (GND)    → HX711 GND
├── Pin 29 (GPIO 5) → HX711 DT
└── Pin 31 (GPIO 6) → HX711 SCK
```

### Camera Interface
```
CSI Port → Pi Camera Module
USB Port → USB Webcam
```

## Security Considerations

1. **Data Privacy**: Invoice data stored locally
2. **Access Control**: File system permissions
3. **Input Validation**: Sanitize all inputs
4. **Error Messages**: Don't expose system details
5. **Logging**: Secure log storage

## Future Architecture Enhancements

### Cloud Integration
```
Local System → API Gateway → Cloud Storage
                          → Analytics Engine
                          → Backup System
```

### Database Integration
```
Transactions → Database → Reports
                       → Analytics
                       → Audit Trail
```

### API Architecture
```
REST API
├── GET  /products
├── POST /transaction
├── GET  /invoices
└── GET  /analytics
```

## See Also

- [README.md](README.md) - General documentation
- [HARDWARE.md](HARDWARE.md) - Hardware setup details
- [CONTRIBUTING.md](CONTRIBUTING.md) - Development guidelines
- [ROADMAP.md](ROADMAP.md) - Future plans
