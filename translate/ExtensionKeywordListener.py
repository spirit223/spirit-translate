# -*- coding: utf-8 -*-
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.DoNothingAction import DoNothingAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from translate.LanguageDiscriminator import ParseQueryError
from translate.PreferencesInfo import PreferencesInfo
from translate.RequestBuilder import RequestBuilder
import json
import traceback
import threading
import logging
import queue

logger = logging.getLogger(__name__)


class ExtensionKeywordListener(EventListener):
    resultQueue = queue.Queue()

    def __init__(self):
        self.tran_count = 0
        self.timer = None

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

    def do_translate(self, text):
        try:
            response = RequestBuilder.build(text)
            self.tran_count += 1
            translated_arr = json.loads(response.data)
            if 'translation' not in translated_arr:
                print("nothing translated result, [%s]" % translated_arr)
                raise TranslateFailException("translate failed, non key 'translation'")
            items = []
            for item in translated_arr['translation']:
                items.append(ExtensionResultItem(name=item,
                                                 description='press enter to copy result',
                                                 icon='images/icon.png',
                                                 on_enter=CopyToClipboardAction(item)))
            ExtensionKeywordListener.resultQueue.put(RenderResultListAction(items))
        except ParseQueryError:
            traceback.print_exc()
            ExtensionKeywordListener.resultQueue.put(RenderResultListAction(self.get_action_to_render(name="Incorrect input",
                                         description="Example: yd apple %s" % text,
                                         on_enter=DoNothingAction())))
        except TranslateFailException as e:
            traceback.print_exc()
            ExtensionKeywordListener.resultQueue.put(self.get_action_to_render(name="translate failed",
                                         description='tran count is %d' % self.tran_count,
                                         on_enter=DoNothingAction()))

    def on_event(self, event, extension):
        text = event.get_argument()
        if text is None:
            return self.get_action_to_render(name="translate",
                                             description="Example: yd apple")
        else:
            if self.timer:
                self.timer.cancel()
            if not ExtensionKeywordListener.resultQueue.empty():
                ExtensionKeywordListener.resultQueue = queue.Queue()
            self.timer = threading.Timer(PreferencesInfo.get_delay(), self.do_translate, args=(text,))
            self.timer.start()
            print('timer is running, delay is %s' % PreferencesInfo.get_delay())
            self.timer.join()
            return ExtensionKeywordListener.resultQueue.get()


class TranslateFailException(Exception):
    pass

