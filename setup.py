"""!
@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2019
@copyright GNU Public License
@cond GNU_PUBLIC_LICENSE
    PyClustering is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    PyClustering is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
@endcond

"""


import os

from setuptools import setup
from setuptools import find_packages


def load_readme():
    readme_file = 'PKG-INFO.rst'
    if os.path.isfile(readme_file):
        with open(readme_file) as file_descr:
            return file_descr.read()

    return "pyclustering is a python data mining library (clustering, oscillatory networks, neural networks)"


setup(
      name='pyclustering',
      packages=find_packages(),
      version='0.9.0',
      description='pyclustring is a python data mining library',
      long_description=load_readme(),
      url='https://github.com/annoviko/pyclustering',
      project_urls={
                     'Homepage': 'https://pyclustering.github.io/',
                     'Repository': 'https://github.com/annoviko/pyclustering',
                     'Documentation': 'https://pyclustering.github.io/docs/0.9.0/html/',
                     'Bug Tracker': 'https://github.com/annoviko/pyclustering/issues'
                   },
      license='GNU Public License',
      classifiers=[
                     'Development Status :: 5 - Production/Stable',
                     'Intended Audience :: Developers',
                     'Intended Audience :: Education',
                     'Intended Audience :: Information Technology',
                     'Intended Audience :: Science/Research',
                     'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                     'Natural Language :: English',
                     'Operating System :: Microsoft',
                     'Operating System :: POSIX :: Linux',
                     'Operating System :: Unix',
                     'Operating System :: MacOS',
                     'Programming Language :: C',
                     'Programming Language :: C++',
                     'Programming Language :: Python :: 3',
                     'Topic :: Education',
                     'Topic :: Scientific/Engineering :: Artificial Intelligence',
                     'Topic :: Scientific/Engineering :: Bio-Informatics',
                     'Topic :: Scientific/Engineering :: Image Recognition',
                     'Topic :: Scientific/Engineering :: Information Analysis',
                     'Topic :: Scientific/Engineering :: Visualization'
                  ],
      keywords='pyclustering data-mining clustering cluster-analysis machine-learning neural-network oscillatory-network',
      author='Andrei Novikov',
      author_email='pyclustering@yandex.ru',

      install_requires=['scipy', 'matplotlib', 'numpy', 'Pillow'],
      python_requires='>=3.5',
      package_data={
                      'pyclustering.samples': ['samples/famous/*.data', 'samples/famous/*.answer', 'samples/fcps/*.data', 'samples/fcps/*.answer', 'samples/simple/*.data', 'samples/simple/*.answer', 'graphs/*.grpr', 'images/*.png', 'images/digits/*.png'],
                      'pyclustering.core': ['x64/linux/ccore.so', 'x86/linux/ccore.so',
                                            'x64/win/ccore.dll', 'x86/win/ccore.dll',
                                            'x64/macos/ccore.so'],
                   },

      data_files=[('', ['LICENSE', 'CHANGES', 'README.rst', 'PKG-INFO.rst'])],
    )
