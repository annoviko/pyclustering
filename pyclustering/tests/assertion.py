"""!

@brief Assert that are used for testing

@authors Andrei Novikov (pyclustering@yandex.ru)
@date 2014-2020
@copyright BSD-3-Clause

"""

import numpy


class assertion:
    @staticmethod
    def eq(argument1, argument2):
        if isinstance(argument1, numpy.ndarray) or isinstance(argument2, numpy.ndarray):
            if not (argument1 == argument2).all():
                raise AssertionError("Expected: '" + str(argument1) + "', Actual: '" + str(argument2) + "'")

        elif not (argument1 == argument2):
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
    def false(argument1, **kwargs):
        message = kwargs.get('message', None)

        error_message = "Expected: 'False', Actual: '%s'" % str(argument1)
        if message:
            error_message = "%s, Info: '%s'" % (error_message, message)

        if argument1:
            raise AssertionError(error_message)

    @staticmethod
    def fail(message=None):
        if message is None:
            raise AssertionError("Failure")
        else:
            raise AssertionError("Failure: '" + message + "'")

    @staticmethod
    def exception(expected_exception, callable_object, *args, **kwargs):
        try:
            callable_object(*args, **kwargs)
        except expected_exception:
            return
        except Exception as actual_exception:
            raise AssertionError("Expected: '%s', Actual: '%s'" %
                                 (expected_exception.__name__, actual_exception.__class__.__name__))

        raise AssertionError("Expected: '%s', Actual: 'None'" % expected_exception.__name__)
