from ulauncher.api.client.Extension import Extension
from ulauncher.api.shared.event import KeywordQueryEvent

from translate.ExtensionKeywordListener import ExtensionKeywordListener


class TranslateExtension(Extension):

    def __init__(self):
        super(TranslateExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, ExtensionKeywordListener())