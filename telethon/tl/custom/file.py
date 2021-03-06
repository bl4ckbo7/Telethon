import mimetypes

from ... import utils
from ...tl import types


class File:
    """
    Convenience class over media like photos or documents, which
    supports accessing the attributes in a more convenient way.

    If any of the attributes are not present in the current media,
    the properties will be ``None``.

    The original media is available through the ``media`` attribute.
    """
    def __init__(self, media):
        self.media = media

    @property
    def id(self):
        """
        The bot-API style ``file_id`` representing this file.
        """
        return utils.pack_bot_file_id(self.media)

    @property
    def name(self):
        """
        The file name of this document.
        """
        return self._from_attr(types.DocumentAttributeFilename, 'file_name')

    @property
    def ext(self):
        """
        The extension from the mime type of this file.
        """
        return mimetypes.guess_extension(self.mime_type)

    @property
    def mime_type(self):
        """
        The mime-type of this file.
        """
        if isinstance(self.media, types.Photo):
            return 'image/jpeg'
        elif isinstance(self.media, types.Document):
            return self.media.mime_type

    @property
    def width(self):
        """
        The width in pixels of this media if it's a photo or a video.
        """
        return self._from_attr((
            types.DocumentAttributeImageSize, types.DocumentAttributeVideo), 'w')

    @property
    def height(self):
        """
        The height in pixels of this media if it's a photo or a video.
        """
        return self._from_attr((
           types.DocumentAttributeImageSize, types.DocumentAttributeVideo), 'h')

    @property
    def duration(self):
        """
        The duration in seconds of the audio or video.
        """
        return self._from_attr((
            types.DocumentAttributeAudio, types.DocumentAttributeVideo), 'duration')

    @property
    def title(self):
        """
        The title of the song.
        """
        return self._from_attr(types.DocumentAttributeAudio, 'title')

    @property
    def performer(self):
        """
        The performer of the song.
        """
        return self._from_attr(types.DocumentAttributeAudio, 'performer')

    @property
    def emoji(self):
        """
        A string with all emoji that represent the current sticker.
        """
        return self._from_attr(types.DocumentAttributeSticker, 'alt')

    @property
    def sticker_set(self):
        """
        The :tl:`InputStickerSet` to which the sticker file belongs.
        """
        return self._from_attr(types.DocumentAttributeSticker, 'stickerset')

    @property
    def size(self):
        """
        The size in bytes of this file.
        """
        if isinstance(self.media, types.Photo):
            return self._size_for(self.media.sizes[-1])
        elif isinstance(self.media, types.Document):
            return self.media.size

    @staticmethod
    def _size_for(kind):
        if isinstance(kind, types.PhotoSize):
            return kind.size
        elif isinstance(kind, types.PhotoStrippedSize):
            return utils._stripped_real_length(kind.bytes)
        elif isinstance(kind, types.PhotoCachedSize):
            return len(kind.bytes)
        # elif isinstance(kind, types.PhotoSizeEmpty):
        return 0

    def _from_attr(self, cls, field):
        if isinstance(self.media, types.Document):
            for attr in self.media.attributes:
                if isinstance(attr, cls):
                    return getattr(attr, field, None)
