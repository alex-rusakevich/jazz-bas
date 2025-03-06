from jazz_bas.compile import jazz_compile


def jazz_execute(jazz_code: str):
    return exec(jazz_compile(jazz_code))
