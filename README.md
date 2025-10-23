# Resume Shortlisting AI Assistant

A Python application that intelligently shortlists resumes by comparing them against job descriptions using OpenAI's GPT-3.5-turbo model. This tool automates and enhances the resume screening process for recruiters and hiring managers.

## 🚀 Quick Start

```bash
# Clone the repository
git clone <your-repo-url>
cd resume-shortlisting-ai

# Set up virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up your OpenAI API key in config.py
# Run the application
python resume_shortlister.py
```

## Features

- **Document Processing**: Reads DOC/DOCX and PDF files for job descriptions and resumes
- **AI-Powered Analysis**: Uses OpenAI SDK to parse job requirements and analyze resumes
- **Intelligent Scoring**: Calculates matching percentages based on skills, experience, and education
- **Comprehensive Ranking**: Ranks resumes from most relevant to least relevant
- **Detailed Output**: Shows matching skills, missing skills, strengths, and areas for improvement
- **Multiple Display Options**: Summary table, detailed rankings, and score distribution
- **Export Functionality**: Save results to text files for further review

## Installation

1. **Clone or download this repository**

2. **Set up Python environment** (Python 3.8+ required):
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

3. **Install required packages**:
   ```powershell
   pip install -r requirements.txt
   ```

4. **Set up OpenAI API Key**:
   - Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys)
   - **Option 1 (Recommended)**: Add to config file:
     - Open `config.py`
     - Set: `OPENAI_API_KEY = "your_actual_api_key_here"`
   - **Option 2**: Use environment variable:
     ```powershell
     $env:OPENAI_API_KEY="your_api_key_here"
     ```

## Usage

### Interactive Mode (Recommended)

Run the main application:
```powershell
python resume_shortlister.py
```

The application will guide you through:
1. Uploading job description file (.docx/.pdf)
2. Selecting resume files (single file, directory, or pattern)
3. AI analysis and ranking
4. Displaying results in various formats

### Programmatic Usage

For integration into other systems, see `example_usage.py`:

```python
from document_parser import DocumentParser
from openai_analyzer import OpenAIResumeAnalyzer
from resume_ranker import ResumeRanker

# Initialize components
parser = DocumentParser()
analyzer = OpenAIResumeAnalyzer(api_key="your_api_key")
ranker = ResumeRanker()

# Read and analyze
job_description = parser.read_job_description("job.docx")
job_requirements = analyzer.parse_job_description(job_description)

resumes = [(path, parser.read_resume(path)) for path in resume_paths]
analyses = analyzer.batch_analyze_resumes(resumes, job_requirements)
ranked_results = ranker.rank_resumes(analyses)

# Display results
ranker.display_summary_table(ranked_results)
```

## File Structure

```
Resume_shortlist_application/
├── resume_shortlister.py      # Main application
├── document_parser.py         # DOC/DOCX file handling
├── openai_analyzer.py        # OpenAI integration & analysis
├── resume_ranker.py          # Ranking and display logic
├── example_usage.py          # Programmatic usage example
├── config.py                 # Configuration file (API key)
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore file
├── README.md                 # This file
└── Product_requirement_document.txt
```

## Modules Overview

### 1. DocumentParser (`document_parser.py`)
- Reads and extracts text from DOC/DOCX and PDF files
- Handles both job descriptions and resumes
- Validates file formats and existence
- Uses multiple PDF parsing libraries for better text extraction

### 2. OpenAIResumeAnalyzer (`openai_analyzer.py`)
- Integrates with OpenAI GPT-3.5-turbo
- Parses job descriptions to extract requirements
- Analyzes resumes for skill matching and scoring
- Returns structured analysis with scores and insights

### 3. ResumeRanker (`resume_ranker.py`)
- Ranks resumes by matching scores
- Provides multiple display formats
- Generates colored terminal output
- Exports results to text files

### 4. Main Application (`resume_shortlister.py`)
- Interactive command-line interface
- Workflow management
- User input handling and validation

## Scoring Criteria

The AI analyzer evaluates resumes based on:

- **Technical Skills Match (40%)**: Alignment with required technical skills
- **Experience Level Match (25%)**: Years and type of experience
- **Education Match (15%)**: Degree requirements and qualifications  
- **Industry Experience (10%)**: Relevant industry background
- **Additional Skills (10%)**: Bonus points for extra relevant skills

## Output Format

### Summary Table
```
Rank  Candidate Name               Score     Top Skills Match
1     John Smith                   87.5%     Python, Machine Learning, AWS
2     Jane Doe                     82.3%     Java, Spring Boot, Docker
3     Bob Johnson                  75.1%     JavaScript, React, Node.js
```

### Detailed Rankings
- Candidate name and overall matching score
- Summary of candidate's profile
- ✓ Matching skills (highlighted in green)
- ✗ Missing skills (highlighted in red)
- ★ Key strengths
- ⚠ Areas for improvement

### Score Distribution
- Average, highest, and lowest scores
- Candidates grouped by score ranges:
  - Excellent (80-100%)
  - Good (60-79%)
  - Average (40-59%)
  - Poor (0-39%)

## Requirements

- Python 3.8 or higher
- OpenAI API key
- DOC/DOCX or PDF files for job descriptions and resumes
- Internet connection for OpenAI API calls

## Dependencies

- `openai>=1.0.0` - OpenAI Python SDK
- `python-docx>=0.8.11` - Microsoft Word document processing
- `PyPDF2>=3.0.1` - PDF document processing
- `pdfplumber>=0.9.0` - Advanced PDF text extraction
- `colorama>=0.4.6` - Cross-platform colored terminal output
- `typing-extensions>=4.0.0` - Type hints support

## Error Handling

The application handles various error scenarios:
- Invalid file formats or paths
- Missing OpenAI API key
- Network connectivity issues
- Malformed documents
- API rate limiting

## Limitations

- Supports DOC/DOCX and PDF file formats
- Requires internet connection for OpenAI API
- Analysis quality depends on document text quality
- API usage costs apply for OpenAI calls

## Future Enhancements

- Web interface (Flask/Django)
- Resume database integration
- Batch processing optimization
- Custom scoring weights
- Multiple AI model support
- Visualization charts and graphs

## Support

For issues or questions:
1. Check file formats are .docx, .doc, or .pdf
2. Verify OpenAI API key is set correctly
3. Ensure internet connectivity
4. Review error messages for specific issues

## License

This project is developed for educational and professional use. Please ensure compliance with OpenAI's usage policies when using their API.

---

**Author**: Avijeet Kumar (Product Owner)  
**Version**: 1.0  
**Last Updated**: October 2024