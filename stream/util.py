from contextlib import contextmanager
from stream import Session



@contextmanager
def get_session():
    """
    Creates and disposes of a (scoped) session properly
    in a multithreaded application.
    From http://stackoverflow.com/q/5544774
    """
    session = Session()
    try:
        yield session
    except:
        session.rollback()
    finally:
        session.close()

def join_threads(threads):
    """
    Join threads in interruptable fashion.
    Necessary for ^C'ing out of a program (KeyboardInterrupt)
    when there is a raw_input prompt.
    From http://stackoverflow.com/a/9790882/145400
    """
    for t in threads:
        while t.isAlive():
            t.join(5)