from typing import Any, Mapping

from jazz_bas.compile import jazz_compile


def jazz_execute(
    jazz_code: str,
    script_globals: dict[str, Any] | None = None,
    script_locals: Mapping[str, object] | None = None,
):
    return exec(jazz_compile(jazz_code), script_globals, script_locals)
