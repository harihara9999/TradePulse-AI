import google.generativeai as genai
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Initialize gemini client
if settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)
else:
    logger.warning("GEMINI_API_KEY is not set. AI analysis will fail if invoked.")

# We will use the gemini-flash-latest model since it's supported by this specific user key
model = genai.GenerativeModel('gemini-flash-latest')

async def generate_analysis_report(sector: str, collected_data: str) -> str:
    """
    Analyzes the collected data using Gemini API and formats it into a Markdown report.
    """
    if not settings.GEMINI_API_KEY:
        raise ValueError("Gemini API key is not configured on the server.")

    prompt = f"""
    You are an expert financial and market analyst. You have been asked to provide a structured Markdown report on current trade opportunities in India for the following sector: "{sector}".
    
    Here is the most recent data and news collected from the web regarding this sector:
    {collected_data}
    
    Based ONLY on the provided data, and your general analytical skills, generate a professional, structured markdown report with the following sections:
    # Market Analysis Report: {sector.capitalize()} Sector (India)
    ## Executive Summary
    ## Current Market Trends
    ## Trade & Investment Opportunities
    ## Risks & Challenges
    ## Conclusion
    
    Make the report professional, well-formatted, and visually easy to read. Do not hallucinate data that contradicts the findings, but synthesize it well.
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        logger.error(f"Error during AI analysis for {sector}: {str(e)}")
        raise Exception(f"Failed to generate AI analysis: {str(e)}")
