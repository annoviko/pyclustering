"""!

@brief Cloud Tool for Yandex Disk service.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""


import os
import zipfile

from cloud.yandex_disk import yandex_disk



class task_handler:
    __LOCAL_PATH_THIRD_PARTIES_LIBS = "ccore/external/libs"
    __LOCAL_PATH_THIRD_PARTIES_INCLUDE = "ccore/external/include"
    __LOCAL_OS_NAMES = {"windows": "win",
                        "linux": "linux",
                        "macos": "macos"}

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

        elif action == 'get_bin':
            self.__get_bin(task.get_param('branch'), task.get_param('os'), task.get_param('platform'))

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


    def __get_bin(self, branch, osys, platform):
        dict_prefix = {"macos": "lib", "linux": "lib", "windows": ""}
        dict_extension = {"macos": "so", "linux": "so", "windows": "dll"}
        dict_os = {"macos": "macos", "linux": "linux", "windows": "win"}

        disk_client = yandex_disk(self.__token)

        remote_path_builds = "/%s/%s/%s" % (branch, osys, platform)
        builds = disk_client.folder_content(remote_path_builds)

        if len(builds) == 0:
            print("WARNING: No builds for system '%s' on platform '%s' (branch '%s')." % (osys, platform, branch))
            return

        sorted_builds = sorted(builds)
        latest_build = sorted_builds[-1]

        remote_path_binary = "%s/%s/%spyclustering.%s" % (remote_path_builds, latest_build, dict_prefix[osys], dict_extension[osys])

        script_path = os.path.dirname(os.path.realpath(__file__))
        local_path_binary = "%s/../../../pyclustering/core/%s/%s/%spyclustering.%s" % (script_path, platform, dict_os[osys], dict_prefix[osys], dict_extension[osys])
        local_path_binary = os.path.realpath(local_path_binary)

        self.__download(remote_path_binary, local_path_binary)
        print("Latest build for '%s' '%s' on branch '%s' is '%s'" % (osys, platform, branch, builds[-1]))


    def __third_party_libs(self, operating_system, platform, to_path):
        disk_client = yandex_disk(self.__token)

        remote_path_libs = "/third_party/" + operating_system + "/" + platform
        if not disk_client.directory_exist(remote_path_libs):
            raise FileExistsError("ERROR: Third party folder '%s' is not found on the cloud." % remote_path_libs)

        lib_files = disk_client.folder_content(remote_path_libs)
        if lib_files is None:
            raise FileExistsError("ERROR: Impossible to get content of third party folder '%s'." % remote_path_libs)

        if len(lib_files) == 0:
            print("WARNING: No third parties for system '%s' on platform '%s'." % (operating_system, platform))
            return

        if to_path is None:
            script_path = os.path.dirname(os.path.realpath(__file__))
            local_binary_folder = script_path + "/../../../" + task_handler.__LOCAL_PATH_THIRD_PARTIES_LIBS + "/" + operating_system + "/" + platform
        else:
            local_binary_folder = to_path

        for file in lib_files:
            remote_file_path = remote_path_libs + "/" + file
            local_file_path = local_binary_folder + "/" + file

            self.__download(remote_file_path, local_file_path)


    def __third_party_include(self, to_path):
        disk_client = yandex_disk(self.__token)

        remote_path_inc = "/third_party/include"
        if not disk_client.directory_exist(remote_path_inc):
            raise FileExistsError("ERROR: Third party folder '%s' is not found on the cloud." % remote_path_inc)

        inc_files = disk_client.folder_content(remote_path_inc)
        if inc_files is None:
            raise FileExistsError("ERROR: Impossible to get content of third party folder '%s'." % remote_path_inc)

        if len(inc_files) == 0:
            print("WARNING: No include third parties.")
            return

        if to_path is None:
            script_path = os.path.dirname(os.path.realpath(__file__))
            local_include_folder = script_path + "/../../../" + task_handler.__LOCAL_PATH_THIRD_PARTIES_INCLUDE
        else:
            local_include_folder = to_path

        for file in inc_files:
            include_library_name = os.path.splitext(file)[0]
            include_library_path = local_include_folder + "/" + include_library_name
            if os.path.isdir(include_library_path):
                print("WARNING: Include library folder already exists.")
                continue

            remote_file_path = remote_path_inc + "/" + file
            local_file_path = local_include_folder + "/" + file

            if os.path.isfile(local_file_path) is True:
                os.remove(local_file_path)

            self.__download(remote_file_path, local_file_path)

            zip_archive = zipfile.ZipFile(local_file_path, 'r')
            zip_archive.extractall(local_include_folder)
            zip_archive.close()

            os.remove(local_file_path)


    def __third_party(self, operating_system, platform, to_path):
        self.__third_party_libs(operating_system, platform, to_path)
        self.__third_party_include(to_path)


    def __help(self):
        print("Following commands are supported by the tool:")
        print(" upload <from> <to>                      - upload file or folder from local machine path to remote path on clound.")
        print(" download <from> <to>                    - download file or folder from remote path on cloud to local machine.")
        print(" rm <path>                               - remove file or folder on cloud.")
        print(" mkdir <path>                            - create folder on cloud.")
        print(" get_third_party <os> <platform> <to>    - download third party from cloud for specific system (linux, windows, macos) and platform (32-bit, 64-bit)\n"
              "                                           to specific folder on local machine.")
        print(" get_bin <branch> <os> <platform>        - download latest binary file for particular branch, system (linux, windows, macos) and platform (32-bit, 64-bit).")
        print("")
        print("Example:")
        print(" python3 ci/cloud $CLOUD_TOKEN get_third_party windows 64-bit")
