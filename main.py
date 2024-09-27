# todo receive input, try to analysis language and translate
# using http lib to send request and analysis response(json) and show result

from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction


class TranslateExtension(Extension):

    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        """
        in this case `event` will be an instance of KeywordQueryEvent
        on_event() may return an action (see Actions).
        :param event: KeywordQueryEvent
        :param extension:
        :return: action
        """
        items = []
        for i in range(5):
            data = {'new_name': 'Item %s was clicked' % i}
            items.append(ExtensionResultItem(icon='images/icon.png',
                                             name='Item %s' % i,
                                             description='Item description %s' % i,
                                             on_enter=ExtensionCustomAction(data, keep_app_open=True)))

        return RenderResultListAction(items)

class ItemEnterEventListener(EventListener):

    def on_event(self, event, extension):
        # event is instance of ItemEnterEvent

        data = event.get_data()
        # do additional actions here...

        # you may want to return another list of results
        # should click item with named new_name
        return RenderResultListAction([ExtensionResultItem(icon='images/icon.png',
                                                           name=data['new_name'],
                                                           on_enter=HideWindowAction())])

if __name__ == '__main__':
    TranslateExtension().run()