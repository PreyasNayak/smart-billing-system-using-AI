# Source Code Directory

This directory contains the main source code modules for the Smart Billing System.

## Recommended Structure

```
src/
├── __init__.py           # Package initialization
├── detector.py           # Object detection using YOLO
├── scale.py              # Load cell reading (HX711)
├── billing.py            # Invoice generation
├── config.py             # Configuration management
├── database.py           # Database operations (optional)
├── utils.py              # Utility functions
└── logger.py             # Logging setup
```

## Module Descriptions

### detector.py
Handles object detection using YOLO model:
- Load and initialize YOLO model
- Process camera frames
- Detect objects and return bounding boxes
- Filter detections by confidence threshold

### scale.py
Manages load cell operations:
- Initialize HX711 connection
- Read weight values
- Apply calibration
- Handle tare/zero operations

### billing.py
Generates invoices and bills:
- Calculate prices based on weight and product
- Apply taxes
- Generate PDF invoices
- Save transaction records

### config.py
Configuration management:
- Load settings from JSON files
- Validate configuration
- Provide default values
- Handle environment variables

### utils.py
Common utility functions:
- Image processing helpers
- Data validation
- File I/O operations
- Date/time formatting

## Getting Started

1. Create your module files in this directory
2. Use the examples in `/examples` as templates
3. Follow Python best practices and PEP 8 style guide
4. Add docstrings to all functions and classes
5. Write unit tests in `/tests` directory

## Example Module Template

```python
"""
Module: detector.py
Description: Object detection using YOLO
"""

import cv2
import numpy as np
from ultralytics import YOLO

class ObjectDetector:
    """YOLO-based object detector."""
    
    def __init__(self, model_path, confidence=0.5):
        """
        Initialize the detector.
        
        Args:
            model_path (str): Path to YOLO model file
            confidence (float): Confidence threshold
        """
        self.model = YOLO(model_path)
        self.confidence = confidence
    
    def detect(self, image):
        """
        Detect objects in an image.
        
        Args:
            image (np.ndarray): Input image
            
        Returns:
            list: Detected objects
        """
        results = self.model(image, conf=self.confidence)
        return results
```

## Development Guidelines

- Keep modules focused on single responsibility
- Write comprehensive docstrings
- Add type hints where applicable
- Handle errors gracefully
- Write unit tests
- Keep functions small and readable

## See Also

- [CONTRIBUTING.md](../CONTRIBUTING.md) for contribution guidelines
- [README.md](../README.md) for overall project documentation
- Examples in `/examples` directory
