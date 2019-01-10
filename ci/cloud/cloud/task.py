"""!

@brief Cloud Tool for Yandex Disk service.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2019
@copyright GNU Public License

@cond GNU_PUBLIC_LICENSE
    PyClustering is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    PyClustering is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
@endcond

"""


class task:
    def __init__(self, action, params):
        self.__action = action.lower()
        self.__params = self.__parse_arguments(params)


    def __parse_arguments(self, params):
        action_params = {}
        if self.__action == 'upload' or self.__action == 'download':
            if len(params) != 2:
                raise ValueError("ERROR: Incorrect amount of arguments ('%d' instead of '2')." % len(params))

            action_params['from'] = params[0]
            action_params['to'] = params[1]

        elif self.__action == 'mkdir':
            if len(params) != 1:
                raise ValueError("ERROR: Incorrect amount of arguments ('%d' instead of '1')." % len(params))

            action_params['folder'] = params[0]

        elif self.__action == 'rm':
            if len(params) != 1:
                raise ValueError("ERROR: Incorrect amount of arguments ('%d' instead of '1')." % len(params))

            action_params['path'] = params[0]

        elif self.__action == 'get_third_party':
            if len(params) != 2 and len(params) != 3:
                raise ValueError("ERROR: Incorrect amount of arguments ('%d' instead of '2' or '3')." % len(params))

            action_params['os'] = params[0]
            action_params['platform'] = params[1]

            action_params['to'] = None
            if len(params) > 2:
                action_params['to'] = params[2]

            if action_params['os'] not in ['windows', 'linux']:
                raise ValueError("ERROR: Unsupported operating system '%s' (available: 'linux', 'windows')." % action_params['os'])

            if action_params['platform'] not in ['x64', 'x86']:
                raise ValueError("ERROR: Unsupported platform '%s' (available: 'x86', 'x64')." % action_params['platform'])

        elif self.__action in ['-h', '--help', 'help']:
            self.__action = 'help'

        else:
            raise ValueError("ERROR: Unknown action is specified '%s'." % self.__action)

        return action_params


    def get_action(self):
        return self.__action


    def get_param(self, name):
        if name not in self.__params:
            raise IndexError("ERROR: Action '%s' does not have parameter '%s'" % (self.__action, len(self.__params)))

        return self.__params[name]