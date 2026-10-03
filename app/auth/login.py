from app.auth.session import SessionManager


def login(user):
    session_manager = SessionManager()
    return session_manager.create_session(user)