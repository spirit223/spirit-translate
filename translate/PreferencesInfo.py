from ulauncher.api.client.EventListener import EventListener


class PreferencesInfo:
    app_id = ''
    app_secrit = ''
    delay = 2


class PreferencesListener(EventListener):
    def on_event(self, event, extension):
        PreferencesInfo.app_id = event.preferences['appId']
        PreferencesInfo.app_secrit = event.preferences['appSecrit']
        PreferencesInfo.app_secrit = event.preferences['delay']


class PreferencesUpdateListener(EventListener):
    def on_event(self, event, extension):
        if event.id == 'appId':
            PreferencesInfo.app_id = event.new_value
        elif event.id == 'appSecrit':
            PreferencesInfo.app_secrit = event.new_value
        elif event.id == 'delay':
            PreferencesInfo.delay = event.new_value