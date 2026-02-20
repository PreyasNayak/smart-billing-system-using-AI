# Contributing to Smart Billing System Using AI

Thank you for your interest in contributing to the Smart Billing System! This document provides guidelines and instructions for contributing.

## 🌟 Ways to Contribute

- Report bugs and issues
- Suggest new features or enhancements
- Improve documentation
- Submit bug fixes
- Add new features
- Optimize existing code
- Write tests

## 🐛 Reporting Bugs

Before creating a bug report, please check existing issues to avoid duplicates.

When reporting a bug, include:

- **Description**: Clear description of the bug
- **Steps to Reproduce**: Detailed steps to reproduce the issue
- **Expected Behavior**: What you expected to happen
- **Actual Behavior**: What actually happened
- **Environment**: 
  - OS and version
  - Python version
  - Hardware (Raspberry Pi model, camera type, load cell model)
  - Relevant library versions
- **Screenshots/Logs**: If applicable
- **Additional Context**: Any other relevant information

### Bug Report Template

```markdown
**Description**
A clear description of the bug.

**Steps to Reproduce**
1. Step one
2. Step two
3. ...

**Expected Behavior**
What should happen.

**Actual Behavior**
What actually happens.

**Environment**
- OS: [e.g., Raspberry Pi OS Bullseye]
- Python: [e.g., 3.9.2]
- Hardware: [e.g., Raspberry Pi 4B, Pi Camera V2]

**Screenshots/Logs**
Add screenshots or log files if applicable.
```

## 💡 Suggesting Features

We welcome feature suggestions! Please:

1. Check if the feature has already been suggested
2. Clearly describe the feature and its benefits
3. Provide use cases
4. Consider implementation complexity

### Feature Request Template

```markdown
**Feature Description**
Clear description of the proposed feature.

**Use Case**
Why is this feature needed? What problem does it solve?

**Proposed Implementation**
(Optional) Ideas on how this could be implemented.

**Alternatives Considered**
(Optional) Alternative solutions you've considered.
```

## 🔧 Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR-USERNAME/smart-billing-system-using-AI.git
cd smart-billing-system-using-AI
```

### 2. Set Up Development Environment

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies (if available)
pip install -r requirements-dev.txt
```

### 3. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

## 📝 Coding Standards

### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and concise
- Maximum line length: 100 characters

### Example Code Style

```python
def detect_object(image, model, confidence_threshold=0.5):
    """
    Detect objects in an image using YOLO model.
    
    Args:
        image (numpy.ndarray): Input image
        model: YOLO model instance
        confidence_threshold (float): Minimum confidence for detection
        
    Returns:
        list: Detected objects with bounding boxes and labels
    """
    # Implementation here
    pass
```

### Code Quality Tools

```bash
# Format code with black (if used)
black src/

# Check code style with flake8 (if used)
flake8 src/

# Type checking with mypy (if used)
mypy src/
```

## ✅ Testing

### Writing Tests

- Write tests for new features
- Ensure existing tests pass
- Aim for good test coverage
- Use descriptive test names

### Running Tests

```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest tests/test_detector.py

# Run with coverage
python -m pytest --cov=src tests/
```

### Test Structure

```python
import pytest
from src.detector import ObjectDetector

class TestObjectDetector:
    def test_load_model(self):
        """Test that model loads correctly."""
        detector = ObjectDetector('yolov8n.pt')
        assert detector.model is not None
        
    def test_detect_objects(self):
        """Test object detection on sample image."""
        # Test implementation
        pass
```

## 📄 Documentation

### Updating Documentation

- Update README.md if you change functionality
- Add docstrings to new functions/classes
- Update configuration examples if needed
- Include usage examples for new features

### Documentation Style

- Use clear, concise language
- Include code examples
- Add comments for complex logic
- Keep formatting consistent

## 🔄 Pull Request Process

### Before Submitting

1. ✅ Test your changes thoroughly
2. ✅ Update documentation
3. ✅ Follow coding standards
4. ✅ Write/update tests
5. ✅ Ensure all tests pass
6. ✅ Update CHANGELOG.md (if exists)

### Submitting a Pull Request

1. **Push your changes**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create Pull Request**
   - Go to the repository on GitHub
   - Click "New Pull Request"
   - Select your branch
   - Fill in the PR template

3. **PR Description Should Include**
   - What changes were made
   - Why these changes are needed
   - How to test the changes
   - Screenshots (for UI changes)
   - Related issues (use "Fixes #123")

### PR Template

```markdown
## Description
Brief description of changes.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Testing
How were these changes tested?

## Screenshots (if applicable)
Add screenshots for visual changes.

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] All tests pass
```

### Review Process

- Maintainers will review your PR
- Address any requested changes
- Once approved, your PR will be merged

## 🎯 Development Priorities

### High Priority
- Bug fixes
- Security improvements
- Documentation improvements
- Performance optimizations

### Medium Priority
- New features
- Hardware compatibility
- UI/UX improvements

### Low Priority
- Code refactoring
- Minor enhancements

## 💬 Communication

- **Issues**: For bug reports and feature requests
- **Pull Requests**: For code contributions
- **Discussions**: For questions and general discussion

## 📜 Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors.

### Expected Behavior

- Be respectful and considerate
- Welcome newcomers
- Accept constructive criticism
- Focus on what's best for the project

### Unacceptable Behavior

- Harassment or discrimination
- Trolling or insulting comments
- Personal or political attacks
- Publishing others' private information

## 🏆 Recognition

Contributors will be recognized in:
- README.md acknowledgments
- Release notes
- Project documentation

## ❓ Questions?

If you have questions about contributing:
- Check existing documentation
- Search through issues
- Open a new issue with your question

## 📚 Additional Resources

- [Python PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [YOLO Documentation](https://docs.ultralytics.com/)
- [OpenCV Tutorials](https://docs.opencv.org/master/d9/df8/tutorial_root.html)
- [Raspberry Pi Documentation](https://www.raspberrypi.org/documentation/)

---

Thank you for contributing to the Smart Billing System! 🎉
