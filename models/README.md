# Models Directory

This directory stores YOLO model weight files.

## Supported Models

### YOLOv8 (Recommended)
- **yolov8n.pt**: Nano - Fastest, lowest accuracy (6.3MB)
- **yolov8s.pt**: Small - Good balance (22MB)
- **yolov8m.pt**: Medium - Better accuracy (52MB)
- **yolov8l.pt**: Large - High accuracy (88MB)
- **yolov8x.pt**: Extra Large - Best accuracy (136MB)

### YOLOv5
- **yolov5n.pt**: Nano
- **yolov5s.pt**: Small
- **yolov5m.pt**: Medium
- **yolov5l.pt**: Large
- **yolov5x.pt**: Extra Large

## Download Models

### Option 1: Automatic Download (Recommended)
The model will be automatically downloaded on first run if using ultralytics:
```python
from ultralytics import YOLO
model = YOLO('yolov8n.pt')  # Downloads automatically if not present
```

### Option 2: Manual Download

**YOLOv8:**
```bash
# From the project root
cd models/

# Download nano model (recommended for Raspberry Pi)
wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt

# Or download small model
wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8s.pt
```

**YOLOv5:**
```bash
cd models/
wget https://github.com/ultralytics/yolov5/releases/download/v7.0/yolov5s.pt
```

## Custom Models

If you train your own YOLO model for specific products:

1. Place your trained model (.pt file) in this directory
2. Update `config/settings.json` to point to your model:
   ```json
   {
     "yolo": {
       "model": "models/my_custom_model.pt"
     }
   }
   ```

## Model Selection Guide

Choose based on your hardware:

| Hardware | Recommended Model | FPS | Accuracy |
|----------|------------------|-----|----------|
| Raspberry Pi 3 | yolov8n.pt | 2-5 | Good |
| Raspberry Pi 4 | yolov8s.pt | 5-10 | Better |
| Jetson Nano | yolov8m.pt | 15-20 | High |
| Desktop (no GPU) | yolov8m.pt | 10-15 | High |
| Desktop (with GPU) | yolov8l.pt | 30+ | Very High |

## Training Custom Models

To train a model for your specific products:

1. **Collect Images**: 
   - 100-500 images per product
   - Various angles, lighting, backgrounds

2. **Annotate Images**:
   - Use Roboflow, LabelImg, or CVAT
   - Create bounding boxes and labels

3. **Train**:
   ```bash
   # Using ultralytics
   yolo train data=my_data.yaml model=yolov8n.pt epochs=100
   ```

4. **Export trained model** to this directory

## File Size Considerations

Models can be large. The .gitignore file excludes .pt files by default to avoid committing them to the repository.

To share models:
- Use Git LFS for version control
- Host on cloud storage (Google Drive, Dropbox)
- Provide download links in documentation

## Verify Model

Test your model:
```python
from ultralytics import YOLO

# Load model
model = YOLO('models/yolov8n.pt')

# Test on image
results = model('test_image.jpg')
results.show()
```

## Troubleshooting

### Model not loading
- Check file exists in models/ directory
- Verify filename in config matches actual file
- Ensure ultralytics is installed: `pip install ultralytics`

### Out of memory errors
- Use smaller model (nano instead of small)
- Reduce image resolution
- Close other applications

### Poor detection accuracy
- Use larger model if hardware allows
- Train custom model for your products
- Improve lighting conditions
- Adjust confidence threshold

## See Also

- [Ultralytics Documentation](https://docs.ultralytics.com/)
- [YOLOv5 Repository](https://github.com/ultralytics/yolov5)
- [YOLOv8 Repository](https://github.com/ultralytics/ultralytics)
