from werkzeug.security import generate_password_hash, check_password_hash

from music.adapters.repository import AbstractRepository
from music.domainmodel.user import User

class NameNotUniqueException(Exception):
    pass

class UnknownUserException(Exception):
    pass

class AuthenticationException(Exception):
    pass

def add_user(user_name: str, password: str, repo: AbstractRepository):
    # Check that the given username is available.
    user = repo.get_user(user_name)
    if user is not None:
        # A user with the given username already exists, therefore it's not available.
        raise NameNotUniqueException
    
    password_hash = generate_password_hash(password)
    user_new_id = int(repo.get_id())

    # Create user and add to the repository.
    user = User(user_new_id, user_name, password_hash)
    repo.add_user(user)

def get_user(user_name: str, repo: AbstractRepository):
    user = repo.get_user(user_name)
    if user is None:
        # No user with the given username, so raise an exception.
        raise UnknownUserException

    return user_to_dict(user)

def authenticate_user(user_name: str, password: str, repo: AbstractRepository):
    authenticated = False 

    user = repo.get_user(user_name)
    if user is not None:
        authenticated = check_password_hash(user.password, password)
    if not authenticated:
        raise AuthenticationException


def user_to_dict(user: User):
    user_dict = {
        'user_name': user.user_name,
        'password': user.password,
    }

    return user_dict

