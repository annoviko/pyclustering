"""!

@brief Cloud Tool for Yandex Disk service.
@details Cloud Tool is used for storing binaries of pyclustering library.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

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
