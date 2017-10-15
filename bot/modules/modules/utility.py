from bot.modules.responses import *


class MiddlewareBotProxy:
    def __init__(self, bot, middleware):
        self.bot = bot
        self.middleware = middleware

    def respond(self, user, response):
        return self.bot.respond(
            user,
            self.middleware.apply_response(user, prepare_response(response))
        )


class StopUpdateProcessing(Exception):
    pass


# TODO переписать пытаюсь сделать общую генерацию, которая не везде подходит, или приходится сильно изъёбываться
def generate_message(message, buttons_inline_markup=None,
                     buttons_reply_makrup=None,
                     extra_data=None, message_id=None,
                     *args):  # extra_data и inline_markup пока костыли, лучше не придумал надо думать лучше
    from bot.models import BotMessage, MessageButton, Question

    import json

    if isinstance(message, str):
        template = BotMessage.objects.get(type=message)
    elif isinstance(message, BotMessage) or isinstance(message, Question):
        template = message
    elif isinstance(message, MarkupResponseBase):
        message.markup = default_markup()
        return message
    print(message)
    if buttons_reply_makrup:
        reply_markup = ReplyKeyboardMarkup(resize_keyboard=True)
        for button in buttons_reply_makrup:
            reply_markup.add(KeyboardButton(button))

    elif buttons_inline_markup:
        reply_markup = InlineKeyboardMarkup()
        for button in buttons_inline_markup:
            try:
                url = button['url']
            except:
                url = None
            data = json.dumps(button['data'])

            reply_markup.add(InlineKeyboardButton(text=button['text'],
                                                  callback_data=data,
                                                  url=url
                                                  ))
    elif buttons_inline_markup is None:
        buttons = template.buttons.all()
        print(buttons)
        if buttons:
            if buttons[0].inline:
                reply_markup = InlineKeyboardMarkup()
                for button in buttons:
                    if button.data:
                        data = button.data
                        data['extra'] = extra_data
                    else:
                        data = {
                            'next_state': button.next_state,
                            'extra': extra_data}

                    # button_id = set_button(data)
                    data = json.dumps(data)
                    reply_markup.add(InlineKeyboardButton(text=button.text,
                                                          callback_data=data,
                                                          url=button.url
                                                          ))
            else:
                reply_markup = ReplyKeyboardMarkup(resize_keyboard=True)
                for button in buttons:
                    reply_markup.add(KeyboardButton(text=button.text))
        else:
            reply_markup = default_markup()
    else:
        reply_markup = None

    if template.file:
        if args[0]:
            file = args[0]
        else:
            file = template.file
        try:
            caption = args[1]
        except:
            caption = ""
        try:
            if file.telegram_id:
                file_bytes = file.telegram_id
            else:
                file_bytes = file.file.read()
                file.file.close()
            if template.file.file_type == 'photo':
                if message_id:
                    return MarkupUpdate(markup=reply_markup,
                                        message_id=message_id)
                else:
                    return PhotoResponse(file_bytes, file, markup=reply_markup,
                                         caption=caption,
                                         disable_notification=template.disable_notification)

            else:
                pass
        except Exception as e:
            print(e)
            return TextResponse(template.text, markup=reply_markup,
                                disable_notification=template.disable_notification)

    else:
        try:
            text = template.text.format(*args)
        except:
            text = template.text
        if message_id:
            return TextUpdate(message=text, markup=reply_markup,
                              message_id=message_id)
        else:
            return TextResponse(message=text, markup=reply_markup,
                                disable_notification=template.disable_notification)


def default_markup():
    from bot.models import MessageButton
    reply_markup = ReplyKeyboardMarkup(resize_keyboard=True)

    buttons = MessageButton.objects.filter(
        message__type='default_message')
    for button in buttons:
        reply_markup.add(KeyboardButton(text=button.text))
    return reply_markup
