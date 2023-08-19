class SteamlabsSIOError(Exception):
    """Base StreamlabsSIO error class"""


class SteamlabsSIOConnectionError(SteamlabsSIOError):
    """Exception raised when connection errors occur"""
