from typing import Dict, Optional 
from langchain_core.tools import tool

#Mock in-memory "database" of packages
MOCK_PACKAGES: Dict[str, str] = {
    "1z3456": "Package 123456 is in transit and will arrive tomorrow.",
    "6z4321": "Package 654321 has been delivered.",
    "1R1111": "Package 111111 is delayed due to weather conditions.",
}

@tool
def track_package_lookup(tracking_number: str) -> str:
    """Mock tracking API lookup.
    This is a LangChain tool that the tracking agent can call."""

    status: Optional[str] = MOCK_PACKAGES.get(tracking_number.upper())
    if status:
        return f"Tracking ID {tracking_number} : {status}"
    return f"Tracking ID {tracking_number} : no information found. Please check the number and try again."
