"""!

@brief Assert that are used for testing

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


class assertion:
    @staticmethod
    def eq(argument1, argument2):
        if not (argument1 == argument2):
            raise AssertionError("Expected: '" + str(argument1) + "', Actual: '" + str(argument2) + "'")


    @staticmethod
    def eq_float(argument1, argument2, eps):
        if abs(argument1 - argument2) >= eps:
            raise AssertionError("Expected: '" + str(argument1) + "', Actual: '" + str(argument2) +
                                 "' (eps: '" + str(eps) + "')")


    @staticmethod
    def gt(argument1, argument2):
        if not (argument1 > argument2):
            raise AssertionError("Expected: '" + str(argument1) + "' > '" + str(argument2) +
                                 "', Actual: '" + str(argument1) + "' vs '" + str(argument2) + "'")

    @staticmethod
    def ge(argument1, argument2):
        if not (argument1 >= argument2):
            raise AssertionError("Expected: '" + str(argument1) + "' >= '" + str(argument2) +
                                 "', Actual: '" + str(argument1) + "' vs '" + str(argument2) + "'")

    @staticmethod
    def lt(argument1, argument2):
        if not (argument1 < argument2):
            raise AssertionError("Expected: '" + str(argument1) + "' < '" + str(argument2) +
                                 "', Actual: '" + str(argument1) + "' vs '" + str(argument2) + "'")

    @staticmethod
    def le(argument1, argument2):
        if not (argument1 <= argument2):
            raise AssertionError("Expected: '" + str(argument1) + "' <= '" + str(argument2) +
                                 "', Actual: '" + str(argument1) + "' vs '" + str(argument2) + "'")

    @staticmethod
    def true(argument1, **kwargs):
        message = kwargs.get('message', None)

        error_message = "Expected: 'True', Actual: '%s'" % str(argument1)
        if message:
            error_message = "%s, Info: '%s'" % (error_message, message)

        if not argument1:
            raise AssertionError(error_message)

    @staticmethod
    def false(argument1):
        if argument1:
            raise AssertionError("Expected: 'False', Actual: '" + str(argument1) + "'")
