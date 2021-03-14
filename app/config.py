from os import environ


HOST = environ.get("HOST", "0.0.0.0")
PORT = environ.get("PORT", 8000)


TITLE_N_FIRST_CHARS = environ.get("TITLE_N_FIRST_CHARS", default=10)
if not isinstance(TITLE_N_FIRST_CHARS, int) or TITLE_N_FIRST_CHARS < 1:
    raise ValueError("`TITLE_N_FIRST_CHARS` may be only integer larger than 0.")
