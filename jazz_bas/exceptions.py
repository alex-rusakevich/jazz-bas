class JassBassError(Exception):
    pass


class CliError(JassBassError):
    pass


class NotATokenError(JassBassError):
    pass


class UnexpectedTokenError(JassBassError):
    pass


class UnsupportedPythonVersionError(JassBassError):
    pass
