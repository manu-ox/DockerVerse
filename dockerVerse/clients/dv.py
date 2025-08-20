from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from pyrogram import idle

from .bot import DvBotClient
from .docker import DvDockerClient
from .types import DvEvent, DockerEventType, DvEventStatus, DvContainer
from dockerVerse.logger import event_log, dv_log
from dockerVerse.utils import bold_text


class DvClient:
    bot: DvBotClient
    docker: DvDockerClient

    def __init__(self):
        self.bot = DvBotClient()
        self.docker = DvDockerClient()

    def start(self):
        self.add_event_handlers()
        self.bot.start()

        dv_log.info("DockerVerse Is Running")
        
        idle()

        self.cleanup()
    
    def cleanup(self):
        self.docker.stop_event_observer()
    
    def add_event_handlers(self):

        from dockerVerse.handlers import command_handler, query_handler

        async def c_handler(_, update):
            await command_handler(self, update)
            
        async def q_handler(_, update):
            await query_handler(self, update)

        self.bot.add_handler(MessageHandler(c_handler))
        self.bot.add_handler(CallbackQueryHandler(q_handler))


        self.docker.start_event_observer(self.docker_event_handler)

    async def docker_event_handler(self, event: DvEvent):
        # Ignoring other events
        if event.type != DockerEventType.CONTAINER: return

        if event.status == DvEventStatus.STARTED:
            updated_status = 'STARTED'
        elif event.status == DvEventStatus.STOPPED:
            updated_status = 'STOPPED'
        elif event.status == DvEventStatus.DESTROYED:
            updated_status = 'DESTROYED'
        else:
            # Not handling restart as restart is 'stop and start'
            return
        
        await self.bot.broadcast(bold_text(f"`{event.container_name}` {updated_status}"))
        event_log.info(f"{updated_status} CONTAINER {event.container_id} {event.container_name}")
    
    def log_user_action(self, container: DvContainer, user_id: int, method: str):
        event_log.info(
            f"USER:{user_id} ACTION:{method} CONTAINER: `{container.id}` `{container.name}`"
        )


