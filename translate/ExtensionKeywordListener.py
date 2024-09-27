from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.DoNothingAction import DoNothingAction


class ExtensionKeywordListener(EventListener):
    def get_action_to_render(self, name, description, on_enter=None):
        item = ExtensionResultItem(name=name,
                                   description=description,
                                   icon='images/icon.png',
                                   on_enter=on_enter or DoNothingAction())

        return RenderResultListAction([item])

    def on_event(self, event, extension):
        query = event.get_argument()
        return self.get_action_to_render(name="translate",
                                         description="Example: yd apple %s " % query or '')
