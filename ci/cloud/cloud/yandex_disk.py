"""!

@brief Cloud Tool for Yandex Disk service.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""


import http.client
import json
import os.path

import urllib.request
from urllib.parse import urlparse


class file_type:
    FILE = 'file'
    DIRECTORY = 'dir'


class yandex_disk:
    __REQUEST_ATTEMPTS = 3
    __SERVICE_ADDRESS = "cloud-api.yandex.net:443"

    __HTTP_DISK = "/v1/disk"
    __HTTP_RESOURCES = "/v1/disk/resources"
    __HTTP_RESOURCES_UPLOAD = "/v1/disk/resources/upload"
    __HTTP_RESOURCES_DOWNLOAD = "/v1/disk/resources/download"


    def __init__(self, token):
        self.__token = token


    def get_free_space(self):
        result, response_content = self.__send_request("GET", yandex_disk.__HTTP_DISK)
        if result != 200:
            print("ERROR: Impossible to obtain information about disk.")
            return None

        json_content = json.loads(response_content)
        total_space = int(json_content['total_space'])
        used_space = int(json_content['used_space'])

        free_space = (total_space - used_space) / 1000000

        return free_space


    def folder_content(self, path):
        result, response_content = self.__send_request("GET", yandex_disk.__HTTP_RESOURCES, {"path": path})
        if result != 200:
            print("ERROR: Impossible to list content of folder '%s'." % path)
            return None

        json_content = json.loads(response_content)
        if json_content['type'] != file_type.DIRECTORY:
            print("ERROR: Specified path '%s' is not folder." % path)
            return None

        folder_content = json_content['_embedded']['items']
        result = []

        for file_info in folder_content:
            result.append(file_info['name'])

        return result


    def upload(self, local_path, remote_path):
        if not os.path.isfile(local_path):
            print("ERROR: Impossible to upload non-existed file '%s'." % local_path)
            return False

        file_descriptor = open(local_path, "rb")
        binary_file = file_descriptor.read()
        file_descriptor.close()

        result, response_content = self.__send_request("GET", yandex_disk.__HTTP_RESOURCES_UPLOAD, {"path": remote_path})
        if result != 200:
            print("ERROR: Impossible to obtain link to upload file to '%s' (code: '%d', description: '%s')" % (remote_path, result, response_content))
            return False

        json_content = json.loads(response_content)
        upload_link = json_content['href']
        result = self.__upload_request(binary_file, upload_link)
        if result != 201:
            print("ERROR: Impossible to upload file using link '%s' (code: '%d')." % (upload_link, result))
            return False

        return True


    def download(self, remote_path, local_path):
        if os.path.isfile(local_path):
            print("ERROR: Impossible to download file to path '%s' because file with such name already exists" % local_path)
            return False

        result, response_content = self.__send_request("GET", yandex_disk.__HTTP_RESOURCES_DOWNLOAD, {"path": remote_path})
        if result != 200:
            print("ERROR: Impossible to obtain link to download file from '%s' (code: '%d', description: '%s')" % (remote_path, result, response_content))
            return False

        json_content = json.loads(response_content)
        download_link = json_content['href']
        status, content = self.__download_request(download_link)

        if status != 200:
            print("ERROR: Impossible to download file using link '%s' (code: '%d')." % (download_link, status))
            return False

        file_descriptor = open(local_path, "wb")
        file_descriptor.write(content)
        file_descriptor.close()

        return True


    def delete(self, path):
        result, response_content = self.__send_request("DELETE", yandex_disk.__HTTP_RESOURCES, {"path": path})
        if result not in [202, 204]:
            print("ERROR: Impossible to delete folder (code: '%d', description: '%s')" % (result, response_content))
            return False

        return True


    def create_folder(self, path):
        result, response_content = self.__send_request("PUT", yandex_disk.__HTTP_RESOURCES, {"path": path})
        if result != 201 and result != 409:
            print("ERROR: Impossible to create folder (code: '%d', description: '%s')" % (result, response_content))
            return False

        return True


    def file_exist(self, path):
        result, response_content = self.__send_request("GET", yandex_disk.__HTTP_RESOURCES, {"path": path})
        if result != 200:
            if result == 401:
                raise PermissionError("ERROR: Impossible to obtain information about file '%s' "
                                      "(unauthorized request)." % path)

            return False

        json_content = json.loads(response_content)
        if json_content['type'] != file_type.FILE:
            return False

        return True


    def directory_exist(self, path):
        result, response_content = self.__send_request("GET", yandex_disk.__HTTP_RESOURCES, {"path": path})
        if result != 200:
            if result == 401:
                raise PermissionError("ERROR: Impossible to obtain information about directory '%s' "
                                      "(unauthorized request)." % path)

            return False

        json_content = json.loads(response_content)
        if json_content['type'] != file_type.DIRECTORY:
            return False

        return True


    def __upload_request(self, binary_file, upload_link):
        parse_result = urlparse(upload_link)

        connection = http.client.HTTPSConnection(parse_result.netloc)
        connection.request("PUT", parse_result.path, binary_file, {'Authorization': "OAuth " + self.__token})
        response_status = connection.getresponse().status

        connection.close()

        return response_status


    def __download_request(self, download_link):
        with urllib.request.urlopen(download_link) as url:
            response_status = url.getcode()
            response_content = url.read()

        return response_status, response_content


    def __send_request(self, method, url, params=None):
        connection = http.client.HTTPSConnection(self.__SERVICE_ADDRESS)

        attempt_counter = 0
        response_status, response_content = None, None

        while ((response_status is None) or ((response_status >= 500) and (response_status < 600))) and (attempt_counter < self.__REQUEST_ATTEMPTS):
            url_complete = url
            url_params = params or {}
            for key, value in url_params.items():
                url_complete += ("?%s=%s" % (str(key), str(value)))

            connection.request(method, url_complete, headers={'Authorization': "OAuth " + self.__token})

            response = connection.getresponse()

            response_status = response.status
            response_content = response.read().decode('utf-8')

            attempt_counter += 1

        connection.close()
        return response_status, response_content
