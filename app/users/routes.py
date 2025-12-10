from app.users import bp
from app.extensions import db
from app.models.user import User, UserIn, UserOut, TokenOut, LoginIn
from auth.auth_service import authenticate_user
from auth.auth import token_auth
from apiflask import abort

@bp.get('/<int:user_id>')
@bp.auth_required(token_auth)
@bp.output(UserOut)
def get_one_user(user_id):
    current_user = token_auth.current_user
    if not current_user:
        abort(401, message="Unauthorized - No user found")

    user = db.get_or_404(User, user_id)
    return user

@bp.get('/')
@bp.auth_required(token_auth) # Protected Route
@bp.output(UserOut(many=True))
def get_all_users():
    current_user = token_auth.current_user
    if not current_user:
        abort(401, message="Unauthorized - No user found")

    all_users = User.query.all()
    return all_users

@bp.post('/')
@bp.input(UserIn, location='json')
@bp.output(UserOut, status_code=201)
def create_user(json_data):
    user = User(**json_data)
    db.session.add(user)
    db.session.commit()
    return user

@bp.patch('/<int:user_id>')
@bp.auth_required(token_auth)
@bp.input(UserIn(partial=True), location='json')
@bp.output(TokenOut, status_code=200)
def update_user(user_id, json_data):
    current_user = token_auth.current_user
    if not current_user:
        abort(401, message="Unauthorized - No user found")

    user = db.get_or_404(User, user_id)

    # User darf nur sich selbst ändern
    if current_user.id != user.id:
        abort(403, message="You can only update your own profile")
    password_changed = False
        
    for attr, value in json_data.items():
        if attr == "password":
            user.password = value
            password_changed = True
        else:
            setattr(user, attr, value)
    
    db.session.commit()

    if password_changed:
        token = user.generate_auth_token(600)
        return {'token': token, 'duration': 600}

    # Standardantwort bei normalen Änderungen
    return {'token': '', 'duration': 0}


@bp.delete('/<int:user_id>')
@bp.auth_required(token_auth) # Protected Route
@bp.output({}, status_code=204)
def delete_user(user_id):
    current_user = token_auth.current_user
    if not current_user:
        abort(401, message="Unauthorized - No user found")

    user = db.get_or_404(User, user_id)
    db.session.delete(user)
    db.session.commit()
    return 'User succesfully deleted'


@bp.post('/login')
@bp.input(LoginIn, location='json')
@bp.output(TokenOut, status_code=200)
def login_user(json_data):
    result = authenticate_user(json_data.get('email'), json_data.get('password'))

    if not result:
        abort(401, message='Invalid email or password')

    return result

