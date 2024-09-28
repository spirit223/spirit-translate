from ulauncher.api.client.Extension import Extension
from ulauncher.api.shared.event import (KeywordQueryEvent, PreferencesEvent, PreferencesUpdateEvent)

from translate.ExtensionKeywordListener import ExtensionKeywordListener
from translate.PreferencesInfo import PreferencesListener, PreferencesUpdateListener


class TranslateExtension(Extension):

    def __init__(self):
        super(TranslateExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, ExtensionKeywordListener())
        self.subscribe(PreferencesEvent, PreferencesListener())
        self.subscribe(PreferencesUpdateEvent, PreferencesUpdateListener())