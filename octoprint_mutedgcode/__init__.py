# coding=utf-8
from __future__ import absolute_import

### (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin, settings and asset plugin. Feel free to add or remove mixins
# as necessary.
#
# Take a look at the documentation on what other plugin mixins are available.

import octoprint.plugin


class MutedgcodePlugin(octoprint.plugin.SettingsPlugin,
                       octoprint.plugin.AssetPlugin,
                       octoprint.plugin.TemplatePlugin,
                       octoprint.plugin.StartupPlugin
                       ):

    def __init__(self):
        self.muted_commands = []

    # ~~ SettingsPlugin mixin

    def get_settings_defaults(self):
        return {
            "commands": []
        }

    def on_after_startup(self):
        self.muted_commands = [v["command"] for v in self._settings.get(["commands"]) if v["enabled"] is True]

    def on_settings_save(self, data):
        octoprint.plugin.SettingsPlugin.on_settings_save(self, data)
        self.muted_commands = [v["command"] for v in self._settings.get(["commands"]) if v["enabled"] is True]

    # ~~ AssetPlugin mixin

    def get_assets(self):
        return {
            "css": ["css/mutedgcode.css"],
            "js": ["js/mutedgcode.js"]
        }

    # ~~ TemplatePlugin mixin

    def get_template_configs(self):
        return [{'type': "sidebar", 'icon': "microphone-slash", 'custom_bindings': True,
                 'template': "mutedgcode_sidebar.jinja2",
                 'template_header': "mutedgcode_sidebar_header.jinja2"}]

    # ~~ Gcode Queueing hook

    def processGCODE(self, comm_instance, phase, cmd, cmd_type, gcode, *args, **kwargs):
        if gcode not in self.muted_commands:
            return

        self._logger.debug("muting command: {}".format(gcode))
        return None,

    # ~~ Softwareupdate hook

    def get_update_information(self):
        return {
            "mutedgcode": {
                "displayName": "Muted GCode",
                "displayVersion": self._plugin_version,
                "type": "github_release",
                "user": "jneilliii",
                "repo": "OctoPrint-MutedGCode",
                "current": self._plugin_version,
                "pip": "https://github.com/jneilliii/OctoPrint-MutedGCode/archive/{target_version}.zip",
            }
        }


__plugin_name__ = "Muted GCode"
__plugin_pythoncompat__ = ">=3,<4"  # Only Python 3


def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = MutedgcodePlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.comm.protocol.gcode.queuing": __plugin_implementation__.processGCODE,
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }
