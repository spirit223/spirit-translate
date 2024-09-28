from ulauncher.api.client.EventListener import EventListener


class PreferencesListener(EventListener):
    app_id = ''
    app_secrit = ''
    def on_event(self, event, extension):
        PreferencesListener.app_id = event.preferences['appId']
        PreferencesListener.app_secrit = event.preferences['appSecrit']

class PreferencesUpdateListener(EventListener):
    def on_event(self, event, extension):
        print(event.id['appId'])
        PreferencesListener.app_id = event.id('appId')
        PreferencesListener.app_secrit = event.id('appSecret')