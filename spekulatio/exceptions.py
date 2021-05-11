class SpekulatioError(Exception):
    pass

class SpekulatioInternalError(SpekulatioError):
    """The system found itself in an unexpected state."""
    pass


class SpekulatioReadError(SpekulatioError):
    """Error raised during the creation of the site in memory."""
    pass


class SpekulatioBuildError(SpekulatioError):
    """Error raised during the creation of the site in disk."""
    pass


class SpekulatioFrontmatterError(SpekulatioError):
    """Error raised while parsing a node's frontmatter."""
    pass


class SpekulatioValueError(SpekulatioReadError):
    """Error raised while parsing a node's values."""
    pass

