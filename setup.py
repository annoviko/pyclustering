"""!
@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2018
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
      name = 'pyclustering',
      packages = find_packages(),
      version = '0.8.1',
      description = 'pyclustring is a python data mining library',
      long_description = load_readme(),
      url = 'https://github.com/annoviko/pyclustering',
      license = 'GNU Public License',
      classifiers = [
                     'Development Status :: 5 - Production/Stable',
                     'Intended Audience :: Developers',
                     'Intended Audience :: Education',
                     'Intended Audience :: Information Technology',
                     'Intended Audience :: Science/Research',
                     'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                     'Natural Language :: English',
                     'Operating System :: Microsoft :: Windows :: Windows 7',
                     'Operating System :: Microsoft :: Windows :: Windows 8',
                     'Operating System :: Microsoft :: Windows :: Windows 10',
                     'Operating System :: POSIX :: Linux',
                     'Operating System :: Unix',
                     'Programming Language :: C',
                     'Programming Language :: C++',
                     'Programming Language :: Python :: 3.4',
                     'Programming Language :: Python :: 3.5',
                     'Programming Language :: Python :: 3.6',
                     'Programming Language :: Python :: 3.7',
                     'Topic :: Education',
                     'Topic :: Scientific/Engineering :: Artificial Intelligence',
                     'Topic :: Scientific/Engineering :: Bio-Informatics',
                     'Topic :: Scientific/Engineering :: Image Recognition',
                     'Topic :: Scientific/Engineering :: Information Analysis',
                     'Topic :: Scientific/Engineering :: Visualization'
                     ],
      keywords = 'pyclustering data-mining clustering cluster-analysis neural-network oscillatory-network',
      author = 'Andrei Novikov',
      author_email = 'pyclustering@yandex.ru',
      
      package_data = {
                      'pyclustering.samples': ['samples/famous/*.data', 'samples/fcps/*.data', 'samples/simple/*.data', 'graphs/*.grpr', 'images/*.png', 'images/digits/*.png'],
                      'pyclustering.core': [ 'x64/linux/ccore.so', 'x86/linux/ccore.so',
                                             'x64/win/ccore.dll', 'x86/win/ccore.dll' ],
                     },

      data_files = [ ('', ['LICENSE', 'CHANGES', 'README.rst', 'PKG-INFO.rst']) ],
    )
