"""!

@brief Cloud Tool for Yandex Disk service.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2018
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


import os

from cloud.client.yandex_disk import yandex_disk


class task_handler:
    def __init__(self, token):
        self.__token = token


    def process(self, client_task):
        action = client_task.get_action()
        if action == 'upload':
            self.__upload(client_task.get_param('from'), client_task.get_param('to'))

        elif action == 'download':
            self.__download(client_task.get_param('from'), client_task.get_param('to'))

        elif action == 'mkdir':
            self.__mkdir(client_task.get_param('folder'))


    def __upload(self, from_path, to_path):
        if not os.path.isfile(from_path):
            raise FileExistsError("ERROR: File '%s' on local machine does not exist." % from_path)

        disk_client = yandex_disk(self.__token)
        if disk_client.file_exist(to_path):
            print("WARNING: File '%s' already exists on the cloud and it will be overwritten." % to_path)
            if not disk_client.delete(to_path):
                raise RuntimeError("ERROR: Impossible to remove file '%s'." % to_path)

        disk_client.upload(from_path, to_path)


    def __download(self, from_path, to_path):
        if os.path.isfile(to_path):
            print("WARNING: File '%s' already exists on the local machine and it will be overwritten." % to_path)
            os.remove(to_path)

        disk_client = yandex_disk(self.__token)
        if disk_client.file_exist(from_path) is False:
            raise FileExistsError("ERROR: File '%s' does not exist on the cloud." % from_path)

        disk_client.download(from_path, to_path)


    def __mkdir(self, folder):
        disk_client = yandex_disk(self.__token)
        if disk_client.file_exist(folder):
            print("WARNING: Folder '%s' already exists." % folder)
            return

        disk_client.create_folder(folder)
