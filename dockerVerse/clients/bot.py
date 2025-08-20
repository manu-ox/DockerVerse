import pyrogram
from pyrogram.errors import PeerIdInvalid, UserIsBlocked
from pyrogram.types import CallbackQuery
from pyrogram.enums import ParseMode

from dockerVerse import config



class DvBotClient(pyrogram.Client):
    def __init__(self):
        super().__init__(
            'bot',
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            parse_mode=ParseMode.MARKDOWN
        )

        self._authorized_users = config.get_authorized_user_ids()

    async def broadcast(self, message_text: str):
        for user in self._authorized_users:
            try:
                await self.send_message(user, message_text)
            except (PeerIdInvalid, UserIsBlocked):
                pass
    
    @staticmethod
    async def acknowledge_query(query: CallbackQuery):
        try:
            await query.answer()
        except: pass
