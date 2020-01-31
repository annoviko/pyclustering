"""!

@brief Cloud Tool for Yandex Disk service.
@details Cloud Tool is used for storing binaries of pyclustering library.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
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


import sys


from cloud.task import task
from cloud.task_handler import task_handler


def run():
    if len(sys.argv) == 2:
        client_task = task(sys.argv[1], [])
        token = ""

    elif len(sys.argv) < 3:
        raise SyntaxError("ERROR: Incorrect amount of arguments '%d' "
                          "(please, see 'python3 ci/cloud --help')." % len(sys.argv))

    else:
        token = sys.argv[1]
        action = sys.argv[2]
        params = sys.argv[3:]

        client_task = task(action, params)

    task_handler(token).process(client_task)


if __name__ == '__main__':
    try:
        run()
        exit(0)

    except Exception as error:
        print(error)
        exit(-1)
