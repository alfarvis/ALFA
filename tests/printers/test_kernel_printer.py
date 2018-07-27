#!/usr/bin/env python3
import unittest
from io import StringIO
from Alfarvis.printers.kernel_printer import KernelPrinter
from Alfarvis.printers import Printer
from unittest.mock import patch


class KernelSubPrinter(KernelPrinter):
    pass


class NonSubclassPrinter(object):
    pass


class TestKernelPrinter(unittest.TestCase):
    def test_kernel_printer(self):
        kernel_printer = KernelPrinter()
        with patch('sys.stdout', new=StringIO()) as fakeOutput:
            kernel_printer.Print('hello world')
            self.assertEqual(fakeOutput.getvalue().strip(), 'hello world')

    def test_kernel_printer_keywords(self):
        kernel_printer = KernelPrinter()
        with patch('sys.stdout', new=StringIO()) as fakeOutput:
            kernel_printer.Print('hello', 'world', sep=',')
            self.assertEqual(fakeOutput.getvalue().strip(), 'hello,world')

    def test_printer_interface(self):
        Printer.selectPrinter(KernelPrinter())
        with patch('sys.stdout', new=StringIO()) as fakeOutput:
            Printer.Print('hello', 'world', sep=',')
            self.assertEqual(fakeOutput.getvalue().strip(), 'hello,world')

    def test_fail_printer_interface(self):
        self.assertRaises(RuntimeError, Printer.selectPrinter, None)
        self.assertRaises(RuntimeError, Printer.selectPrinter, NonSubclassPrinter())
        Printer.selectPrinter(KernelSubPrinter())


if __name__ == "__main__":
    unittest.main()
