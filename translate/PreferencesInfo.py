from ulauncher.api.client.EventListener import EventListener


class PreferencesInfo:
    _app_id = ''
    _app_secrit = ''
    _delay = 2

    @staticmethod
    def get_delay():
        return float(PreferencesInfo._delay)

    @staticmethod
    def get_app_id():
        return PreferencesInfo._app_id

    @staticmethod
    def get_app_secrit():
        return PreferencesInfo._app_secrit

    @staticmethod
    def get_preferences():
        time = PreferencesInfo.get_delay()
        id = PreferencesInfo.get_app_id()
        secrit = PreferencesInfo.get_app_secrit()
        return {'delay':time, 'id':id, 'secrit':secrit}

class PreferencesListener(EventListener):
    def on_event(self, event, extension):
        PreferencesInfo._app_id = event.preferences['appId']
        PreferencesInfo._app_secrit = event.preferences['appSecrit']
        PreferencesInfo._delay = event.preferences['delay']


class PreferencesUpdateListener(EventListener):
    def on_event(self, event, extension):
        print('preferences updated')
        if event.id == 'appId':
            PreferencesInfo._app_id = event.new_value
        elif event.id == 'appSecrit':
            PreferencesInfo._app_secrit = event.new_value
        elif event.id == 'delay':
            PreferencesInfo._delay = event.new_value