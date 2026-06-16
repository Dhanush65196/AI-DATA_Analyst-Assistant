"""
LLM integration helper module
"""
import json
import logging
import os
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


class LLMHelper:
    """Helper class for LLM integrations"""
    
    _ALLOWED_MODELS = {"gpt-3.5-turbo", "gpt-4", "gpt-4-turbo", "gpt-4o", "gpt-4o-mini"}

    def __init__(self):
        """Initialize LLMHelper"""
        self.api_key = os.getenv("OPENAI_API_KEY")
        model = os.getenv("LLM_MODEL", "gpt-3.5-turbo")
        self.model = model if model in self._ALLOWED_MODELS else "gpt-3.5-turbo"
    
    def get_insights(self, analysis_results: Dict[str, Any]) -> str:
        """
        Generate AI insights from analysis results
        
        Args:
            analysis_results: Dictionary containing analysis results
            
        Returns:
            str: AI-generated insights
        """
        try:
            # Format analysis results for LLM
            prompt = self._format_prompt(analysis_results)
            
            # Call LLM (implementation depends on chosen provider)
            insights = self._call_llm(prompt)
            
            return insights
        except Exception:
            logger.exception("Error generating insights")
            return "Error generating insights. Please try again later."
    
    def _format_prompt(self, analysis_results: Dict[str, Any]) -> str:
        """Format analysis results into a prompt for LLM"""
        prompt = f"""
        Based on the following data analysis results, provide key insights and recommendations:
        
        Data Shape: {analysis_results.get('shape')}
        Columns: {', '.join(analysis_results.get('columns', []))}
        Missing Values: {analysis_results.get('missing_values')}
        Statistics: {json.dumps(analysis_results.get('statistics', {}), indent=2, default=str)}
        Duplicate Rows: {analysis_results.get('duplicate_rows')}
        
        Please provide:
        1. Key findings from the data
        2. Potential data quality issues
        3. Recommended next steps for analysis
        """
        return prompt.strip()
    
    def _call_llm(self, prompt: str) -> str:
        """Call LLM API with prompt"""
        # Placeholder implementation
        # In production, integrate with OpenAI, Anthropic, or other LLM providers
        
        if not self.api_key:
            return "LLM API key not configured. Please set OPENAI_API_KEY environment variable."
        
        try:
            # Example using OpenAI (uncomment when ready to use)
            # import openai
            # openai.api_key = self.api_key
            # response = openai.ChatCompletion.create(
            #     model=self.model,
            #     messages=[{"role": "user", "content": prompt}],
            #     temperature=0.7
            # )
            # return response.choices[0].message.content
            
            return "LLM integration not yet implemented"
        except Exception:
            logger.exception("Error calling LLM")
            return "Error calling LLM service. Please try again later."
    
    def generate_report(self, analysis_results: Dict[str, Any]) -> str:
        """Generate a comprehensive analysis report"""
        report = f"""
        # Data Analysis Report
        
        ## Dataset Overview
        - Shape: {analysis_results.get('shape')}
        - Total Columns: {len(analysis_results.get('columns', []))}
        
        ## Columns
        {chr(10).join([f"- {col}" for col in analysis_results.get('columns', [])])}
        
        ## Data Quality
        - Missing Values: {sum(analysis_results.get('missing_values', {}).values())}
        - Duplicate Rows: {analysis_results.get('duplicate_rows', 0)}
        
        ## Statistical Summary
        {json.dumps(analysis_results.get('statistics', {}), indent=2, default=str)}
        """
        return report.strip()
