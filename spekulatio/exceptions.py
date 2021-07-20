class SpekulatioError(Exception):
    """Base exception for all Spekulatio errors."""

    pass


class SpekulatioInternalError(SpekulatioError):
    """The system found itself in an unexpected state."""

    pass


class SpekulatioConfigError(SpekulatioError):
    """The user has provided an invalid piece of configuration."""

    pass


class SpekulatioReadError(SpekulatioError):
    """Error raised during the creation of the site in memory."""

    pass


class SpekulatioFrontmatterError(SpekulatioReadError):
    """Error raised while parsing a node's frontmatter."""

    pass


class SpekulatioValueError(SpekulatioReadError):
    """Error raised while parsing a node's values."""

    pass


class SpekulatioWriteError(SpekulatioError):
    """Error raised during the creation of the site in disk."""

    pass


class SpekulatioSkipExtraction(Exception):
    """Don't process values for this node (eg. static files)"""

    pass
