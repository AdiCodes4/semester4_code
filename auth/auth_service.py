from app.models.user import User
from auth.auth import token_auth

def authenticate_user(email: str, password: str, token_duration=600):
    """Verifies user credentials and returns token data, or None if invalid."""
    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return None

    token = user.generate_auth_token(token_duration)

    return {
        'token': token,
        'duration': token_duration,
        'user_id': user.id
    }