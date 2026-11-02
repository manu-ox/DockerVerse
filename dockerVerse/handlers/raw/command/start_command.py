from pyrogram.types import InlineKeyboardMarkup, Message

from dockerVerse import DvClient
from dockerVerse.handlers import Buttons, Commands
from dockerVerse.utils import bold_text


@Commands.start.set_handler
async def start_command_handler(client: DvClient, message: Message):
    buttons = [[Buttons.container_list.button('LIST CONTAINERS')]]
    
    await message.reply(
        bold_text("DockerVerse Is Running"),
        reply_markup=InlineKeyboardMarkup(buttons)
    )

    