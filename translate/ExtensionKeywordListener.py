import time

from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.DoNothingAction import DoNothingAction
from translate.LanguageDiscriminator import ParseQueryError, LanguageDiscriminator
from translate.PreferencesInfo import PreferencesInfo
from translate.RequestBuilder import RequestBuilder
import json
import traceback


class ExtensionKeywordListener(EventListener):
    def __init__(self):
        self.countdown_time = PreferencesInfo.delay
        self.is_running = False

    def get_action_to_render(self, name, description, on_enter=None):
        """
        generate result item
        :param name: title
        :param description: second title
        :param on_enter: what to do
        :return: RenderResultListAction
        """
        item = ExtensionResultItem(name=name,
                                   description=description,
                                   icon='images/icon.png',
                                   on_enter=on_enter or DoNothingAction())

        return RenderResultListAction([item])

    def on_event(self, event, extension):
        self.is_running = True
        time.sleep(self.countdown_time)
        text = event.get_argument()
        if text is None:
            return self.get_action_to_render(name="translate",
                                             description="Example: yd apple")
        else:
            try:
                text = text.encode('utf-8').decode('utf-8')
                res = RequestBuilder.build(text)
                # res.data.translation is str array contain translate result
                translation_arr = json.loads(res.data)
                items = []
                if 'translation' not in translation_arr:
                    raise TranslateFailException("translate failed, non key 'translation', input is %s" % text)
                for item in translation_arr['translation']:
                    items.append(ExtensionResultItem(name=item,
                                                     description=item,
                                                     icon='images/icon.png',
                                                     on_enter=DoNothingAction()))
                return RenderResultListAction(items)
            except ParseQueryError:
                return self.get_action_to_render(name="Incorrect input",
                                                 description="Example: yd apple %s" % text)
            except TranslateFailException as e:
                return self.get_action_to_render(name="translate failed",
                                                 description="reason: %s" % e)
            except Exception as e:
                traceback.print_exc()
                return self.get_action_to_render(name="extension error!",
                                                 description="%s" % e)


class TranslateFailException(Exception):
    pass
