from app.scripts.validate_library import validate_library


def run_startup_checks() -> None:
    """
    Hard fail if library is invalid.
    This runs once at application boot.
    """
    ok, errors = validate_library(return_errors=True)

    if not ok:
        formatted = "\n".join(f" - {e}" for e in errors)
        raise RuntimeError(
            "❌ Library validation failed at startup:\n" + formatted
        )
