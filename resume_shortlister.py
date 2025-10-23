"""
Resume Shortlisting AI Assistant - Main Application
A web-based application that intelligently shortlists resumes by comparing them against job descriptions using OpenAI's SDK.

Usage:
    python resume_shortlister.py

Make sure to set your OPENAI_API_KEY environment variable before running.
"""

import os
import glob
from typing import List, Tuple
from document_parser import DocumentParser
from openai_analyzer import OpenAIResumeAnalyzer, ResumeAnalysis
from resume_ranker import ResumeRanker, ScoreCalculator
from colorama import init, Fore, Style, Back

try:
    from config import OPENAI_API_KEY
except ImportError:
    print("Warning: config.py not found. Will try environment variable.")
    OPENAI_API_KEY = ""

# Initialize colorama for colored output
init(autoreset=True)


class ResumeShortlister:
    """Main application class for resume shortlisting."""
    
    def __init__(self, api_key: str | None = None):
        """
        Initialize the Resume Shortlister application.
        
        Args:
            api_key (str): OpenAI API key. If not provided, will use environment variable.
        """
        self.document_parser = DocumentParser()
        self.analyzer = OpenAIResumeAnalyzer(api_key)
        self.ranker = ResumeRanker()
        
        print(f"{Back.BLUE}{Fore.WHITE} Resume Shortlisting AI Assistant {Style.RESET_ALL}")
        print(f"{Fore.CYAN}Powered by OpenAI GPT-3.5-turbo{Style.RESET_ALL}\n")
    
    def get_job_description(self) -> Tuple[str, str]:
        """
        Get job description file from user input.
        
        Returns:
            Tuple[str, str]: (file_path, job_description_text)
        """
        while True:
            print(f"{Fore.YELLOW}📋 JOB DESCRIPTION{Style.RESET_ALL}")
            job_file = input(f"{Fore.WHITE}Enter path to job description file (.docx/.pdf): {Style.RESET_ALL}").strip()
            
            if not job_file:
                print(f"{Fore.RED}Please provide a file path.{Style.RESET_ALL}")
                continue
            
            # Expand user path and handle relative paths
            job_file = os.path.expanduser(job_file)
            if not os.path.isabs(job_file):
                job_file = os.path.abspath(job_file)
            
            if not self.document_parser.validate_file(job_file):
                print(f"{Fore.RED}Invalid file. Please provide a valid .docx file.{Style.RESET_ALL}")
                continue
            
            job_description = self.document_parser.read_job_description(job_file)
            if job_description:
                print(f"{Fore.GREEN}✓ Job description loaded successfully!{Style.RESET_ALL}")
                print(f"{Fore.CYAN}Preview: {job_description[:200]}...{Style.RESET_ALL}\n")
                return job_file, job_description
            else:
                print(f"{Fore.RED}Error reading job description file.{Style.RESET_ALL}")
    
    def get_resume_files(self) -> List[Tuple[str, str]]:
        """
        Get resume files from user input.
        
        Returns:
            List[Tuple[str, str]]: List of (file_path, resume_text) tuples
        """
        resumes = []
        
        while True:
            print(f"{Fore.YELLOW}📄 RESUME FILES{Style.RESET_ALL}")
            print("Options:")
            print("1. Enter single resume file path")
            print("2. Enter directory containing resume files")
            print("3. Enter file pattern (e.g., /path/to/resumes/*.docx or *.pdf)")
            
            choice = input(f"{Fore.WHITE}Select option (1-3): {Style.RESET_ALL}").strip()
            
            if choice == "1":
                resume_file = input(f"{Fore.WHITE}Enter resume file path (.docx/.pdf): {Style.RESET_ALL}").strip()
                resume_file = os.path.expanduser(resume_file)
                if not os.path.isabs(resume_file):
                    resume_file = os.path.abspath(resume_file)
                
                if self.document_parser.validate_file(resume_file):
                    resume_text = self.document_parser.read_resume(resume_file)
                    if resume_text:
                        resumes.append((resume_file, resume_text))
                        print(f"{Fore.GREEN}✓ Resume loaded: {os.path.basename(resume_file)}{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}Error reading resume file.{Style.RESET_ALL}")
                        continue
                else:
                    print(f"{Fore.RED}Invalid resume file.{Style.RESET_ALL}")
                    continue
            
            elif choice == "2":
                directory = input(f"{Fore.WHITE}Enter directory path: {Style.RESET_ALL}").strip()
                directory = os.path.expanduser(directory)
                if not os.path.isabs(directory):
                    directory = os.path.abspath(directory)
                
                if not os.path.isdir(directory):
                    print(f"{Fore.RED}Invalid directory path.{Style.RESET_ALL}")
                    continue
                
                # Find all .docx and .pdf files in directory
                docx_files = glob.glob(os.path.join(directory, "*.docx"))
                pdf_files = glob.glob(os.path.join(directory, "*.pdf"))
                files = docx_files + pdf_files
                
                if not files:
                    print(f"{Fore.RED}No .docx or .pdf files found in directory.{Style.RESET_ALL}")
                    continue
                
                for file_path in files:
                    resume_text = self.document_parser.read_resume(file_path)
                    if resume_text:
                        resumes.append((file_path, resume_text))
                        print(f"{Fore.GREEN}✓ Resume loaded: {os.path.basename(file_path)}{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}Error reading: {os.path.basename(file_path)}{Style.RESET_ALL}")
            
            elif choice == "3":
                pattern = input(f"{Fore.WHITE}Enter file pattern: {Style.RESET_ALL}").strip()
                pattern = os.path.expanduser(pattern)
                
                files = glob.glob(pattern)
                if not files:
                    print(f"{Fore.RED}No files found matching pattern.{Style.RESET_ALL}")
                    continue
                
                for file_path in files:
                    if self.document_parser.validate_file(file_path):
                        resume_text = self.document_parser.read_resume(file_path)
                        if resume_text:
                            resumes.append((file_path, resume_text))
                            print(f"{Fore.GREEN}✓ Resume loaded: {os.path.basename(file_path)}{Style.RESET_ALL}")
                        else:
                            print(f"{Fore.RED}Error reading: {os.path.basename(file_path)}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Invalid choice. Please select 1, 2, or 3.{Style.RESET_ALL}")
                continue
            
            # Ask if user wants to add more resumes
            if resumes:
                add_more = input(f"\n{Fore.WHITE}Add more resumes? (y/n): {Style.RESET_ALL}").strip().lower()
                if add_more not in ['y', 'yes']:
                    break
            else:
                print(f"{Fore.RED}No resumes loaded. Please try again.{Style.RESET_ALL}")
        
        print(f"\n{Fore.GREEN}✓ Total resumes loaded: {len(resumes)}{Style.RESET_ALL}")
        return resumes
    
    def analyze_and_rank(self, job_description: str, resumes: List[Tuple[str, str]]) -> List[ResumeAnalysis]:
        """
        Analyze and rank resumes against job description.
        
        Args:
            job_description (str): Job description text
            resumes (List[Tuple[str, str]]): List of resume file paths and texts
            
        Returns:
            List[ResumeAnalysis]: Ranked list of resume analyses
        """
        print(f"\n{Back.YELLOW}{Fore.BLACK} ANALYSIS IN PROGRESS {Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")
        
        # Step 1: Parse job description
        print(f"{Fore.WHITE}🔍 Parsing job description...{Style.RESET_ALL}")
        job_requirements = self.analyzer.parse_job_description(job_description)
        print(f"{Fore.GREEN}✓ Job requirements extracted{Style.RESET_ALL}")
        
        # Display parsed job info
        print(f"\n{Fore.CYAN}Job Details:{Style.RESET_ALL}")
        print(f"  Title: {job_requirements.get('job_title', 'Not specified')}")
        print(f"  Required Skills: {len(job_requirements.get('required_skills', []))} skills")
        print(f"  Experience Level: {job_requirements.get('experience_level', 'Not specified')}")
        
        # Step 2: Analyze resumes
        print(f"\n{Fore.WHITE}🤖 Analyzing resumes with AI...{Style.RESET_ALL}")
        analyses = self.analyzer.batch_analyze_resumes(resumes, job_requirements)
        print(f"{Fore.GREEN}✓ All resumes analyzed{Style.RESET_ALL}")
        
        # Step 3: Rank results
        print(f"{Fore.WHITE}📊 Ranking candidates...{Style.RESET_ALL}")
        ranked_analyses = self.ranker.rank_resumes(analyses)
        print(f"{Fore.GREEN}✓ Ranking complete{Style.RESET_ALL}")
        
        return ranked_analyses
    
    def display_results(self, analyses: List[ResumeAnalysis]):
        """
        Display analysis results in multiple formats.
        
        Args:
            analyses (List[ResumeAnalysis]): List of resume analyses
        """
        if not analyses:
            print(f"{Fore.RED}No results to display.{Style.RESET_ALL}")
            return
        
        while True:
            print(f"\n{Back.GREEN}{Fore.BLACK} RESULTS DISPLAY OPTIONS {Style.RESET_ALL}")
            print("1. Summary Table          (Quick overview in tabular format)")
            print("2. Score Distribution     (Statistical analysis of scores)")
            print("3. Detailed Rankings      (In-depth analysis of each candidate)")
            print("4. Show All               (Complete report with all views)")
            print("5. Save Results to File   (Export analysis to text file)")
            print("6. Start Again            (Restart with new job/resumes)")
            print("7. Exit                   (Close the application)")
            
            choice = input(f"\n{Fore.WHITE}Select display option (1-7): {Style.RESET_ALL}").strip()
            
            if choice == "1":
                self.ranker.display_rankings(analyses)
            elif choice == "2":
                self.ranker.display_summary_table(analyses)
            elif choice == "3":
                self.ranker.display_score_distribution(analyses)
            elif choice == "4":
                filename = input(f"{Fore.WHITE}Enter filename (default: resume_analysis_results.txt): {Style.RESET_ALL}").strip()
                if not filename:
                    filename = "resume_analysis_results.txt"
                self.ranker.save_results_to_file(analyses, filename)
            elif choice == "5":
                self.ranker.display_summary_table(analyses)
                self.ranker.display_score_distribution(analyses)
                self.ranker.display_rankings(analyses)
            elif choice == "6":
                return "restart"  # Signal to restart from beginning
            elif choice == "7":
                break
            else:
                print(f"{Fore.RED}Invalid choice. Please select 1-7.{Style.RESET_ALL}")
    
    def run(self):
        """Run the complete resume shortlisting workflow."""
        while True:
            try:
                # Step 1: Get job description
                job_file, job_description = self.get_job_description()
                
                # Step 2: Get resume files
                resumes = self.get_resume_files()
                
                if not resumes:
                    print(f"{Fore.RED}No resumes to analyze. Exiting.{Style.RESET_ALL}")
                    return
                
                # Step 3: Analyze and rank
                analyses = self.analyze_and_rank(job_description, resumes)
                
                # Step 4: Display results
                result = self.display_results(analyses)
                
                if result == "restart":
                    print(f"\n{Fore.CYAN}🔄 Starting fresh analysis...{Style.RESET_ALL}\n")
                    continue  # Restart from the beginning
                else:
                    print(f"\n{Fore.GREEN}✨ Resume shortlisting completed successfully!{Style.RESET_ALL}")
                    break  # Exit normally
                
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}Process interrupted by user.{Style.RESET_ALL}")
                break
            except Exception as e:
                print(f"\n{Fore.RED}An error occurred: {str(e)}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Please check your inputs and try again.{Style.RESET_ALL}")
                
                # Ask if user wants to try again
                retry = input(f"\n{Fore.WHITE}Would you like to start over? (y/n): {Style.RESET_ALL}").strip().lower()
                if retry != 'y' and retry != 'yes':
                    break


def main():
    """Main function to run the resume shortlister."""
    # Check for OpenAI API key in config file first, then environment
    api_key = OPENAI_API_KEY or os.getenv('OPENAI_API_KEY')
    if not api_key:
        print(f"{Fore.RED}Error: OpenAI API key not found!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Please add your API key to config.py file:{Style.RESET_ALL}")
        print(f"{Fore.WHITE}1. Open config.py{Style.RESET_ALL}")
        print(f"{Fore.WHITE}2. Set: OPENAI_API_KEY = \"your_actual_api_key_here\"{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Alternatively, set environment variable: $env:OPENAI_API_KEY=\"your_key\"{Style.RESET_ALL}")
        return
    
    # Initialize and run the application
    app = ResumeShortlister(api_key)
    app.run()


if __name__ == "__main__":
    main()