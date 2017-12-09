#!/usr/bin/env python2
import re
from Alfarvis import alpha_module_dictionary

if __name__ == "__main__":
    print("Input a text to receive response from Alfarvis")
    print "Enter Bye to close the program"
    #print(">", end=" ")
    input_text = ''
    pattern = re.compile('\w*(L|l)oad (A|a)l(f|ph)a\s*\w* (\d+.?\d*)\w*')
    alpha = alpha_module_dictionary[1.0]()
    while (input_text != 'Bye' and input_text != 'bye'):
        try:
            input_text = raw_input('> ')
            match_out = pattern.match(input_text)
            if match_out:
                print match_out.groupdict
                version = float(match_out.group(4))
                print "Trying to load alpha v", version
                if version in alpha_module_dictionary:
                    try:
                        alpha = alpha_module_dictionary[version]()
                        print "Successfully loaded alpha version", version
                    except:
                        print "Cannot instantiate alpha"
                        alpha = None
                else:
                    print "No existing version: ", version
            elif alpha is not None:
                print alpha(input_text)
            else:
                print "No alpha loaded!"
        except (KeyboardInterrupt, EOFError) as e:
            print ""
            break
    print "Closing Program! Good Bye."
