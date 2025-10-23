# OpenAI Configuration Template
# Copy this file to config.py and add your actual API key

# OpenAI API Configuration
OPENAI_API_KEY = "your_openai_api_key_here"  # Replace with your actual API key
OPENAI_MODEL = "gpt-3.5-turbo"
MAX_TOKENS = 1500
TEMPERATURE = 0.7

# Application Configuration  
DEFAULT_RESULTS_FILE = "resume_analysis_results.txt"
MAX_RESUMES_BATCH = 50

# Analysis Configuration
MIN_SCORE_THRESHOLD = 0
MAX_MATCHING_SKILLS_DISPLAY = 10
MAX_MISSING_SKILLS_DISPLAY = 5

# Instructions:
# 1. Get your API key from: https://platform.openai.com/api-keys
# 2. Replace "your_openai_api_key_here" with your actual key
# 3. Save this file as config.py (not config_template.py)
# 4. Never commit config.py to version control (it's in .gitignore)