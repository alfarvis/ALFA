#!/usr/bin/env python
from Alfarvis.data_handlers import create_reader_dictionary
from Alfarvis.basic_definitions import DataType, CommandStatus
from Alfarvis import package_directory
import unittest
import os


class TestDataHandlers(unittest.TestCase):

    def setUp(self):
        self.handlers = create_reader_dictionary()

    def test_read_csv(self):
        csv_handler = self.handlers[DataType.csv]
        file_path = os.path.join(package_directory, 'test_data/data.csv')
        keyword_list = ['tumor', 'data']
        pre_eval_res = csv_handler.preRead(file_path, keyword_list)
        res_list = csv_handler.read(file_path, keyword_list, pre_eval_res)
        # Adding logical arrays as categorical will increase the count to 35
        self.assertEqual(len(res_list), 33)
        self.assertEqual(res_list[0].keyword_list, keyword_list)

    def test_read_wrong_csv(self):
        csv_handler = self.handlers[DataType.csv]
        file_path = os.path.join(package_directory, 'resources/random.csv')
        pre_eval_res = csv_handler.preRead(file_path, None)
        res = csv_handler.read(file_path, None, pre_eval_res)
        self.assertEqual(res.command_status, CommandStatus.Error)

    def test_read_image(self):
        image_handler = self.handlers[DataType.image]
        file_path = os.path.join(package_directory, 'test_data/image.jpg')
        keyword_list = ['cell', 'phone', 'image']
        image_handler.read(file_path, keyword_list)
        # Check image is loaded correctly

    def test_read_database(self):
        # Try different databases with some wrong/bad ones
        data_base_handler = self.handlers[DataType.data_base]
        file_path = os.path.join(package_directory,
                                 'resources/file_database.csv')
        keyword_list = ['base', 'database']
        data_base_handler.read(file_path, keyword_list)


if __name__ == '__main__':
    unittest.main()
