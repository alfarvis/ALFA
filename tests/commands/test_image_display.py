#!/usr/bin/env python3
import unittest
from Alfarvis.basic_definitions import DataType, CommandStatus, DataObject
from Alfarvis import package_directory, create_command_database
from Alfarvis.commands.image_display import ImageDisplay
from skimage.io import imread
import matplotlib.pyplot as plt
import os


class TestImageDisplay(unittest.TestCase):

    def testSearchingImageDisplay(self):
        command_database = create_command_database()
        result = command_database.search(["display", "image"])
        self.assertEqual(len(result), 1)
        result = command_database.search(["show", "image"])
        self.assertEqual(len(result), 1)

    def testDataTypes(self):
        image_command = ImageDisplay()
        argument_types = image_command.argumentTypes()
        self.assertEqual(len(argument_types), 1)
        self.assertTrue(argument_types[0].optional)
        self.assertEqual(argument_types[0].argument_type[0], DataType.image)
        self.assertEqual(argument_types[0].tags, [])

    def testEvaluate(self):
        image_command = ImageDisplay()
        arg = image_command.argumentTypes()[0]
        # Use None when varstore does not have anything stored
        arguments = {arg.keyword: None}
        result_object = image_command.evaluate(**arguments)
        self.assertEqual(result_object.command_status, CommandStatus.Error)

        # Use false data
        data_object = DataObject(123, ['random', 'image'])
        arguments = {arg.keyword: data_object}
        data_object.data = 123
        result_object = image_command.evaluate(**arguments)
        self.assertEqual(result_object.command_status, CommandStatus.Error)
        # No more optional image should be passed by parser:
        result_object = image_command.evaluate(**{arg.keyword: None})
        self.assertEqual(result_object.command_status, CommandStatus.Error)
        # Use real image
        image_data = imread(os.path.join(
            package_directory, 'test_data', 'image.jpg'))
        data_object.data = image_data
        result_object = image_command.evaluate(**arguments)
        self.assertEqual(result_object.command_status, CommandStatus.Success)
        plt.close()


if __name__ == '__main__':
    unittest.main()
