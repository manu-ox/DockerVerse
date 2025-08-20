from pyrogram.types import Message, CallbackQuery
from pyrogram import errors as bot_errors
from docker import errors as docker_errors
from functools import wraps
from typing import Callable
import traceback
from requests.exceptions import ConnectionError

from dockerVerse import errors as dv_errors
from dockerVerse import DvClient
from dockerVerse.logger import dv_log




async def respond(request: Message | CallbackQuery, response: str):
    # Request is either CallbackQuery or NewMessage.Event
    if isinstance(request, CallbackQuery):
        return await request.answer(response, show_alert=True)
    
    return await request.reply(response)


def bot_handler(func: Callable[[DvClient, Message | CallbackQuery], None]):
    """
    Error handling decorator for request handlers
    """

    @wraps(func)
    async def wrapper(client: DvClient, request: Message | CallbackQuery):
        try:
            await func(client, request)
        except docker_errors.APIError as e:
            dv_log.error(traceback.format_exc(), exc_info=True)
            await respond(request, f"#ERROR: Docker Api failed")
        except docker_errors.NotFound:
            await respond(request, "#ERROR: Container not found!")
        except dv_errors.ContainerProtectedError:
            await respond(request, "#ERROR: Container Protected!")
        except dv_errors.ContainerAccessProhibitedError:
            await respond(request, "#ERROR: Continer cannot be accesed!")
        except ConnectionError:
            await respond(request, "#ERROR: Docker Daemon disconnected!")
        except (bot_errors.PeerIdInvalid, bot_errors.UserIsBlocked):
            # Ignoring blocked users
            pass
        except (bot_errors.QueryIdInvalid, bot_errors.MessageNotModified):
            # Ignorable
            pass
        except Exception as e:
            dv_log.error(traceback.format_exc(), exc_info=True)
            await respond(request, f"#ERROR: {e.__class__.__name__}")
    
    return wrapper

