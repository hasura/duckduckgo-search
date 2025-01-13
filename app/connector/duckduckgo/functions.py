from hasura_ndc import start
from hasura_ndc.function_connector import FunctionConnector
from pydantic import BaseModel
from hasura_ndc.errors import UnprocessableContent
from typing import List
from duckduckgo_search import DDGS

connector = FunctionConnector()

class Result(BaseModel):
    title: str
    href: str
    body: str

@connector.register_query
def web_search(search_term: str, limit: int = 10, region: str = "us-en") -> List[Result]:
    """
    Perform a web search using DuckDuckGo and return the results.
    Takes in default input arguments for limit and region.
    limit is the number of results to return, default 10.
    region is the region to search in, default "us-en".

    Args:
        search_term (str): The term to search for.

    Returns:
        List[Result]: A list of search result objects.
    """
    try:
        with DDGS() as ddgs:
            results = [
                Result(title=entry['title'], href=entry['href'], body=entry.get('body', ''))
                for entry in ddgs.text(search_term, region=region, safesearch='off', timelimit=None, max_results=limit)
            ]
        return results
    except Exception as e:
        raise UnprocessableContent(detail=f"Error during web search: {str(e)}")

if __name__ == "__main__":
    start(connector)
