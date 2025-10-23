# Contributing to Resume Shortlisting AI Assistant

Thank you for your interest in contributing to this project!

## Development Setup

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/resume-shortlisting-ai.git
   cd resume-shortlisting-ai
   ```

3. **Set up development environment**:
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Linux/Mac:
   source .venv/bin/activate
   
   pip install -r requirements.txt
   ```

4. **Configure API key**:
   ```bash
   cp config_template.py config.py
   # Edit config.py and add your OpenAI API key
   ```

## Making Changes

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** and test thoroughly

3. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Add: description of your changes"
   ```

4. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Create a Pull Request** on GitHub

## Code Style

- Follow PEP 8 Python style guidelines
- Use descriptive variable and function names
- Add docstrings to functions and classes
- Include type hints where appropriate

## Testing

Before submitting changes:
- Test with different file formats (DOCX, PDF)
- Test with various job descriptions and resumes
- Ensure error handling works correctly

## Areas for Contribution

- [ ] Support for more file formats
- [ ] Improved skill matching algorithms
- [ ] Better error handling and user feedback
- [ ] Performance optimizations
- [ ] UI/UX improvements
- [ ] Additional export formats
- [ ] Batch processing enhancements

## Questions?

Feel free to open an issue for any questions or suggestions!