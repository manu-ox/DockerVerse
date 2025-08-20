import dotenv
import os
import socket


dotenv.load_dotenv()

DOCKER_SOCKET = 'unix://var/run/docker.sock'


def _get_env(name: str, /, *, required=False) -> str | None:
    value = os.environ.get(name)

    if not value:
        if not required:
            return None
        raise ValueError(f"ENV '{name}' is essential and not found!")
    
    return value


def _convert_to_user_id(user_id: str) -> str:
    try:
        return int(user_id)
    except ValueError:
        # User id should be an integer
        raise ValueError(f"Invalid User ID: {user_id}")


def _convert_to_short_container_id(container_id: str) -> str:
    try:
        return container_id[:12]
    except KeyError:
        # Short container id is of length 12
        raise ValueError(f"Invalid Container ID: {container_id}")



_authorized_user_ids_var = _get_env('AUTHORIZED_USER_IDS', required=True)
_protected_container_ids_var = _get_env('PROTECTED_CONTAINER_IDS')
_allowed_container_ids_var = _get_env('ALLOWED_CONTAINER_IDS')
_container_ids_to_ignore_var = _get_env('CONTAINER_IDS_TO_IGNORE')

# Telegram vars
API_ID = int(_get_env("TELEGRAM_API_ID", required=True))
API_HASH = _get_env("TELEGRAM_API_HASH", required=True)
BOT_TOKEN = _get_env("TELEGRAM_BOT_TOKEN", required=True)


_IS_DOCKER_ENV = bool(_get_env('IS_DOCKER_ENV'))


# Telegram user-id of Authorized users
if isinstance(_authorized_user_ids_var, str):
    _AUTHORIZED_USER_IDS = [
        _convert_to_user_id(uid) 
        for uid in _authorized_user_ids_var.split(',')
    ]
else:
    _AUTHORIZED_USER_IDS = []


# Short ids of Allowed containers
if isinstance(_allowed_container_ids_var, str):
    _ALLOWED_CONTAINER_IDS = [
        _convert_to_short_container_id(cid) 
        for cid in _allowed_container_ids_var.split(',')
    ]
else:
    _ALLOWED_CONTAINER_IDS = []


# Short ids of containers to Ignore
if isinstance(_container_ids_to_ignore_var, str):
    _CONTAINER_IDS_TO_IGNORE = [
        _convert_to_short_container_id(cid) 
        for cid in _container_ids_to_ignore_var.split(',')
    ]
else:
    _CONTAINER_IDS_TO_IGNORE = []


# Short ids of Protected containers
if isinstance(_protected_container_ids_var, str):
    _PROTECTED_CONTAINER_IDS = [
        _convert_to_short_container_id(cid)
        for cid in _protected_container_ids_var.split(',')
    ]
else:
    _PROTECTED_CONTAINER_IDS = []


if _IS_DOCKER_ENV:
    # If dockerVerse itself is in docker, protecting it by default
    # As container hostname equals short container id
    _PROTECTED_CONTAINER_IDS.append(
        socket.gethostname()
    )


def is_protected_container(short_container_id: str) -> bool:
    """
    Check if container is protected
    A protected container is not allowed to start, stop or restart
    """
    return short_container_id in _PROTECTED_CONTAINER_IDS
    

def is_accessible_container(short_container_id: str) -> bool:
    """
    Check if container is allowed to access
    """
    if _ALLOWED_CONTAINER_IDS:
        return short_container_id in _ALLOWED_CONTAINER_IDS
    
    return short_container_id not in _CONTAINER_IDS_TO_IGNORE


def get_authorized_user_ids() -> list[int]:
    """
    Returns a copy of authorized users id list
    """
    return _AUTHORIZED_USER_IDS.copy()


def is_authorized_user(user_id) -> bool:
    """
    Check if a user is authorized or not
    """
    return user_id in _AUTHORIZED_USER_IDS



