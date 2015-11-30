from distutils.core import setup, Extension

module = Extension('testModule', sources = ['testModule.c'])

setup(name='PackageName', 
	version='1.0',
	description = 'This is a package for testModule',
    ext_modules=[module])