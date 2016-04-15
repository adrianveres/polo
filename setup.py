from setuptools import setup
from distutils.core import Extension
from distutils.command.sdist import sdist as _sdist

import numpy

try:
    from Cython.Distutils import build_ext
except ImportError:
    use_cython = False
else:
    use_cython = True

cmdclass = {}
ext_modules = []

if use_cython:
    ext_modules += [
        Extension("polo.polo", [ "polo/polo.pyx" ], include_dirs=[numpy.get_include()]),
    ]
    cmdclass.update({ 'build_ext': build_ext })
else:
    ext_modules += [
        Extension("polo.polo", [ "polo/polo.c" ], include_dirs=[numpy.get_include()]),
    ]

setup(
    name = "polo",
    packages = ['polo'],
    version = '0.4',
    description = 'Optimal Linear Ordering of Hierarchical Trees',
    author = 'Adrian Veres',
    author_email = 'adrianveres@gmail.com',
    url = 'https://github.com/adrianveres/polo',
    download_url = 'https://github.com/adrianveres/polo/tarball/0.1',
    keywords = ['hierarchical', 'clustering', 'linear ordering', 'leaves'], 
    cmdclass = cmdclass,
    ext_modules=ext_modules,
    classifiers = [],
    install_requires=['numpy', 'scipy'],
    package_data={'polo': ['data/*']},
    )





class sdist(_sdist):
    def run(self):
        # Make sure the compiled Cython files in the distribution are up-to-date
        from Cython.Build import cythonize
        cythonize(['polo.pyx'], include_dirs=[numpy.get_include()])
        _sdist.run(self)
cmdclass['sdist'] = sdist