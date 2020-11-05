import argparse
import enum
import logging
import os.path
import re
import signal
import subprocess


class EExitCode(enum.IntEnum):
    success = 0,
    executable_not_found = -1
    failure_tests_not_found = -2


class Runner:
    def __init__(self, executable, attempts=1):
        self.__executable = executable
        self.__attempts = attempts
        self.__exit_code = EExitCode.success

    def run(self):
        if os.path.isfile(self.__executable):
            result = subprocess.run(self.__executable, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

            output = result.stdout.decode('utf-8')
            print(output)

            exit_code = result.returncode
            if exit_code == EExitCode.success:
                exit(exit_code)
            elif exit_code == -signal.SIGSEGV:
                logging.error("Segmentation fault signal is received during unit-testing process.")
                exit(exit_code)

            for _ in range(self.__attempts):
                exit_code, output = self.__rerun(output)
                if exit_code == EExitCode.success:
                    exit(exit_code)
                elif exit_code == EExitCode.failure_tests_not_found:
                    logging.error("There is nothing to rerun - failure tests are not found despite failure code '"
                                  + str(result.returncode) + "'.")
                    exit(exit_code)
        else:
            logging.error("Impossible to find executable file '%s'." % self.__executable)
            exit(EExitCode.executable_not_found)

    def __rerun(self, output):
        failures = Runner.__get_failures(output)
        if len(failures) == 0:
            return EExitCode.failure_tests_not_found, None

        logging.info("Rerun failed tests: '%s'" % failures)

        argument = "--gtest_filter="
        for fail in failures:
            argument += ":" + fail

        result = subprocess.run([self.__executable, argument], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = result.stdout.decode('utf-8')
        print(output)

        return result.returncode, output

    @staticmethod
    def __get_failures(output):
        failures = set()

        lines = output.splitlines()
        expression_failure = re.compile("\[\s+FAILED\s+\] (\S+)\.(\S+)")
        for line in lines:
            result = expression_failure.match(line)
            if result is not None:
                suite = result.group(1)
                test = result.group(2)
                failures.add("%s.%s" % (suite, test))

        return failures


parser = argparse.ArgumentParser()
parser.add_argument('-e', '--executable', required=True, type=str, help='Execution object to run.')
arguments = parser.parse_args()

executable = arguments.executable

logging.basicConfig(level=logging.INFO)
Runner("./" + arguments.executable).run()
