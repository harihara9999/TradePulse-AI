from duckduckgo_search import DDGS
import logging

logger = logging.getLogger(__name__)

async def collect_market_data(sector: str) -> str:
    """
    Collects recent news and market data for a given sector in India.
    Returns a combined text of the search results.
    """
    logger.info(f"Collecting market data for sector: {sector}")
    query = f"{sector} sector market trade opportunities news India"
    
    try:
        results = []
        with DDGS() as ddgs:
            # fetch up to 10 news/search results
            search_results = ddgs.text(query, max_results=10)
            
            for index, r in enumerate(search_results):
                title = r.get("title", "")
                snippet = r.get("body", "")
                link = r.get("href", "")
                results.append(f"{index + 1}. {title}\nSummary: {snippet}\nSource: {link}\n")
                
        if not results:
            return "No recent market data found for this sector."
            
        combined_text = "\n".join(results)
        return combined_text

    except Exception as e:
        logger.error(f"Error during data collection for {sector}: {str(e)}")
        raise Exception(f"Failed to collect market data: {str(e)}")
