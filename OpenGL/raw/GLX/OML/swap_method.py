'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GLX import _types as _cs
# End users want this...
from OpenGL.raw.GLX._types import *
from OpenGL.raw.GLX import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GLX_OML_swap_method'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GLX,'GLX_OML_swap_method',error_checker=_errors._error_checker)
GLX_SWAP_COPY_OML=_C('GLX_SWAP_COPY_OML',0x8062)
GLX_SWAP_EXCHANGE_OML=_C('GLX_SWAP_EXCHANGE_OML',0x8061)
GLX_SWAP_METHOD_OML=_C('GLX_SWAP_METHOD_OML',0x8060)
GLX_SWAP_UNDEFINED_OML=_C('GLX_SWAP_UNDEFINED_OML',0x8063)

