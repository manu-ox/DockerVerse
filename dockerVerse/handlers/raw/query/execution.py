from pyrogram.types import Message, CallbackQuery
from datetime import datetime
from threading import Thread
import asyncio
import re

from dockerVerse import DvClient
from dockerVerse.config import is_protected_container
from dockerVerse.handlers import Buttons
from dockerVerse.clients.types import DvContainer
from dockerVerse.utils import bold_text, error_handler
from dockerVerse.handlers.types.methods import ContainerMethod
from dockerVerse.logger import event_log


class Click:
    TIME_INTERVAL: int = 10  # seconds
    _last_click_id: str = None
    _last_click_time: datetime = None
    _click_count: int = 0

    @classmethod
    def count(cls, id: str):
        if cls._last_click_time:
            time_taken = (datetime.now() - cls._last_click_time).seconds
            if time_taken < cls.TIME_INTERVAL and cls._last_click_id == id:
                cls._click_count += 1
                return cls._click_count
        
        cls._last_click_id = id
        cls._last_click_time = datetime.now()
        cls._click_count = 1
        return 1


async def control_execution(client: DvClient, query: CallbackQuery, container: DvContainer, method: str):
    if is_protected_container(container.id):
        return await query.answer(f"Container {container.name} is Protected")
    
    if Click.count(query.data) < 2:
        return await query.answer("Click again to Confirm", show_alert=True)
    
    process_message = await client.bot.send_message(
        chat_id=query.from_user.id,
        text=(
            f"Performing {bold_text(method)} on `{container.name}` ...\n"
        )
    )

    if method == ContainerMethod.start:
        fn = client.docker.start_container
    elif method == ContainerMethod.stop:
        fn = client.docker.stop_container
    elif method == ContainerMethod.restart:
        fn = client.docker.restart_container
    else:
        raise ValueError("Invalid Container Method")
    
    @error_handler
    async def remaining_process():
        start_time = datetime.now()
        fn(container.id)

        await client.log_user_action(
            container, query.from_user.id, method
        )

        time_taken = datetime.now() - start_time
        await process_message.edit_text((
            f"`{container.name}` Completed {bold_text(method)} in {time_taken.seconds}s\n"
        ))

        # Refreshing info with view method by patching
        query.data = re.sub(
            f"{ContainerMethod.start}|{ContainerMethod.stop}|{ContainerMethod.restart}",
            ContainerMethod.view,
            query.data
        )

        await Buttons.container_compact_view.raw_handler(client, query)

    # Doing remaining tasks in another thread to prevent blocking
    Thread(target=lambda: asyncio.run(remaining_process())).start()
    await query.answer(f"Performing {method}", show_alert=True)

    

@Buttons.container_start.set_handler
async def container_start_button_handler(client: DvClient, query: CallbackQuery):
    container_id = Buttons.container_start.get_container_id(query.data)
    container = client.docker.get_container(container_id)

    if container.is_running:
        return await query.answer("Container is already running!", show_alert=True)
    
    await control_execution(client, query, container, ContainerMethod.start)
    
    
@Buttons.container_stop.set_handler
async def container_stop_button_handler(client: DvClient, query: CallbackQuery):
    container_id = Buttons.container_stop.get_container_id(query.data)
    container = client.docker.get_container(container_id)

    if not container.is_running:
        return await query.answer("Container is not running!", show_alert=True)
    
    await control_execution(client, query, container, ContainerMethod.stop)


@Buttons.container_restart.set_handler
async def container_restart_button_handler(client: DvClient, query: CallbackQuery):
    container_id = Buttons.container_restart.get_container_id(query.data)
    container = client.docker.get_container(container_id)

    if not container.is_running:
        return await query.answer("Container is not running!", show_alert=True)
    
    await control_execution(client, query, container, ContainerMethod.restart)
    
