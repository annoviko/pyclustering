"""!

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2016
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

import os;

from distutils.command.install import install;

from setuptools import setup;
from setuptools import find_packages;

from subprocess import call;

from sys import platform as _platform;


class ccore_install(install):
    def run(self):
        print("[CCORE BUILD] Current platform:", _platform);
        if (_platform == "linux") or (_platform == "linux2"):
            print("[CCORE BUILD] CCORE library should be built for", _platform);
            
            def make_ccore_library():
                call('cd ccore/ && make ccore && cd -', shell = True);
            
            self.execute(make_ccore_library, [], 'Build CCORE library...');

        install.run(self);


def full_setup():
    setup(
          name = 'pyclustering',
          version = '0.6.dev1',
          description = 'pyclustring is a python data mining library',
          url = 'https://github.com/annoviko/pyclustering',
          license = 'GNU Public License',
          classifiers = [
                         'Development Status :: 3 - Alpha',
                         'Intended Audience :: Developers',
                         'License :: GNU Public License',
                         'Programming Language :: Python :: 3.4',
                         'Programming Language :: C++'
                         ],
          keywords = 'pyclustering data mining cluster analysis neural oscillatory networks',
          author = 'Andrei Novikov',
          author_email = 'pyclustering@yandex.ru',
          packages = find_packages(),
          package_data = {
                            'pyclustering.samples': ['samples/*.txt', 'graphs/*.grpr', 'images/*.png', 'images/digits/*.png'],
                            'pyclustering.core': ['x64/linux/ccore.so', 'x64/win/ccore.dll'],
                          },
          
          cmdclass = { 'install': ccore_install }
        );


full_setup();

