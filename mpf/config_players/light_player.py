from mpf.core.config_player import ConfigPlayer
from mpf.core.utility_functions import Util


class LightPlayer(ConfigPlayer):
    config_file_section = 'light_player'
    show_section = 'lights'
    machine_collection_name = 'lights'

    def play(self, settings, mode=None, caller=None, priority=None,
             play_kwargs=None):

        super().play(settings, mode, caller, priority, play_kwargs)

        if 'lights' in settings:
            settings = settings['lights']

        for light, s in settings.items():
            self.caller_target_map[caller].add(light)

            try:
                light.on(**s)
            except AttributeError:
                self.machine.lights[light].on(**s)

    def clear(self, caller, priority):
        try:
            for light in self.caller_target_map[caller]:
                light.off(priority=priority)
        except KeyError:
            pass

    def get_express_config(self, value):
        value = str(value).replace(' ', '').lower()
        fade = 0
        if '-f' in value:
            composite_value = value.split('-f')
            value = composite_value[0]
            fade = Util.string_to_ms(composite_value[1])

        return dict(brightness=value, fade_ms=fade)

player_cls = LightPlayer