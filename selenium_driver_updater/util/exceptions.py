class Error(Exception):
    """Base class for exceptions in this module."""

class StatusCodeNotEqualException(Error):
    """Raises if status_code of url is not equal to 200"""
    pass

class DriverVersionInvalidException(Error):
    """Raises if current driver version is not equal to its latest version"""
    pass

class GithubApiLimitException(Error):
    """Raises if access to github api is restricted"""
    pass

class UnknownArchiveFormatException(Error):
    """Raises if unknown archive format was specified/downloaded"""
    pass
