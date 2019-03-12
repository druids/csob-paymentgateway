from datetime import datetime
from typing import Optional


def get_dttm(date_time: Optional[datetime] = None) -> str:
    """
    Get DTTM from datetime or actual time.

    Args:
        date_time: The input datetime or None for use now()

    Returns:
        dttm - str
    """
    return (date_time or datetime.now()).strftime('%Y%m%d%H%M%S')
