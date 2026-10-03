class SessionManager:

    def create_session(self, user):
        return {
            "user_id": user.user_id,
            "active": True
        }