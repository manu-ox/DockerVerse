from pyrogram.types import CallbackQuery, InlineKeyboardMarkup
from datetime import datetime, timedelta

from dockerVerse.utils import format_time, bold_text
from dockerVerse import DvClient
from dockerVerse.handlers import Buttons



DEFAULT_LOGS_TIME = 15  # Minutes
DEFAULT_LOGS_LINE = 50

LOGS_TIME_UPDATE_UNIT = 15  # Minutes
LOGS_LINE_UPDATE_UNIT = 25


@Buttons.time_logs.set_handler
async def container_time_logs_button_handler(client: DvClient, query: CallbackQuery):
    container_id = Buttons.time_logs.get_container_id(query.data)
    minutes = Buttons.time_logs.get_number(query.data)

    if minutes <= 0:
        # Happens only if messed 
        return await query.answer("Invalid time")
    
    container_log = client.docker.get_logs_by_time(container_id, minutes)

    if not container_log.logs:
        return await query.answer(
            f"No Logs in last {minutes} minutes", show_alert=True
        )
    
    curr_time = datetime.now()
    from_time = curr_time - timedelta(minutes=minutes)

    caption = f"{format_time(from_time)} ->\n{format_time(curr_time)}"
    
    with container_log:
        await client.bot.send_document(
            query.from_user.id,
            container_log.filename,
            caption=bold_text(caption)
        )
    
    await client.bot.acknowledge_query(query)


@Buttons.line_logs.set_handler
async def container_line_logs_button_handler(client: DvClient, query: CallbackQuery):
    container_id = Buttons.line_logs.get_container_id(query.data)
    lines = Buttons.line_logs.get_number(query.data)

    if lines <= 0:
        # Happens only if code messed 
        return await query.answer("Invalid number of lines")
    
    container_log = client.docker.get_logs_by_line(container_id, lines)

    if not container_log.logs:
        return await query.answer(f"Nothing in logs yet", show_alert=True)
    
    caption = f"Last {lines} lines of logs"
    
    with container_log:
        await client.bot.send_document(
            query.from_user.id,
            container_log.filename,
            caption=bold_text(caption)
        )
    
    await client.bot.acknowledge_query(query)



@Buttons.update_logs_time.set_handler
async def logs_time_update_handler(client: DvClient, query: CallbackQuery):
    time = Buttons.update_logs_time.get_number(query.data)
    container_id = Buttons.update_logs_time.get_container_id(query.data)

    if time <= 0:
        return await client.bot.acknowledge_query(query)
    
    logs_button = Buttons.time_logs.button(
        f"Last {time} minutes logs",
        container_id=container_id, number=time
    )

    def control_button(time: int, x: int, *, inc=False):
        return Buttons.update_logs_time.button(
            f"{'+' if inc else '-'}{LOGS_TIME_UPDATE_UNIT * x} minutes",
            container_id=container_id,
            number=time,
        )
    
    inc_1x_button = control_button(time + LOGS_TIME_UPDATE_UNIT, 1, inc=True)
    dec_1x_button = control_button(time - LOGS_TIME_UPDATE_UNIT, 1)
    inc_2x_button = control_button(time + (2 * LOGS_TIME_UPDATE_UNIT), 2, inc=True)
    dec_2x_button = control_button(time - (2 * LOGS_TIME_UPDATE_UNIT), 2)
    inc_4x_button = control_button(time + (4 * LOGS_TIME_UPDATE_UNIT), 4, inc=True)
    dec_4x_button = control_button(time - (4 * LOGS_TIME_UPDATE_UNIT), 4)

    back_button = Buttons.container_logs_option.button(
        "\u2039\u2039 Go back",
        container_id=container_id
    )

    buttons = [
        [logs_button],
        [dec_1x_button, inc_1x_button],
        [dec_2x_button, inc_2x_button],
        [dec_4x_button, inc_4x_button],
        [back_button]
    ]

    await query.edit_message_reply_markup(InlineKeyboardMarkup(buttons))
    await client.bot.acknowledge_query(query)


@Buttons.update_logs_line.set_handler
async def logs_line_update_handler(client: DvClient, query: CallbackQuery):
    number = Buttons.update_logs_line.get_number(query.data)
    container_id = Buttons.update_logs_line.get_container_id(query.data)

    if number <= 0:
        return await client.bot.acknowledge_query(query)
    
    logs_button = Buttons.line_logs.button(
        f"Last {number} lines of logs",
        container_id=container_id, number=number
    )

    def control_button(number: int, x: int, *, inc=False):
        return Buttons.update_logs_line.button(
            f"{'+' if inc else '-'}{LOGS_LINE_UPDATE_UNIT * x} lines",
            number=number,
            container_id=container_id
        )
    
    inc_1x_button = control_button(number + LOGS_LINE_UPDATE_UNIT, 1, inc=True)
    dec_1x_button = control_button(number - LOGS_LINE_UPDATE_UNIT, 1)
    inc_2x_button = control_button(number + (2 * LOGS_LINE_UPDATE_UNIT), 2, inc=True)
    dec_2x_button = control_button(number - (2 * LOGS_LINE_UPDATE_UNIT), 2)
    inc_4x_button = control_button(number + (4 * LOGS_LINE_UPDATE_UNIT), 4, inc=True)
    dec_4x_button = control_button(number - (4 * LOGS_LINE_UPDATE_UNIT), 4)

    back_button = Buttons.container_logs_option.button(
        "\u2039\u2039 Go back",
        container_id=container_id
    )

    buttons = [
        [logs_button],
        [dec_1x_button, inc_1x_button],
        [dec_2x_button, inc_2x_button],
        [dec_4x_button, inc_4x_button],
        [back_button]
    ]

    await query.edit_message_reply_markup(InlineKeyboardMarkup(buttons))
    await client.bot.acknowledge_query(query)


@Buttons.container_logs_option.set_handler
async def logs_option_button_handler(client: DvClient, query: CallbackQuery):
    container_id = Buttons.container_logs_option.get_container_id(query.data)

    time_logs_button = Buttons.update_logs_time.button(
        "Logs By Time", number=DEFAULT_LOGS_TIME, container_id=container_id
    )
    
    line_logs_button = Buttons.update_logs_line.button(
        "Logs By Lines", number=DEFAULT_LOGS_LINE, container_id=container_id
    )

    back_button = Buttons.container_compact_view.button(
        "\u2039\u2039 Go back", container_id=container_id
    )

    buttons = [
        [time_logs_button],
        [line_logs_button],
        [back_button]
    ]

    await query.edit_message_reply_markup(InlineKeyboardMarkup(buttons))

