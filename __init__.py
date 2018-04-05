"""
Alfarvis

Text based parsing tool
"""
import os

package_directory = os.path.dirname(os.path.abspath(__file__))

from Alfarvis.alpharvis_versions import create_alpha_module_dictionary
from Alfarvis.commands import create_command_database
import Alfarvis.basic_definitions
import Alfarvis.history
