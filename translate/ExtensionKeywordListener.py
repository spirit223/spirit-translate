# -*- coding: utf-8 -*-
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.DoNothingAction import DoNothingAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from translate.LanguageDiscriminator import ParseQueryError, LanguageDiscriminator
from translate.PreferencesInfo import PreferencesInfo
from translate.RequestBuilder import RequestBuilder
import json
import traceback
import threading
import logging

logger = logging.getLogger(__name__)


class ExtensionKeywordListener(EventListener):
    def __init__(self):
        self.tran_count = 0
        self.count = 0


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
        print("trigger KeywordQueryEvent! %d" % ++self.count)
        text = event.get_argument()
        if text is None:
            return self.get_action_to_render(name="translate",
                                             description="Example: yd apple")
        else:
            try:
                res = RequestBuilder.build(text)
                self.tran_count += 1
                # res.data.translation is str array contain translate result
                translated_arr = json.loads(res.data)
                items = []
                if 'translation' not in translated_arr:
                    logger.error(translated_arr)
                    raise TranslateFailException("translate failed, non key 'translation'")
                for item in translated_arr['translation']:
                    items.append(ExtensionResultItem(name=item,
                                                     description='press enter to copy result',
                                                     icon='images/icon.png',
                                                     on_enter=CopyToClipboardAction(item)))
                return RenderResultListAction(items)
            except ParseQueryError:
                return self.get_action_to_render(name="Incorrect input",
                                                 description="Example: yd apple %s" % text)
            except TranslateFailException as e:
                return self.get_action_to_render(name="translate failed",
                                                 description='tran count is %d' % self.tran_count)
            except Exception as e:
                traceback.print_exc()
                return self.get_action_to_render(name="extension error!",
                                                 description='tran count is %d' % self.tran_count)


class TranslateFailException(Exception):
    pass

class CountDown:
    def __init__(self):
        self.countdown_time = PreferencesInfo.delay
