from pyrogram.types import Message, CallbackQuery
from pyrogram.enums import ChatType

from dockerVerse import config, DvClient
from .types import Commands
from .utils import get_enabled_buttons, get_enabled_commands
from .error import bot_handler



ENABLED_COMMANDS = get_enabled_commands()
ENABLED_BUTTONS = get_enabled_buttons()


@bot_handler
async def command_handler(client: DvClient, message: Message):
    if message.chat.type != ChatType.PRIVATE or not message.text:
        # Ignoring commands from non private chats
        return
    
    if not config.is_authorized_user(message.from_user.id):
        return await message.reply("You are not Authorized!")
    

    for command in ENABLED_COMMANDS:
        if command.pattern.match(message.text):
            await command.raw_handler(client, message)
            break
    else:
        await Commands.start.raw_handler(client, message)


@bot_handler
async def query_handler(client: DvClient, query: CallbackQuery):
    if not query.message or query.message.chat.type != ChatType.PRIVATE:
        # Ignoring clicks from non private chats
        return await query.answer()
    
    if not config.is_authorized_user(query.from_user.id):
        return await query.answer("You are not Authorized!", show_alert=True)
    
    
    for button in ENABLED_BUTTONS:
        if button.pattern.match(query.data):
            await button.raw_handler(client, query)
            break
    else:
        await query.answer("Invalid!")
