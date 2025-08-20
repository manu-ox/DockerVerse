from pyrogram import errors as bot_errors
from docker import errors as docker_errors
from functools import wraps
from typing import Callable
import traceback
from requests.exceptions import ConnectionError

from dockerVerse import errors as dv_errors
from dockerVerse.logger import dv_log



def error_handler(func: Callable):
    """Error handling decorator"""

    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            await func(*args, **kwargs)
        except docker_errors.APIError as e:
            traceback_string = traceback.format_exc()
            dv_log.error(f"{e}\n{traceback_string}", exc_info=True)
        except docker_errors.NotFound as e:
            dv_log.warning(str(e))
        except (dv_errors.ContainerProtectedError, dv_errors.ContainerAccessProhibitedError) as e:
            dv_log.warning(str(e))
        except ConnectionError:
            dv_log.error("Docker Daemon disconnected")
        except (bot_errors.PeerIdInvalid, bot_errors.UserIsBlocked):
            pass
        except (bot_errors.QueryIdInvalid, bot_errors.MessageNotModified):
            pass
        except Exception as e:
            dv_log.error(traceback.format_exc(), exc_info=True)
    
    return wrapper

