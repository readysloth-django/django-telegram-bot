from typing import (Union,
                    Optional,
                    Callable,
                    Coroutine)

from telegram import InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import (filters,
                          BaseHandler,
                          MessageHandler,
                          ConversationHandler)


class CBConversationHandler(ConversationHandler):
    def __init__(self,
                 *args,
                 before_update_state_cb: Optional[Callable] = None,
                 after_update_state_cb: Optional[Callable] = None,
                 **kwargs):
        self.__before_update_state_cb = before_update_state_cb
        self.__after_update_state_cb = after_update_state_cb

        super().__init__(*args, **kwargs)

    def _update_state(self, *args, **kwargs):
        if self.__before_update_state_cb:
            self.__before_update_state_cb(self, *args, **kwargs)

        super()._update_state(*args, **kwargs)

        if self.__after_update_state_cb:
            self.__after_update_state_cb(self, *args, **kwargs)


class Interaction:
    def __init__(self,
                 name: str,
                 text: Union[str, Coroutine],
                 handler: BaseHandler,
                 keyboard: Optional[Coroutine] = None,
                 markup: Union[ReplyKeyboardMarkup, InlineKeyboardMarkup] = ReplyKeyboardMarkup,
                 next_interaction: Optional['Interaction'] = None,
                 before_reply_cb: Coroutine = None,
                 after_reply_cb: Coroutine = None):
        self.text = text
        if type(text) == str:
            async def text_wrapper(*args, **kwargs):
                return text
            self.text = text_wrapper

        self.name = name
        self.next_interaction = next_interaction
        self.handler = handler(callback=self)
        self.keyboard = keyboard
        self.before_reply_cb = before_reply_cb
        self.after_reply_cb = after_reply_cb

    async def __call__(self, update, context):
        message_source = update.effective_message
        reply_text = await self.text(update, context)
        if self.before_reply_cb:
            await self.before_reply_cb(update, context)

        if self.keyboard:
            kbd = await self.keyboard(update, context)
            markup = self.markup(kbd)
            await message_source.reply_text(reply_text,
                                            reply_markup=markup,
                                            parse_mode=ParseMode.HTML)
            if self.after_reply_cb:
                await self.after_reply_cb(update, context)
            return f'{self.name}-kbd'

        next_state = ConversationHandler.END
        if self.next_interaction:
            next_state = self.next_interaction.name
        await message_source.reply_text(reply_text, parse_mode=ParseMode.HTML)

        if self.after_reply_cb:
            await self.after_reply_cb(update, context)
        return next_state

    def __str__(self):
        if self.next_interaction:
            return f'{self.name} -> {self.next_interaction.name}'
        return self.name

    def to_dict(self):
        if not self.next_interaction:
            return {self.name: [MessageHandler(filters.TEXT, self)]}
        return {self.name: [MessageHandler(filters.TEXT, self)],
                **self.next_interaction.to_dict()}

    def to_chain(self):
        if not self.next_interaction:
            return str(self)
        return f'{self} -> {self.next_interaction.to_chain()}'
