import time
import requests
from typing import List, Dict, Any

S2_SEARCH_URL = "https://api.semanticscholar.org/graph/v1/paper/search"

def retrieve_academic_papers(topic: str, limit: int = 3) -> List[Dict[str, Any]]:
    """
    TEMPORARY: Returns a list of hardcoded dummy papers for guaranteed demo success.
    The topic being researched is included in the abstract to test the summarizer.
    """
    print(f"⚠️ Running in DEMO MODE: Bypassing Semantic Scholar API for stability.")
    
    # Return a list of papers with an abstract that references the topic
    # This allows the summarizer.py (Gemini) to still run and produce a valid review.
    return [
        {
            "title": f"The Role of AI in Addressing: {topic} (Demo Paper 1)",
            "abstract": (
                f"This paper explores the theoretical frameworks and practical applications "
                f"of modern AI systems in solving complex real-world challenges, with a focus "
                f"on the critical research area of {topic}. It discusses ethical concerns "
                f"and future directions for large language models in this domain."
            ),
            "url": "https://www.example.com/demo-paper-1"
        },
        {
            "title": f"A Comprehensive Review of Algorithms for: {topic} (Demo Paper 2)",
            "abstract": (
                f"We provide a comprehensive review of existing machine learning algorithms "
                f"related to {topic}. The analysis confirms that a federated, privacy-preserving "
                f"approach is most effective for decentralized data sets. This work serves as "
                f"a baseline for future research in this field."
            ),
            "url": "https://www.example.com/demo-paper-2"
        },
    ]

    # NOTE: To switch back to the live API, you must replace this file with the original code.