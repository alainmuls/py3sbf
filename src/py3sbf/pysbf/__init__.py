# /home/amuls/amPython/py3sbf/pysbf/__init__.py
"""
pysbf - A Python module to parse Septentrio Binary Format (SBF) files.
"""
from .sbf import load

# You can also expose other elements if needed, for example:
# from .parsers import SomeParserClass
# from .blocks import BLOCKNAMES

__all__ = ['load']