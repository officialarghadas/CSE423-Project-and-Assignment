'''OpenGL extension EXT.index_array_formats

This module customises the behaviour of the 
OpenGL.raw.GL.EXT.index_array_formats to provide a more 
Python-friendly API

Overview (from the spec)
	
	This extends the number of packed vertex formats accepted by
	InterleavedArrays to include formats which specify color indexes
	rather than RGBA colors.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/EXT/index_array_formats.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GL import _types, _glgets
from OpenGL.raw.GL.EXT.index_array_formats import *
from OpenGL.raw.GL.EXT.index_array_formats import _EXTENSION_NAME

def glInitIndexArrayFormatsEXT():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION