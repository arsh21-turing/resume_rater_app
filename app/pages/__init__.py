# Pages package initialization
from app.pages.home import display_home
from app.pages.about import display_about
from app.pages.results import display_results

__all__ = [
    'display_home',
    'display_about',
    'display_results'
]