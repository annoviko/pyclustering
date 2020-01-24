import enum
import sys

from pyclustering.tests.tests_runner import pyclustering_tests, pyclustering_integration_tests, pyclustering_unit_tests


class exit_code(enum.IntEnum):
    success = 0,
    error_unknown_type_test = -1,
    error_too_many_arguments = -2,
    error_failure = -3


if __name__ == "__main__":
    result = None
    exit_code = exit_code.success

    if len(sys.argv) == 1:
        result = pyclustering_tests().run()

    elif len(sys.argv) == 2:
        if sys.argv[1] == "--integration":
            result = pyclustering_integration_tests().run()

        elif sys.argv[1] == "--unit":
            result = pyclustering_unit_tests().run()

        else:
            print("Unknown type of test is specified '" + str(sys.argv[1]) + "'.")
            exit_code = exit_code.error_unknown_type_test

    else:
        print("Too many arguments '" + str(len(sys.argv)) + "' is used.")
        exit_code = exit_code.error_too_many_arguments

    # Get execution result
    if result is not None:
        if result.wasSuccessful() is False:
            exit_code = exit_code.error_failure

    exit(exit_code)
