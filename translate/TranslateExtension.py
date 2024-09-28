from ulauncher.api.client.Extension import Extension
from ulauncher.api.shared.event import (KeywordQueryEvent,PreferencesEvent)

from translate.ExtensionKeywordListener import ExtensionKeywordListener
from translate.PreferencesListener import PreferencesListener


class TranslateExtension(Extension):

    def __init__(self):
        super(TranslateExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, ExtensionKeywordListener())
        self.subscribe(PreferencesEvent, PreferencesListener())