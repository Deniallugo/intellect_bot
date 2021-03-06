import io
import mimetypes
import magic

from abc import ABCMeta, abstractmethod
from telebot import TeleBot

from .messages import prepare_message, Message
from .markup import prepare_markup


class NotAllowedTypeError(Exception):
    pass


class InvalidTypeError(Exception):
    pass


class ResponseBase(metaclass=ABCMeta):
    def __init__(self, delay=0.0, **options):
        self.delay = delay
        self.options = options

    @abstractmethod
    def send_to(self, bot, chat_id):
        pass


class MarkupResponseBase(ResponseBase, metaclass=ABCMeta):
    def __init__(self, markup=None, **options):
        super().__init__(**options)
        self.markup = markup or prepare_markup(None)


class FileResponseBase(MarkupResponseBase, metaclass=ABCMeta):
    allowed_types = None
    _magic = magic.Magic(mime=True)

    class RemoteFile:

        def __init__(self, token):
            self.token = token

        def __enter__(self):
            return self.token

        def __exit__(self, *args):
            pass

    def __init__(self, data, caption=None, filename=None, **options):
        assert isinstance(data, (str, bytes, io.BufferedIOBase, io.RawIOBase))
        super().__init__(**options)

        if isinstance(data, (io.BufferedIOBase, io.RawIOBase)):
            filename = filename or getattr(data, 'name')
            data = data.read()

        if not isinstance(data, str) and filename is None:
            file_type = self._magic.from_buffer(data[:256])

            if self.allowed_types and file_type not in self.allowed_types:
                raise NotAllowedTypeError(
                    'Source type "%s" is not supported '
                    'by this type of response' % file_type)

            ext = mimetypes.guess_extension(file_type)
            if ext is None:
                raise InvalidTypeError('Can\'t determine type of source')

            filename = 'public%s' % ext

        self.data = data
        self.caption = caption
        self.filename = filename

    def request_data(self):
        if isinstance(self.data, str):
            return self.RemoteFile(self.data)

        blob = io.BytesIO(self.data)
        blob.name = self.filename
        return blob


class TextResponse(MarkupResponseBase):
    def __init__(self, message, **options):
        assert isinstance(message, (Message, str))
        super().__init__(**options)
        if isinstance(message, str):
            message = Message(message)
        self.message = message

    def send_to(self, bot, chat_id):
        assert isinstance(bot, TeleBot)
        return bot.send_message(
            chat_id,
            self.message.text,
            parse_mode=self.message.parse_mode,
            reply_markup=self.markup,
            **self.options
        )


class LocationResponse(MarkupResponseBase):
    def __init__(self, longtitude, latitude, **options):
        assert isinstance(longtitude, float)
        assert isinstance(latitude, float)
        super().__init__(**options)
        self.longtitude = longtitude
        self.latitude = latitude

    def send_to(self, bot, chat_id):
        assert isinstance(bot, TeleBot)
        return bot.send_location(
            chat_id,
            longitude=self.longtitude,
            latitude=self.latitude,
            reply_markup=self.markup,
            **self.options)


class PhotoResponse(FileResponseBase):
    allowed_types = {'image/jpeg', 'image/png', 'image/gif',
                     'image/tiff', 'image/tiff-fx'}

    def send_to(self, bot, chat_id):
        assert isinstance(bot, TeleBot)
        with self.request_data() as data:
            return bot.send_photo(
                chat_id,
                data,
                caption=self.caption,
                reply_markup=self.markup,
                **self.options
            )


class AudioResponse(FileResponseBase):
    allowed_types = {'audio/mpeg', 'audio/MPA', 'audio/mpa-robust'}

    def send_to(self, bot, chat_id):
        assert isinstance(bot, TeleBot)
        with self.request_data() as data:
            return bot.send_audio(
                chat_id,
                data,
                caption=self.caption,
                reply_markup=self.markup,
                **self.options
            )


class VideoResponse(FileResponseBase):
    allowed_types = {'video/mp4'}

    def send_to(self, bot, chat_id):
        assert isinstance(bot, TeleBot)
        with self.request_data() as data:
            return bot.send_video(
                chat_id,
                data,
                caption=self.caption,
                reply_markup=self.markup,
                **self.options
            )


class DocumentResponse(FileResponseBase):
    def send_to(self, bot, chat_id):
        assert isinstance(bot, TeleBot)
        with self.request_data() as data:
            return bot.send_document(
                chat_id,
                data,
                caption=self.caption,
                reply_markup=self.markup,
                **self.options
            )


class TextUpdate(TextResponse):
    def __init__(self, message, message_id, **options):
        assert message_id is not None
        super().__init__(message, **options)
        self.message_id = message_id

    def send_to(self, bot, chat_id):
        assert isinstance(bot, TeleBot)
        return bot.edit_message_text(
            self.message.text,
            chat_id,
            self.message_id,
            parse_mode=self.message.parse_mode,
            reply_markup=self.markup,
            **self.options
        )


class MarkupUpdate(MarkupResponseBase):
    def __init__(self, message_id, **options):
        assert message_id is not None
        super().__init__(**options)
        self.message_id = message_id

    def send_to(self, bot, chat_id):
        assert isinstance(bot, TeleBot)
        return bot.edit_message_reply_markup(
            chat_id,
            self.message_id,
            reply_markup=self.markup,
            **self.options
        )


class ChatAction(ResponseBase):
    def __init__(self, action):
        """
        :param action:  One of the strings: 'typing', 'upload_photo',
        'record_video', 'upload_video', 'record_audio', 'upload_audio',
        'upload_document', 'find_location'.
        """
        super().__init__()
        self.action = action

    def send_to(self, bot, chat_id):
        assert isinstance(bot, TeleBot)
        return bot.send_chat_action(chat_id, self.action)


def prepare_response(response):
    if isinstance(response, ResponseBase):
        return response

    if isinstance(response, str):
        return TextResponse(
            message=prepare_message(response),
            markup=prepare_markup(None)
        )

    if isinstance(response, tuple):
        res_len = len(response)
        assert res_len > 0

        props = dict(message=prepare_message(response[0]))
        if res_len > 1 and isinstance(response[1], (list, tuple)):
            props['markup'] = prepare_markup(response[1])

        return TextResponse(**props)


class VenueResponse(LocationResponse):
    def __init__(self, title, address, **options):
        super().__init__(**options)
        self.title = title
        self.address = address

    def send_to(self, bot, chat_id):
        assert isinstance(bot, TeleBot)
        return bot.send_venue(
            chat_id,
            longitude=self.longtitude,
            latitude=self.latitude,
            address=self.address,
            title=self.title,
            reply_markup=self.markup,
            **self.options)
