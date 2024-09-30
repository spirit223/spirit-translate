from ulauncher.api.client.EventListener import EventListener


class PreferencesInfo:
    _app_id = ''
    _app_secrit = ''
    _delay = 2

    @staticmethod
    def get_delay():
        print('get delay is %s' % PreferencesInfo._delay)
        return PreferencesInfo._delay

    @staticmethod
    def get_app_id():
        print('get app_id is %s' % PreferencesInfo._delay)
        return PreferencesInfo._app_id

    @staticmethod
    def get_app_secrit():
        print('get app_secrit is %s' % PreferencesInfo._delay)
        return PreferencesInfo._app_secrit

    @staticmethod
    def get_preferences():
        time = PreferencesInfo.get_delay()
        id = PreferencesInfo.get_app_id()
        secrit = PreferencesInfo.get_app_secrit()
        return {'delay':time, 'id':id, 'secrit':secrit}

class PreferencesListener(EventListener):
    def on_event(self, event, extension):
        print('update preferences')
        PreferencesInfo._app_id = event.preferences['appId']
        PreferencesInfo._app_secrit = event.preferences['appSecrit']
        PreferencesInfo._delay = event.preferences['delay']
        print('PreferencesInfo.delay is %s' % PreferencesInfo._delay)


class PreferencesUpdateListener(EventListener):
    def on_event(self, event, extension):
        print('preferences updated')
        if event.id == 'appId':
            PreferencesInfo._app_id = event.new_value
        elif event.id == 'appSecrit':
            PreferencesInfo._app_secrit = event.new_value
        elif event.id == 'delay':
            PreferencesInfo._delay = event.new_value
            print('PreferencesInfo.delay is %s' % PreferencesInfo._delay)