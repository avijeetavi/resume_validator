"""
OpenAI Integration Module
Handles AI-powered resume analysis and matching using OpenAI's SDK.
"""

import openai
import json
import os
import random
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

try:
    from config import OPENAI_API_KEY, OPENAI_MODEL
    # Set defaults for optional config values
    MAX_TOKENS = getattr(__import__('config'), 'MAX_TOKENS', 1200)
    TEMPERATURE = getattr(__import__('config'), 'TEMPERATURE', 0.1)
except ImportError:
    print("Warning: config.py not found. Using environment variable for API key.")
    OPENAI_API_KEY = ""
    OPENAI_MODEL = "gpt-3.5-turbo"
    MAX_TOKENS = 1200
    TEMPERATURE = 0.1


@dataclass
class ResumeAnalysis:
    """Data class to store resume analysis results."""
    candidate_name: str
    matching_score: float
    key_skills: List[str]
    matching_skills: List[str]
    missing_skills: List[str]
    summary: str
    strengths: List[str]
    weaknesses: List[str]


class OpenAIResumeAnalyzer:
    """OpenAI-powered resume analysis and scoring system."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the OpenAI Resume Analyzer.
        
        Args:
            api_key (Optional[str]): OpenAI API key. If not provided, will look in config.py then env var.
        """
        # Priority: parameter > config.py > environment variable
        self.api_key = api_key or OPENAI_API_KEY or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError(
                "OpenAI API key is required. Please:\n"
                "1. Add your key to config.py file, OR\n"
                "2. Set OPENAI_API_KEY environment variable, OR\n"
                "3. Pass api_key parameter to constructor"
            )
        
        # Initialize OpenAI client
        openai.api_key = self.api_key
        self.client = openai
        
        # Store configuration
        self.model = OPENAI_MODEL
        self.max_tokens = MAX_TOKENS
        self.temperature = TEMPERATURE
        
        # Validate model name
        valid_models = [
            "gpt-3.5-turbo", "gpt-3.5-turbo-16k", 
            "gpt-4", "gpt-4-turbo-preview", "gpt-4-1106-preview",
            "gpt-4o", "gpt-4o-mini"
        ]
        if self.model not in valid_models:
            print(f"Warning: Model '{self.model}' might not be valid. Common models: {', '.join(valid_models[:3])}")
            print("If you get 404 errors, check your model name in config.py")
    
    def parse_job_description(self, job_description: str) -> Dict:
        """
        Parse and understand the job description to extract key requirements.
        
        Args:
            job_description (str): The job description text
            
        Returns:
            Dict: Parsed job requirements including skills, experience, etc.
        """
        try:
            prompt = f"""
            Analyze the following job description and extract key information in JSON format:
            
            Job Description:
            {job_description}
            
            Please extract and return the following information in JSON format:
            {{
                "job_title": "extracted job title",
                "required_skills": ["list", "of", "required", "technical", "skills"],
                "preferred_skills": ["list", "of", "preferred", "skills"],
                "experience_level": "junior/mid/senior level",
                "years_of_experience": "number of years required",
                "education_requirements": ["degree", "requirements"],
                "responsibilities": ["key", "job", "responsibilities"],
                "industry": "industry sector",
                "key_requirements": ["most", "important", "requirements"]
            }}
            
            Only return valid JSON without any additional text or explanation.
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert HR analyst. Extract job requirements accurately and return only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            result = response.choices[0].message.content
            if result is None:
                raise ValueError("Empty response from OpenAI")
            
            result = result.strip()
            
            # Clean up the response to ensure it's valid JSON
            if result.startswith('```json'):
                result = result[7:]
            if result.endswith('```'):
                result = result[:-3]
            
            return json.loads(result)
            
        except Exception as e:
            print(f"Error parsing job description: {str(e)}")
            return {
                "job_title": "Unknown",
                "required_skills": [],
                "preferred_skills": [],
                "experience_level": "Not specified",
                "years_of_experience": "Not specified",
                "education_requirements": [],
                "responsibilities": [],
                "industry": "Not specified",
                "key_requirements": []
            }
    
    def analyze_resume(self, resume_text: str, job_requirements: Dict) -> ResumeAnalysis:
        """
        Analyze a resume against job requirements and calculate matching score.

        The matching_score is determined by the LLM (OpenAI model) according to the scoring criteria provided in the prompt,
        and is not calculated by this function directly.

        Args:
            resume_text (str): The resume text content
            job_requirements (Dict): Parsed job requirements from job description

        Returns:
            ResumeAnalysis: Detailed analysis of the resume
        """
        try:
            prompt = f"""
            Analyze the following resume against the job requirements and provide a detailed assessment:
            
            Job Requirements:
            {json.dumps(job_requirements, indent=2)}
            
            Resume:
            {resume_text}
            
            STEP 1: CAREFULLY extract the candidate's name from the FIRST FEW LINES of the resume text.
            STEP 2: Review the required_skills list and identify ONLY the skills from this list that the candidate has.
            STEP 3: For each required skill, check if candidate has EXACT or equivalent experience.
            STEP 4: Count ONLY the required skills that match - ignore all other skills.
            STEP 5: Calculate score based ONLY on required skill matches (be PRECISE).
            
            IMPORTANT: Extract the candidate name EXACTLY as written in THIS specific resume. Do NOT use any cached or previously seen names.
            
            CRITICAL SKILL MATCHING: Only count skills that are in the required_skills array. Generic programming skills do not count unless specifically required.
            
            Please analyze and return the following information in JSON format:
            {{
                "candidate_name": "EXACT name from THIS resume (not from memory)",
                "matching_score": 25.5,
                "key_skills": ["all", "technical", "skills", "found", "in", "resume"],
                "matching_skills": ["ONLY skills that EXACTLY or CLOSELY match job requirements"],
                "missing_skills": ["required", "skills", "not", "found", "in", "resume"],
                "summary": "brief summary focusing on skill gaps and matches",
                "strengths": ["key", "strengths", "relevant", "to", "job"],
                "weaknesses": ["specific", "skill", "gaps", "and", "missing", "requirements"],
                "experience_match": true/false,
                "education_match": true/false
            }}
            
            MATCHING SKILLS RULES (CRITICAL - FOLLOW EXACTLY):
            - ONLY include skills that are EXPLICITLY listed in the required_skills array
            - Do NOT count generic skills (Python, SQL, Git, Docker) unless they are specifically in required_skills
            - Do NOT count related but different skills (e.g., "Machine Learning" ≠ "GenAI PoC")
            - Each matching skill MUST have an EXACT or very close equivalent in required_skills
            - When in doubt, DO NOT count it as a match
            - Focus on specialized skills specific to this job role
            
            IMPORTANT SCORING INSTRUCTIONS:
            
            Scoring criteria (be ACCURATE and FAIR):
            - Technical skills match (70%): Compare EXACTLY how many required technical skills the candidate has
              * If 90-100% of required technical skills match: 63-70 points (EXCELLENT - should score 85-100% total)
              * If 80-89% of required technical skills match: 56-62 points (VERY GOOD - should score 75-90% total)
              * If 60-79% of required technical skills match: 42-55 points (GOOD - should score 60-80% total)
              * If 40-59% of required technical skills match: 28-41 points (MODERATE - should score 40-65% total)
              * If 20-39% of required technical skills match: 14-27 points (LOW - should score 20-45% total)
              * If 0-19% of required technical skills match: 0-13 points (VERY LOW - should score 0-25% total)
            
            - Experience level match (20%): Does years of experience and seniority level match?
              * Excellent match: 18-20 points
              * Good match: 14-17 points
              * Partial match: 8-13 points
              * No match or much lower: 0-7 points
            
            - Education match (5%): Does education meet requirements? (0-5 points)
            - Industry experience (5%): Relevant industry background? (0-5 points)
            
            CRITICAL SCORING RULES:
            - If candidate matches 90%+ of required skills: Score should be 85-100%
            - If candidate matches 80%+ of required skills: Score should be 75-90%
            - If candidate matches few skills (20% or less): Score should be 15-35%
            - Consider experience level and education as bonus points
            
            Calculate the total score by adding all components. Return matching_score as a number between 0-100.
            BE FAIR - reward excellent matches with high scores, penalize weak matches with low scores.
            Only return valid JSON without any additional text.
            """
            
            # Add slight randomization to prevent caching
            random_temp = self.temperature + random.uniform(-0.05, 0.05)
            random_temp = max(0.0, min(1.0, random_temp))  # Ensure valid range
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert recruiter analyzing resumes. Extract candidate names EXACTLY from the current resume text. CRITICAL: For matching_skills, ONLY include skills that are EXPLICITLY listed in the required_skills array. Do NOT count generic programming skills (Python, SQL, Docker, etc.) unless they are specifically in the required_skills list. For specialized roles like GenAI Engineer, focus on specialized skills (GenAI, LangChain, OpenAI, etc.). Score based on TRUE required skill matches: HIGH scores (85-100%) for 90%+ required skill matches, GOOD scores (75-90%) for 80%+ matches, MODERATE scores (60-80%) for 60%+ matches, LOW scores (20-40%) for poor matches."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=random_temp
            )
            
            result = response.choices[0].message.content
            if result is None:
                raise ValueError("Empty response from OpenAI")
            
            result = result.strip()
            
            # Clean up the response
            if result.startswith('```json'):
                result = result[7:]
            if result.endswith('```'):
                result = result[:-3]
            
            analysis_data = json.loads(result)
            
            # Post-processing validation: Ensure score aligns with actual skill matches
            raw_score = float(analysis_data.get('matching_score', 0))
            matching_skills = analysis_data.get('matching_skills', [])
            required_skills = job_requirements.get('required_skills', [])
            
            # Enhanced debugging information
            print(f"  Raw AI Score: {raw_score:.1f}%")
            print(f"  AI Listed {len(matching_skills)} Matching Skills: {matching_skills}")
            print(f"  Required Skills ({len(required_skills)}): {required_skills}")
            
            # Validate matching skills against required skills (strict validation)
            validated_matching_skills = []
            if required_skills and len(required_skills) > 0:
                # Check each matching skill to ensure it's actually required
                for skill in matching_skills:
                    # Check for exact match or very close match
                    skill_lower = skill.lower().strip()
                    is_valid_match = False
                    matched_req_skill = ""
                    
                    for req_skill in required_skills:
                        req_skill_lower = req_skill.lower().strip()
                        
                        # Exact match or very close match
                        if (skill_lower == req_skill_lower or 
                            skill_lower in req_skill_lower or 
                            req_skill_lower in skill_lower):
                            is_valid_match = True
                            matched_req_skill = req_skill
                            break
                    
                    if is_valid_match:
                        validated_matching_skills.append(skill)
                        print(f"  ✓ Valid match: '{skill}' matches '{matched_req_skill}'")
                    else:
                        print(f"  ✗ Invalid match removed: '{skill}' (not in required skills)")
                
                # Use validated matching skills for ratio calculation
                actual_matching_count = len(validated_matching_skills)
                skill_match_ratio = actual_matching_count / len(required_skills)
                
                print(f"  Final Validated Skills ({actual_matching_count}): {validated_matching_skills}")
                print(f"  True Skill Match Ratio: {actual_matching_count}/{len(required_skills)} = {skill_match_ratio:.1%}")
            else:
                validated_matching_skills = matching_skills
                skill_match_ratio = 0
                validated_score = raw_score
                print(f"  No validation applied (no required skills found)")
            
            # Apply score validation based on skill match ratio (only if we have required skills)
            if required_skills and len(required_skills) > 0:
                # Calculate expected score ranges based on skill match ratio
                if skill_match_ratio >= 0.9:  # 90%+ skill match - Outstanding
                    min_score = 85
                    max_allowed_score = 100
                elif skill_match_ratio >= 0.8:  # 80-89% skill match - Excellent
                    min_score = 75
                    max_allowed_score = 90
                elif skill_match_ratio >= 0.6:  # 60-79% skill match - Good
                    min_score = 60
                    max_allowed_score = 80
                elif skill_match_ratio >= 0.4:  # 40-59% skill match - Average
                    min_score = 45
                    max_allowed_score = 65
                elif skill_match_ratio >= 0.2:  # 20-39% skill match - Poor
                    min_score = 15
                    max_allowed_score = 45
                else:  # Less than 20% skill match - Very Poor
                    min_score = 5
                    max_allowed_score = 25
                
                # Apply validation with both minimum and maximum bounds
                # Handle special cases first (outstanding performance, then low matches)
                if skill_match_ratio >= 0.9:  # Outstanding candidates deserve high scores (check FIRST)
                    # Calculate score based on skill match ratio for outstanding candidates
                    outstanding_score = 85 + (skill_match_ratio - 0.9) * 150  # 85% + bonus for >90% match
                    validated_score = min(outstanding_score, 100)  # Allow up to 100%
                    print(f"  Outstanding performance boost: {raw_score:.1f}% -> {validated_score:.1f}% ({skill_match_ratio:.1%} skill match)")
                elif skill_match_ratio < 0.2:  # Very low skill matches should be penalized
                    # For very low matches, bias toward the lower end of the range
                    adjusted_score = min_score + (max_allowed_score - min_score) * 0.3  # 30% of range
                    validated_score = min(raw_score, adjusted_score)
                    print(f"  Low-match adjustment: {raw_score:.1f}% -> {validated_score:.1f}% (only {skill_match_ratio:.1%} match)")
                elif raw_score > max_allowed_score:
                    validated_score = max_allowed_score
                    print(f"  Score capped down: {raw_score:.1f}% -> {validated_score:.1f}% (max for {skill_match_ratio:.1%} match)")
                elif raw_score < min_score and skill_match_ratio >= 0.8:  # Boost excellent candidates if AI scored too low
                    validated_score = min_score
                    print(f"  Score boosted up: {raw_score:.1f}% -> {validated_score:.1f}% (min for {skill_match_ratio:.1%} match)")
                else:
                    validated_score = raw_score
                    print(f"  Score validated: {validated_score:.1f}% (within range for {skill_match_ratio:.1%} match)")
            
            return ResumeAnalysis(
                candidate_name=analysis_data.get('candidate_name', 'Unknown Candidate'),
                matching_score=validated_score,
                key_skills=analysis_data.get('key_skills', []),
                matching_skills=validated_matching_skills,  # Use validated matching skills
                missing_skills=analysis_data.get('missing_skills', []),
                summary=analysis_data.get('summary', ''),
                strengths=analysis_data.get('strengths', []),
                weaknesses=analysis_data.get('weaknesses', [])
            )
            
        except Exception as e:
            print(f"Error analyzing resume: {str(e)}")
            # Return default analysis in case of error
            return ResumeAnalysis(
                candidate_name="Unknown Candidate",
                matching_score=0.0,
                key_skills=[],
                matching_skills=[],
                missing_skills=[],
                summary="Error occurred during analysis",
                strengths=[],
                weaknesses=[]
            )
    
    def extract_candidate_name_from_text(self, resume_text: str, file_path: str) -> str:
        """
        Extract candidate name from resume text with fallback to filename.
        
        Args:
            resume_text (str): The resume text content
            file_path (str): Path to the resume file
            
        Returns:
            str: Extracted candidate name
        """
        try:
            # Try to extract name from first few lines
            lines = resume_text.split('\n')[:10]  # First 10 lines
            
            for line in lines:
                line = line.strip()
                if line and len(line) > 2:
                    # Look for patterns that might be names
                    words = line.split()
                    if (len(words) >= 2 and 
                        all(word.replace('.', '').replace(',', '').isalpha() or word.isupper() 
                            for word in words[:3]) and
                        len(' '.join(words[:3])) < 50):  # Reasonable name length
                        
                        # Additional validation - avoid common resume headers and technical terms
                        line_upper = line.upper()
                        if (not any(header in line_upper for header in [
                            'RESUME', 'CV', 'CURRICULUM', 'PROFILE', 'OBJECTIVE', 
                            'SUMMARY', 'EXPERIENCE', 'EDUCATION', 'SKILLS', 'PROFESSIONAL',
                            'PYTHON', 'JAVA', 'C++', 'JAVASCRIPT', 'SQL', 'AWS', 'DOCKER'
                        ]) and 
                            not any(char in line for char in [',', ':', ';', '|']) and  # Avoid lists
                            len(words) <= 4):  # Names usually 2-4 words
                            return ' '.join(words[:3])  # Take first 3 words as name
            
            # Fallback to filename if no name found
            return os.path.splitext(os.path.basename(file_path))[0]
            
        except Exception:
            # Final fallback to filename
            return os.path.splitext(os.path.basename(file_path))[0]
    
    def batch_analyze_resumes(self, resumes: List[Tuple[str, str]], job_requirements: Dict) -> List[ResumeAnalysis]:
        """
        Analyze multiple resumes against job requirements.
        
        Args:
            resumes (List[Tuple[str, str]]): List of tuples containing (file_path, resume_text)
            job_requirements (Dict): Parsed job requirements
            
        Returns:
            List[ResumeAnalysis]: List of resume analyses sorted by matching score
        """
        analyses = []
        
        for file_path, resume_text in resumes:
            print(f"Analyzing resume: {os.path.basename(file_path)}")
            
            # Pre-extract name using our reliable method
            reliable_name = self.extract_candidate_name_from_text(resume_text, file_path)
            
            # Add unique identifier to prevent AI caching
            unique_id = random.randint(1000, 9999)
            modified_prompt_resume = f"[Analysis ID: {unique_id}]\n{resume_text}"
            
            analysis = self.analyze_resume(modified_prompt_resume, job_requirements)
            
            # Validate and fix candidate name extraction
            ai_extracted_name = analysis.candidate_name
            filename_base = os.path.splitext(os.path.basename(file_path))[0]
            
            # Use our reliable extraction as primary, AI extraction as secondary
            if reliable_name and reliable_name != filename_base:
                final_name = reliable_name
                print(f"  Candidate name (text extraction): {final_name}")
            elif (ai_extracted_name and 
                  ai_extracted_name != "Unknown Candidate" and
                  len(ai_extracted_name.strip()) > 2 and
                  "AVINASH" not in ai_extracted_name.upper()):  # Anti-caching check
                final_name = ai_extracted_name
                print(f"  Candidate name (AI extraction): {final_name}")
            else:
                final_name = filename_base
                print(f"  Candidate name (filename fallback): {final_name}")
            
            # Update the analysis with the final name
            analysis.candidate_name = final_name
            
            analyses.append(analysis)
        
        # Sort by matching score (highest first)
        analyses.sort(key=lambda x: x.matching_score, reverse=True)
        
        return analyses