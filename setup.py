"""!
@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""


import os
import pyclustering

from setuptools import setup
from setuptools import find_packages
from setuptools.command.test import test as command


def load_readme():
    readme_file = 'PKG-INFO.rst'
    if os.path.isfile(readme_file):
        with open(readme_file) as file_descr:
            return file_descr.read()

    return "pyclustering is a python data mining library (cluster-analysis, graph coloring, oscillatory networks)"


class setup_tests_runner(command):
    def run_tests(self):
        from pyclustering.tests.tests_runner import tests_runner
        tests_runner.run()


setup(
      name='pyclustering',
      packages=find_packages(),
      version=pyclustering.__version__,
      description='pyclustring is a python data mining library',
      long_description=load_readme(),
      url='https://github.com/annoviko/pyclustering',
      project_urls={
                     'Homepage': 'https://pyclustering.github.io/',
                     'Repository': 'https://github.com/annoviko/pyclustering',
                     'Documentation': 'https://pyclustering.github.io/docs/0.10.1/html/index.html',
                     'Bug Tracker': 'https://github.com/annoviko/pyclustering/issues'
                   },
      license='BSD-3-Clause',
      classifiers=[
                     'Development Status :: 5 - Production/Stable',
                     'Intended Audience :: Developers',
                     'Intended Audience :: Education',
                     'Intended Audience :: Information Technology',
                     'Intended Audience :: Science/Research',
                     'License :: OSI Approved :: BSD License',
                     'Natural Language :: English',
                     'Operating System :: Microsoft',
                     'Operating System :: Microsoft :: Windows',
                     'Operating System :: POSIX :: Linux',
                     'Operating System :: Unix',
                     'Operating System :: iOS',
                     'Programming Language :: C',
                     'Programming Language :: C++',
                     'Programming Language :: Python :: 3',
                     'Topic :: Education',
                     'Topic :: Scientific/Engineering :: Artificial Intelligence',
                     'Topic :: Scientific/Engineering :: Bio-Informatics',
                     'Topic :: Scientific/Engineering :: Information Analysis',
                     'Topic :: Scientific/Engineering :: Visualization',
                     'Topic :: Software Development :: Libraries'
                  ],
      keywords='pyclustering data-mining clustering cluster-analysis machine-learning neural-network oscillatory-network',
      author='Andrei Novikov',
      author_email='pyclustering@yandex.ru',

      install_requires=['scipy>=1.1.0', 'matplotlib>=3.0.0', 'numpy>=1.15.2', 'Pillow>=5.2.0'],
      python_requires='>=3.6',
      package_data={
                      'pyclustering.samples': ['samples/famous/*.*',
                                               'samples/fcps/*.*',
                                               'samples/simple/*.*',
                                               'graphs/*.*',
                                               'images/*.*',
                                               'images/digits/*.*'],
                      'pyclustering.core': ['64-bit/linux/libpyclustering.so', '32-bit/linux/libpyclustering.so',
                                            '64-bit/win/pyclustering.dll', '32-bit/win/pyclustering.dll',
                                            '64-bit/macos/libpyclustering.so'],
                   },

      data_files=[('', ['LICENSE', 'CHANGES', 'README.rst', 'PKG-INFO.rst'])],

      cmdclass={'test': setup_tests_runner}
    )
