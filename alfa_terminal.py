#!/usr/bin/env python3
"""
Main executable that calls alpha with specified version
and facilitates communication between user and alpha
through command line
"""
import re
from Alfarvis import create_alpha_module_dictionary
from Alfarvis.printers import Printer
from Alfarvis.printers.kernel_printer import KernelPrinter
from Alfarvis.windows import Window
from Alfarvis.windows.regular_window import RegularWindow

if __name__ == "__main__":  # pragma: no cover
    # Create alpha module dictionary
    alpha_module_dictionary = create_alpha_module_dictionary()
    Printer.selectPrinter(KernelPrinter())
    Window.selectWindowType(RegularWindow)
    ThreadPoolManager.initialize()
    print("Input a text to receive response from Alfarvis")
    print("Enter Bye to close the program")
    #print(">", end=" ")
    input_text = ''
    pattern = re.compile('(L|l)oad (A|a)l(f|ph)a\s*\w*\s*(\d+.?\d*)\w*')
    latest_version = max(alpha_module_dictionary.keys())
    alpha = alpha_module_dictionary[latest_version]()
    while (input_text != 'Bye' and input_text != 'bye'):
        try:
            input_text = input('> ')
            match_out = pattern.search(input_text)
            if match_out:
                print(match_out.groupdict)
                version = float(match_out.group(4))
                print("Trying to load alpha v", version)
                if version in alpha_module_dictionary:
                    try:
                        alpha = alpha_module_dictionary[version]()
                        print("Successfully loaded alpha version", version)
                    except:
                        print("Cannot instantiate alpha")
                        alpha = None
                else:
                    print("No existing version: ", version)
            elif alpha is not None:
                print(alpha(input_text))
            else:
                print("No alpha loaded!")
        except (KeyboardInterrupt, EOFError) as e:
            print("")
            break
    print("closing threads!")
    ThreadPoolManager.close()
    print("Closing Program! Good Bye.")
