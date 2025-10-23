# Git Setup Instructions for Personal Repository

## Step 1: Initialize Git Repository (if not already done)
```bash
cd /path/to/Resume_shortlist_application
git init
```

## Step 2: Add All Files to Git
```bash
# Add all files except those in .gitignore
git add .

# Check what files are staged
git status
```

## Step 3: Create Initial Commit
```bash
git commit -m "Initial commit: Resume Shortlisting AI Assistant

- Complete Python application for AI-powered resume analysis
- OpenAI GPT-3.5-turbo integration for intelligent scoring
- Support for DOCX and PDF file formats
- Multiple display options and export functionality
- Comprehensive skill validation and scoring system
- Interactive CLI interface with restart capability"
```

## Step 4: Create GitHub Repository
1. Go to GitHub.com
2. Click "+" → "New repository"
3. Name it: `resume-shortlisting-ai` (or your preferred name)
4. Description: "AI-powered resume shortlisting tool using OpenAI GPT"
5. Choose Public/Private as needed
6. Don't initialize with README (you already have one)
7. Click "Create repository"

## Step 5: Connect to Remote Repository
```bash
# Add your GitHub repository as remote origin
git remote add origin https://github.com/YOUR_USERNAME/resume-shortlisting-ai.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 6: Verify Upload
- Check your GitHub repository
- Ensure all files are uploaded
- config.py should NOT be there (it's in .gitignore)
- README.md should display properly

## Future Updates
```bash
# When you make changes:
git add .
git commit -m "Description of changes"
git push origin main
```

## Important Notes
- Your OpenAI API key in config.py is protected by .gitignore
- Test files are excluded but can be included if needed
- Resume and JD folder is excluded to protect private data
- Update LICENSE file with your name
- Consider making repository private if dealing with sensitive data

## Repository Structure
```
resume-shortlisting-ai/
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies  
├── config_template.py        # Configuration template
├── resume_shortlister.py     # Main application
├── openai_analyzer.py        # AI analysis engine
├── document_parser.py        # Document processing
├── resume_ranker.py         # Results display and ranking
├── .gitignore               # Git ignore rules
├── LICENSE                  # MIT License
└── CONTRIBUTING.md          # Contribution guidelines
```