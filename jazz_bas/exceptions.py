class JassBassError(Exception):
    pass


class CliError(JassBassError):
    pass


class JassBassSyntaxError(JassBassError):
    pass


class UnmetDependencyError(JassBassError):
    pass
