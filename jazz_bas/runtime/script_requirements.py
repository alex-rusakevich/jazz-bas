import sys

from jazz_bas import MIN_JAZZ_BAS_VERSION, MIN_PYTHON_VERSION, __version__
from jazz_bas.exceptions import UnmetDependencyError


def require_python(python_version=MIN_PYTHON_VERSION):
    if sys.version_info < python_version:
        raise UnmetDependencyError(
            "Python {}.{} or higher is required. Your current version is {}".format(
                python_version[0], python_version[1], sys.version
            )
        )


def require_jazz_bas(jb_version=MIN_JAZZ_BAS_VERSION):
    if tuple(int(i) for i in __version__.split(".")) < jb_version:
        raise UnmetDependencyError(
            "Jazz.bas {}.{} or higher is required. Your current version is {}".format(
                jb_version[0], jb_version[1], sys.version
            )
        )
