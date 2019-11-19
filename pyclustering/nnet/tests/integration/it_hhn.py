"""!

@brief Integration-tests for Hodgkin-Huxley oscillatory network.

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


import unittest

from pyclustering.nnet.tests.hhn_templates import HhnTestTemplates

from pyclustering.core.tests import remove_library


class HhnIntegrationTest(unittest.TestCase):
    def testGlobalSyncWithSameStimulus(self):
        HhnTestTemplates.templateSyncEnsembleAllocation([27, 27, 27], None, 600, 50, [[0, 1, 2]], True);

    def testGlobalSyncWithVariousStimulus(self):
        HhnTestTemplates.templateSyncEnsembleAllocation([26, 26, 27, 27, 26, 25], None, 600, 50, [[0, 1, 2, 3, 4, 5]], True);

    def testPartialSync(self):
        HhnTestTemplates.templateSyncEnsembleAllocation([25, 25, 50, 50], None, 800, 200, [[0, 1], [2, 3]], True);

    def testThreeEnsembles(self):
        HhnTestTemplates.templateSyncEnsembleAllocation([0, 0, 25, 25, 47, 47], None, 2400, 600, [[0, 1], [2, 3], [4, 5]], True);

    @remove_library
    def testProcessingWhenLibraryCoreCorrupted(self):
        HhnTestTemplates.templateSyncEnsembleAllocation([27, 27, 27], None, 600, 50, [[0, 1, 2]], True);
