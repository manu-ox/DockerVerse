from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup

from dockerVerse import DvClient
from dockerVerse.handlers import Commands, Buttons
from dockerVerse.handlers.error import respond
from dockerVerse.utils import bold_text, get_status_tag


@Commands.list.set_handler
@Buttons.container_list.set_handler
async def list_handler(client: DvClient, update: Message | CallbackQuery):
    container_list = client.docker.get_all_containers()

    if len(container_list) == 0:
        return await respond(update, "No containers to list")
    
    buttons = []
    button_row = []
    text = bold_text("List of Containers\n")

    for i, c in enumerate(container_list):
        text += f"\n`{i+1:2}`: {get_status_tag(c.is_running)} `{c.name}`"

        button_row.append(
            Buttons.container_compact_view.button(f"{i+1}", container_id=c.id)
        )

        if (i+1) % 3 == 0:
            buttons.append(button_row)
            button_row = list()

    if button_row:
        buttons.append(button_row)
    
    refresh_button = Buttons.container_list.button('REFRESH')
    buttons.append([refresh_button])

    if isinstance(update, CallbackQuery):
        await client.bot.acknowledge_query(update)
        await update.message.edit_text(text, reply_markup=InlineKeyboardMarkup(buttons))
    else:
        await client.bot.send_message(update.from_user.id, text, reply_markup=InlineKeyboardMarkup(buttons))
    
