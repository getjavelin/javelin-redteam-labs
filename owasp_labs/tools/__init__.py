"""
Tools package for OWASP labs
"""

from .install_libraries import get_install_libraries_tool, install_libraries
from .web_scraper import fetch_website_content, get_web_scraping_tool

__all__ = [
    "fetch_website_content",
    "get_web_scraping_tool",
    "install_libraries",
    "get_install_libraries_tool",
]
