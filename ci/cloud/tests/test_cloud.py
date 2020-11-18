"""!

@brief Tests for Cloud Tool.
@details In case of running unit-tests make sure that environment variable with name 'CLOUD_TOKEN' exists. This
         variable should contains token for authorization.

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""


import os
import unittest


from cloud.task import task
from cloud.task_handler import task_handler
from cloud.yandex_disk import yandex_disk


class cloud_unit_test(unittest.TestCase):
    def setUp(self):
        token = os.environ.get('CLOUD_TOKEN')
        self.assertIsNotNone(token)

        self.__token = token
        self.__disk_client = yandex_disk(token)


    def test_get_info(self):
        free_space = self.__disk_client.get_free_space()
        self.assertGreater(free_space, 0)


    def test_get_content_folder(self):
        self.assertIsNotNone(self.__disk_client.folder_content("/"))


    def test_create_delete_folder(self):
        folder_name = "/test_folder1"
        self.assertTrue(self.__disk_client.create_folder(folder_name))
        self.assertTrue(self.__disk_client.directory_exist(folder_name))

        content = self.__disk_client.folder_content(folder_name)
        self.assertEqual(len(content), 0)

        self.assertTrue(self.__disk_client.delete(folder_name))
        self.assertFalse(self.__disk_client.directory_exist(folder_name))


    def test_upload_file(self):
        folder_name = "/test_folder2"
        file_name = "test_file1.txt"
        file_path = folder_name + "/" + file_name

        file_descriptor = open(file_name, "w+")
        file_descriptor.write('Hello World! Hello PyClustering!')
        file_descriptor.close()

        self.assertTrue(self.__disk_client.create_folder(folder_name))
        self.assertFalse(self.__disk_client.file_exist(file_path))

        self.assertTrue(self.__disk_client.upload(file_name, file_path))
        self.assertTrue(self.__disk_client.file_exist(file_path))

        self.assertTrue(self.__disk_client.delete(file_path))
        self.assertFalse(self.__disk_client.file_exist(file_path))

        self.assertTrue(self.__disk_client.delete(folder_name))
        os.remove(file_name)


    def test_upload_download(self):
        folder_name = "/test_folder3"
        file_name1 = "test_file2.txt"
        file_name2 = "test_file3.txt"
        file_path = folder_name + "/" + file_name1

        file_descriptor = open(file_name1, "w+")
        content_file1 = "Hello World! Hello PyClustering! Hello PyClustering!"
        file_descriptor.write(content_file1)
        file_descriptor.close()

        self.assertTrue(self.__disk_client.create_folder(folder_name))
        self.assertFalse(self.__disk_client.file_exist(file_path))

        self.assertTrue(self.__disk_client.upload(file_name1, file_path))
        self.assertTrue(self.__disk_client.file_exist(file_path))

        self.assertTrue(self.__disk_client.download(file_path, file_name2))
        self.assertTrue(os.path.isfile(file_name2))

        file_descriptor = open(file_name2, "r")
        content_file2 = file_descriptor.read()
        file_descriptor.close()

        self.assertEqual(content_file1, content_file2)

        self.assertTrue(self.__disk_client.delete(folder_name))
        os.remove(file_name1)
        os.remove(file_name2)


    def test_command_create(self):
        folder_name = "/test_folder4"

        client_task = task("mkdir", [folder_name])
        task_handler(self.__token).process(client_task)

        self.assertTrue(self.__disk_client.directory_exist(folder_name))
        self.assertTrue(self.__disk_client.delete(folder_name))


    def test_command_upload_download(self):
        folder_name = "/test_folder5"
        file_name1 = "test_file4.txt"
        file_name2 = "test_file5.txt"
        file_path = folder_name + "/" + file_name1

        file_descriptor = open(file_name1, "w+")
        content_file1 = "Hello PyClustering! Hello PyClustering! Hello PyClustering!"
        file_descriptor.write(content_file1)
        file_descriptor.close()

        client_task = task("mkdir", [folder_name])
        task_handler(self.__token).process(client_task)

        self.assertTrue(self.__disk_client.directory_exist(folder_name))

        client_task = task("upload", [file_name1, file_path])
        task_handler(self.__token).process(client_task)

        self.assertTrue(self.__disk_client.file_exist(file_path))

        client_task = task("download", [file_path, file_name2])
        task_handler(self.__token).process(client_task)

        self.assertTrue(os.path.isfile(file_name2))

        file_descriptor = open(file_name2, "r")
        content_file2 = file_descriptor.read()
        file_descriptor.close()

        self.assertEqual(content_file1, content_file2)

        self.assertTrue(self.__disk_client.delete(folder_name))
        os.remove(file_name1)
        os.remove(file_name2)
