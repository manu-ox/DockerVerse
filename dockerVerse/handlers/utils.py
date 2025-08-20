from .types import Buttons, Commands
from .types.base import ButtonHandler, CommandHandler



def get_enabled_commands() -> list[CommandHandler]:
    for command in Commands.ENABLED_COMMANDS:

        try:
            getattr(command, 'raw_handler')
        except AttributeError:
            raise KeyError(f"Handler function not set for {command.__class__.__name__}")
        
    return Commands.ENABLED_COMMANDS


def get_enabled_buttons() -> list[ButtonHandler]:
    for button in Buttons.ENABLED_BUTTONS:

        try:
            getattr(button, 'raw_handler')
        except AttributeError:
            raise KeyError(f"Handler function not set for {button.__class__.__name__}")
        
    return Buttons.ENABLED_BUTTONS


