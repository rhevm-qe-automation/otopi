#
# otopi -- plugable installer
# Copyright (C) 2012-2013 Red Hat, Inc.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
#


"""Command provider."""


import os


from otopi import command
from otopi import constants
from otopi import plugin
from otopi import util


@util.export
class Plugin(plugin.PluginBase, command.CommandBase):
    """Command provider.

    Environment:
        SysEnv.COMMAND_PATH -- search path.

    """
    def __init__(self, context):
        super(Plugin, self).__init__(context=context)

    def _search(self):
        searchPath = self.environment[
            constants.SysEnv.COMMAND_PATH
        ].split(':')
        for cmd in self.command.enum():
            if self.command.get(command=cmd, optional=True) is None:
                for path in searchPath:
                    cmdPath = os.path.join(path, cmd)
                    if os.path.exists(cmdPath):
                        self.command.set(command=cmd, path=cmdPath)

    @plugin.event(
        stage=plugin.Stages.STAGE_INIT,
        priority=plugin.Stages.PRIORITY_HIGH,
    )
    def _init(self):
        self.environment.setdefault(
            constants.SysEnv.COMMAND_PATH,
            constants.Defaults.COMMAND_SEARCH_PATH
        )
        self.context.registerCommand(command=self)

    @plugin.event(
        name=constants.Stages.SYSTEM_COMMAND_DETECTION,
        stage=plugin.Stages.STAGE_PROGRAMS,
    )
    def _programs(self):
        self._search()

    @plugin.event(
        name=constants.Stages.SYSTEM_COMMAND_REDETECTION,
        stage=plugin.Stages.STAGE_MISC,
        priority=plugin.Stages.PRIORITY_HIGH,
    )
    def _misc(self):
        self._search()


# vim: expandtab tabstop=4 shiftwidth=4
