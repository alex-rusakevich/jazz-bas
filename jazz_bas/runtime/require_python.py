import sys

from jazz_bas import MIN_PYTHON_VERSION
from jazz_bas.exceptions import UnsupportedPythonVersionError


def require_python(python_version=MIN_PYTHON_VERSION):
    if sys.version_info < python_version:
        raise UnsupportedPythonVersionError(
            "Python {}.{} or higher is required. Your current version is {}".format(
                python_version[0], python_version[1], sys.version
            )
        )
