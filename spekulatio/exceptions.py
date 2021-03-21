class SpekulatioError(Exception):
    pass


class SpekulatioReadError(SpekulatioError):
    pass


class SpekulatioWriteError(SpekulatioError):
    pass


class SpekulatioFrontmatterError(SpekulatioError):
    pass


class SpekulatioValueError(SpekulatioReadError):
    pass
