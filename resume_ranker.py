"""
Resume Scoring and Display Module
Handles ranking, scoring, and visualization of resume analysis results.
"""

from typing import List
from colorama import init, Fore, Style, Back
from openai_analyzer import ResumeAnalysis
import os

# Initialize colorama for cross-platform colored output
init(autoreset=True)


class ResumeRanker:
    """Handles ranking and display of resume analysis results."""
    
    def __init__(self):
        """Initialize the resume ranker."""
        pass
    
    def rank_resumes(self, analyses: List[ResumeAnalysis]) -> List[ResumeAnalysis]:
        """
        Rank resumes by matching score (highest to lowest).
        
        Args:
            analyses (List[ResumeAnalysis]): List of resume analyses
            
        Returns:
            List[ResumeAnalysis]: Sorted list of analyses by matching score
        """
        return sorted(analyses, key=lambda x: x.matching_score, reverse=True)
    
    def get_score_color(self, score: float) -> str:
        """
        Get color code based on matching score.
        
        Args:
            score (float): Matching score (0-100)
            
        Returns:
            str: Color code for terminal output
        """
        if score >= 80:
            return Fore.GREEN
        elif score >= 60:
            return Fore.YELLOW
        elif score >= 40:
            return Fore.CYAN
        else:
            return Fore.RED
    
    def display_rankings(self, analyses: List[ResumeAnalysis]):
        """
        Display ranked resumes with detailed information.
        
        Args:
            analyses (List[ResumeAnalysis]): List of resume analyses to display
        """
        if not analyses:
            print(f"{Fore.RED}No resumes to display.{Style.RESET_ALL}")
            return
        
        print(f"\n{Back.BLUE}{Fore.WHITE} RESUME SHORTLISTING RESULTS {Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'=' * 80}{Style.RESET_ALL}")
        print(f"Total Candidates Analyzed: {len(analyses)}")
        print(f"{'=' * 80}")
        
        for i, analysis in enumerate(analyses, 1):
            score_color = self.get_score_color(analysis.matching_score)
            
            print(f"\n{Back.WHITE}{Fore.BLACK} RANK #{i} {Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
            
            # Candidate name and score
            print(f"{Fore.WHITE}Candidate: {Style.BRIGHT}{analysis.candidate_name}{Style.RESET_ALL}")
            print(f"{Fore.WHITE}Matching Score: {score_color}{Style.BRIGHT}{analysis.matching_score:.1f}%{Style.RESET_ALL}")
            
            # Summary
            if analysis.summary:
                print(f"{Fore.WHITE}Summary: {analysis.summary}{Style.RESET_ALL}")
            
            # Matching skills
            if analysis.matching_skills:
                print(f"\n{Fore.GREEN}✓ Matching Skills:{Style.RESET_ALL}")
                for skill in analysis.matching_skills[:10]:  # Show top 10
                    print(f"  {Fore.GREEN}• {skill}{Style.RESET_ALL}")
                if len(analysis.matching_skills) > 10:
                    print(f"  {Fore.GREEN}... and {len(analysis.matching_skills) - 10} more{Style.RESET_ALL}")
            
            # Missing skills
            if analysis.missing_skills:
                print(f"\n{Fore.RED}✗ Missing Skills:{Style.RESET_ALL}")
                for skill in analysis.missing_skills[:5]:  # Show top 5 missing
                    print(f"  {Fore.RED}• {skill}{Style.RESET_ALL}")
                if len(analysis.missing_skills) > 5:
                    print(f"  {Fore.RED}... and {len(analysis.missing_skills) - 5} more{Style.RESET_ALL}")
            
            # Strengths
            if analysis.strengths:
                print(f"\n{Fore.YELLOW}★ Key Strengths:{Style.RESET_ALL}")
                for strength in analysis.strengths[:3]:  # Show top 3
                    print(f"  {Fore.YELLOW}• {strength}{Style.RESET_ALL}")
            
            # Weaknesses
            if analysis.weaknesses:
                print(f"\n{Fore.MAGENTA}⚠ Areas for Improvement:{Style.RESET_ALL}")
                for weakness in analysis.weaknesses[:3]:  # Show top 3
                    print(f"  {Fore.MAGENTA}• {weakness}{Style.RESET_ALL}")
            
            print(f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
    
    def display_summary_table(self, analyses: List[ResumeAnalysis]):
        """
        Display a summary table of all candidates.
        
        Args:
            analyses (List[ResumeAnalysis]): List of resume analyses
        """
        if not analyses:
            return
        
        print(f"\n{Back.GREEN}{Fore.BLACK} CANDIDATE SUMMARY TABLE {Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'=' * 100}{Style.RESET_ALL}")
        
        # Header
        print(f"{Fore.WHITE}{Style.BRIGHT}{'Rank':<6}{'Candidate Name':<30}{'Score':<10}{'Top Skills Match':<40}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'-' * 100}{Style.RESET_ALL}")
        
        for i, analysis in enumerate(analyses, 1):
            score_color = self.get_score_color(analysis.matching_score)
            
            # Get top 3 matching skills for display
            top_skills = ', '.join(analysis.matching_skills[:3]) if analysis.matching_skills else 'None'
            if len(top_skills) > 37:
                top_skills = top_skills[:34] + "..."
            
            print(f"{Fore.WHITE}{i:<6}{analysis.candidate_name[:29]:<30}"
                  f"{score_color}{analysis.matching_score:.1f}%{Style.RESET_ALL:<7}"
                  f"{Fore.CYAN}{top_skills:<40}{Style.RESET_ALL}")
        
        print(f"{Fore.CYAN}{'-' * 100}{Style.RESET_ALL}")
    
    def display_score_distribution(self, analyses: List[ResumeAnalysis]):
        """
        Display score distribution statistics.
        
        Args:
            analyses (List[ResumeAnalysis]): List of resume analyses
        """
        if not analyses:
            return
        
        scores = [analysis.matching_score for analysis in analyses]
        
        # Calculate statistics
        avg_score = sum(scores) / len(scores)
        max_score = max(scores)
        min_score = min(scores)
        
        # Count by ranges
        excellent = len([s for s in scores if s >= 80])
        good = len([s for s in scores if 60 <= s < 80])
        average = len([s for s in scores if 40 <= s < 60])
        poor = len([s for s in scores if s < 40])
        
        print(f"\n{Back.MAGENTA}{Fore.WHITE} SCORE DISTRIBUTION {Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")
        
        print(f"{Fore.WHITE}Average Score: {Fore.YELLOW}{avg_score:.1f}%{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Highest Score: {Fore.GREEN}{max_score:.1f}%{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Lowest Score:  {Fore.RED}{min_score:.1f}%{Style.RESET_ALL}")
        
        print(f"\n{Fore.WHITE}Score Ranges:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}Excellent (80-100%): {excellent} candidates{Style.RESET_ALL}")
        print(f"  {Fore.YELLOW}Good (60-79%):      {good} candidates{Style.RESET_ALL}")
        print(f"  {Fore.CYAN}Average (40-59%):   {average} candidates{Style.RESET_ALL}")
        print(f"  {Fore.RED}Poor (0-39%):       {poor} candidates{Style.RESET_ALL}")
        
        print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")
    
    def save_results_to_file(self, analyses: List[ResumeAnalysis], output_file: str = "resume_analysis_results.txt"):
        """
        Save analysis results to a text file.
        
        Args:
            analyses (List[ResumeAnalysis]): List of resume analyses
            output_file (str): Output file name
        """
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("RESUME SHORTLISTING RESULTS\n")
                f.write("=" * 80 + "\n")
                f.write(f"Total Candidates Analyzed: {len(analyses)}\n")
                f.write("=" * 80 + "\n\n")
                
                for i, analysis in enumerate(analyses, 1):
                    f.write(f"RANK #{i}\n")
                    f.write("─" * 50 + "\n")
                    f.write(f"Candidate: {analysis.candidate_name}\n")
                    f.write(f"Matching Score: {analysis.matching_score:.1f}%\n")
                    f.write(f"Summary: {analysis.summary}\n\n")
                    
                    if analysis.matching_skills:
                        f.write("✓ Matching Skills:\n")
                        for skill in analysis.matching_skills:
                            f.write(f"  • {skill}\n")
                        f.write("\n")
                    
                    if analysis.missing_skills:
                        f.write("✗ Missing Skills:\n")
                        for skill in analysis.missing_skills:
                            f.write(f"  • {skill}\n")
                        f.write("\n")
                    
                    if analysis.strengths:
                        f.write("★ Key Strengths:\n")
                        for strength in analysis.strengths:
                            f.write(f"  • {strength}\n")
                        f.write("\n")
                    
                    if analysis.weaknesses:
                        f.write("⚠ Areas for Improvement:\n")
                        for weakness in analysis.weaknesses:
                            f.write(f"  • {weakness}\n")
                    
                    f.write("─" * 50 + "\n\n")
                
                # Add summary statistics
                scores = [analysis.matching_score for analysis in analyses]
                avg_score = sum(scores) / len(scores)
                
                f.write("SUMMARY STATISTICS\n")
                f.write("=" * 30 + "\n")
                f.write(f"Average Score: {avg_score:.1f}%\n")
                f.write(f"Highest Score: {max(scores):.1f}%\n")
                f.write(f"Lowest Score: {min(scores):.1f}%\n")
            
            print(f"\n{Fore.GREEN}✓ Results saved to: {output_file}{Style.RESET_ALL}")
            
        except Exception as e:
            print(f"{Fore.RED}Error saving results: {str(e)}{Style.RESET_ALL}")


class ScoreCalculator:
    """Utility class for score calculations and validations."""
    
    @staticmethod
    def normalize_score(score: float) -> float:
        """
        Normalize score to be between 0 and 100.
        
        Args:
            score (float): Raw score
            
        Returns:
            float: Normalized score (0-100)
        """
        return max(0.0, min(100.0, score))
    
    @staticmethod
    def calculate_weighted_score(skill_match: float, experience_match: float, 
                               education_match: float, additional_factors: float) -> float:
        """
        Calculate weighted score based on different factors.
        
        Args:
            skill_match (float): Skills matching percentage (0-100)
            experience_match (float): Experience matching percentage (0-100)
            education_match (float): Education matching percentage (0-100)
            additional_factors (float): Additional factors percentage (0-100)
            
        Returns:
            float: Weighted total score
        """
        # Weights: Skills(50%), Experience(30%), Education(15%), Others(5%)
        weighted_score = (
            skill_match * 0.5 +
            experience_match * 0.3 +
            education_match * 0.15 +
            additional_factors * 0.05
        )
        
        return ScoreCalculator.normalize_score(weighted_score)