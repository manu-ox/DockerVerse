from pyrogram.types import CallbackQuery, InlineKeyboardMarkup
from enum import Enum, auto

from dockerVerse.utils import bold_text
from dockerVerse.handlers import Buttons
from dockerVerse import DvClient



class ViewOptions(Enum):
    compact = auto()
    detailed = auto()


@Buttons.container_compact_view.set_handler
async def compact_view_button_handler(client: DvClient, query: CallbackQuery):
    await view_handler(client, query, ViewOptions.compact)


@Buttons.container_detailed_view.set_handler
async def detailed_view_button_handler(client: DvClient, query: CallbackQuery):
    await view_handler(client, query, ViewOptions.detailed)


async def view_handler(client: DvClient, query: CallbackQuery, option: ViewOptions):
    container_id = Buttons.container_compact_view.get_container_id(query.data)
    container = client.docker.get_container(container_id)

    if container.is_running:
        execution_control_buttons = [
            Buttons.container_stop.button('STOP', container_id=container_id),
            Buttons.container_restart.button('RESTART', container_id=container_id),
        ]
    else:
        execution_control_buttons = [
            Buttons.container_start.button('START', container_id=container_id),
        ]
    
    logs_button = Buttons.container_logs_option.button(
        'LOGS', container_id=container_id
    )

    if option == ViewOptions.compact:
        alternate_text = "DETAILED VIEW"
        alternate_handler = Buttons.container_detailed_view
        refresh_handler = Buttons.container_compact_view
        container_info = container.to_string()
    else:
        alternate_text = "COMPACT VIEW"
        alternate_handler = Buttons.container_compact_view
        refresh_handler = Buttons.container_detailed_view
        container_info = container.to_string(detailed=True)

    refresh_button = refresh_handler.button("REFRESH", container_id=container_id)

    container_list_button = Buttons.container_list.button(
        "\u2039\u2039 Back to Container List"
    )

    alternate_view_button = alternate_handler.button(alternate_text, container_id=container_id)

    buttons = [
        [alternate_view_button],
        execution_control_buttons,
        [logs_button],
        [refresh_button],
        [container_list_button]
    ]

    await client.bot.acknowledge_query(query)

    await query.message.edit(
        text=bold_text(container_info),
        reply_markup=InlineKeyboardMarkup(buttons)
    )


