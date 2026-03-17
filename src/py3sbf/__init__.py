# This makes py3sbf a package

# To allow 'from py3sbf import pysbf'
from . import pysbf
# You could also expose specific things from pysbf directly if desired:
# from .pysbf import load