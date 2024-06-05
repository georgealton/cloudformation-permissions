import nox
from nox.sessions import Session

BASE_PYTHON = "3.12"


@nox.session(tags=["tests"])
def test(session: Session) -> None:
    """Run Tests."""
    session.install(".")
    session.run("pytest", "-v")
