import re

class LanguageDiscriminator:
    def __init__(self):
        pass

    @staticmethod
    def detect_language(text: str):
        """
        detects the language of a given text

        if the number of english characters is greater than the chinese number of characters, return en
        else return zh-CHS

        note: the number of chinese and english characters equal, return zh-CHS

        any other condition will raise ParseQueryError
        :param text: need to judge the language
        :return: 'zh-cn' or 'en'
        :raise ParseQueryError: any other condition
        """
        if not text or not str:
            raise ParseQueryError(str('nothing content or invalid length'))
        # filter out special characters
        # cleaned_text = re.sub(r'[^a-zA-Z\u4e00-\u9fa5]', '', text)

        # count the number of chinese and english characters
        chinese_count = len(re.findall(r'[\u4e00-\u9fa5]', text))
        english_count = len(re.findall(r'[a-zA-Z]', text))

        if chinese_count == 0 and english_count == 0:
            raise ParseQueryError("text [%s] parse failed" % text)
        elif chinese_count > english_count:
            return 'zh-CHS'
        elif english_count > chinese_count:
            return 'en'
        elif english_count == chinese_count:
            return 'zh-CHS'
        else:
            raise ParseQueryError("text [%s] parse failed" % text)



class ParseQueryError(Exception):
    pass