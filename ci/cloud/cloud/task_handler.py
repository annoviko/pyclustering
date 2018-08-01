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

from cloud.yandex_disk import yandex_disk



class task_handler:
    __LOCAL_PATH_THIRD_PARTIES = "ccore/external/libs"
    __LOCAL_OS_NAMES = { "windows" : "win",
                         "linux" : "linux"  }

    def __init__(self, token):
        self.__token = token


    def process(self, task):
        action = task.get_action()
        if action == 'upload':
            self.__upload(task.get_param('from'), task.get_param('to'))

        elif action == 'download':
            self.__download(task.get_param('from'), task.get_param('to'))

        elif action == 'mkdir':
            self.__mkdir(task.get_param('folder'))

        elif action == 'rm':
            self.__rm(task.get_param('path'))

        elif action == 'get_third_party':
            self.__third_party(task.get_param('os'), task.get_param('platform'), task.get_param('to'))

        elif action == 'help':
            self.__help()

        else:
            raise RuntimeError("ERROR: Unknown action is specified '%s'." % action)


    def __upload(self, from_path, to_path):
        if not os.path.isfile(from_path):
            raise FileExistsError("ERROR: File '%s' on local machine does not exist." % from_path)

        disk_client = yandex_disk(self.__token)
        if disk_client.file_exist(to_path):
            print("WARNING: File '%s' already exists on the cloud and it will be overwritten." % to_path)
            if not disk_client.delete(to_path):
                raise RuntimeError("ERROR: Impossible to remove file '%s'." % to_path)

        if disk_client.upload(from_path, to_path) is True:
            print("INFO: File '%s' is successfully uploaded to '%s'." % (from_path, to_path))


    def __download(self, from_path, to_path):
        if os.path.isfile(to_path):
            print("WARNING: File '%s' already exists on the local machine and it will be overwritten." % to_path)
            os.remove(to_path)

        disk_client = yandex_disk(self.__token)
        if disk_client.file_exist(from_path) is False:
            raise FileExistsError("ERROR: File '%s' does not exist on the cloud." % from_path)

        if disk_client.download(from_path, to_path) is True:
            print("INFO: File '%s' is successfully downloaded to '%s'." % (from_path, to_path))


    def __mkdir(self, folder):
        disk_client = yandex_disk(self.__token)
        if disk_client.file_exist(folder):
            print("INFO: Folder '%s' already exists." % folder)
            return

        if disk_client.create_folder(folder) is True:
            print("INFO: Folder '%s' is successfully created." % folder)


    def __rm(self, path):
        disk_client = yandex_disk(self.__token)
        if disk_client.file_exist(path) or disk_client.directory_exist(path):
            disk_client.delete(path)
            print("INFO: '%s' is successfully removed." % path)

        else:
            print("WARNING: File or folder '%s' is not found." % path)


    def __third_party(self, operating_system, platform, to_path):
        disk_client = yandex_disk(self.__token)
        remote_path = "/third_party/" + operating_system + "/" + platform
        if not disk_client.directory_exist(remote_path):
            raise FileExistsError("ERROR: Third party folder '%s' is not found on the cloud." % remote_path)

        files = disk_client.folder_content(remote_path)
        if files is None:
            raise FileExistsError("ERROR: Impossible to get content of third party folder '%s'." % remote_path)

        if len(files) == 0:
            print("WARNING: No third parties for system '%s' on platform '%s'." % (operating_system, platform))
            return

        if to_path is None:
            script_path = os.path.dirname(os.path.realpath(__file__))
            local_binary_folder = script_path + "/../../../" + task_handler.__LOCAL_PATH_THIRD_PARTIES + "/" + operating_system + "/" + platform
        else:
            local_binary_folder = to_path

        for file in files:
            remote_file_path = remote_path + "/" + file
            local_file_path = local_binary_folder + "/" + file

            self.__download(remote_file_path, local_file_path)


    def __help(self):
        print("Following commands are supported by the tool:")
        print(" upload <from> <to>                    - upload file or folder from local machine path to remote path on clound.")
        print(" download <from> <to>                  - download file or folder from remote path on cloud to local machine.")
        print(" rm <path>                             - remove file or folder on cloud.")
        print(" mkdir <path>                          - create folder on cloud.")
        print(" get_third_party <os> <platform> <to>  - download third party libraries from cloud for specific operating system"
              " (linux or windows) and platform (x64 or x86) to specific folder on local machine.")
        print("")
        print("Example:")
        print(" python3 ci/cloud $CLOUD_TOKEN get_third_party windows x64")
