/*
 * View model for Muted GCode
 *
 * Author: jneilliii
 * License: AGPLv3
 */
$(function() {
    function MutedgcodeViewModel(parameters) {
        var self = this;

        self.settingsViewModel = parameters[0];
        self.muted_commands = ko.observableArray();

        self.onBeforeBinding = function(){
            self.muted_commands(self.settingsViewModel.settings.plugins.mutedgcode.commands());
        };

        self.onSettingsBeforeSave = function(){
            self.settingsViewModel.settings.plugins.mutedgcode.commands(self.muted_commands());
        };

        self.toggleCommand = function(data){
            self.settingsViewModel.saveData();
            return true;
        };

        self.addCommand = function(){
            self.muted_commands.push({'command': ko.observable($('#mutedgcode_command').val()), 'enabled': ko.observable(true)});
            self.muted_commands.sort(function (left, right) {
                return left.command() === right.command() ? 0 : left.command() < right.command() ? -1 : 1;
            });
            self.settingsViewModel.saveData();
            $('#mutedgcode_command').val('');
        };

        self.removeCommand = function(data){
            self.muted_commands.remove(data);
            self.settingsViewModel.saveData();
        };
    }

    OCTOPRINT_VIEWMODELS.push({
        construct: MutedgcodeViewModel,
        dependencies: [ "settingsViewModel" ],
        elements: [ "#sidebar_plugin_mutedgcode_wrapper" ]
    });
});
