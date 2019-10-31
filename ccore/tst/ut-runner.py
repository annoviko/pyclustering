import enum
import logging
import os.path
import re
import subprocess


class EExitCode(enum.IntEnum):
    success = 0,
    executable_not_found = -1


class Runner:
    def __init__(self, executable, attempts=1):
        self.__executable = executable
        self.__attempts = attempts
        self.__exit_code = EExitCode.success

    def run(self):
        if os.path.isfile(self.__executable):
            result = subprocess.run(self.__executable, stdout=subprocess.PIPE)
            output = result.stdout.decode('utf-8')
            print(output)

            exit_code = result.returncode
            for _ in range(self.__attempts):
                exit_code, output = self.__rerun(output)
                if exit_code == EExitCode.success:
                    break
        else:
            logging.error("Impossible to find executable file '%s'." % self.__executable)
            exit_code = EExitCode.executable_not_found

        exit(exit_code)

    def __rerun(self, output):
        failures = Runner.__get_failures(output)
        logging.info("Rerun failed tests: '%s'" % failures)

        argument = "--gtest_filter="
        for fail in failures:
            argument += ":" + fail

        result = subprocess.run([self.__executable, argument], stdout=subprocess.PIPE)
        output = result.stdout.decode('utf-8')
        print(output)

        return result.returncode, output

    @staticmethod
    def __get_failures(output):
        failures = set()

        lines = output.splitlines()
        expression = re.compile("\[\s+FAILED\s+\] (\S+)\.(\S+)")
        for line in lines:
            result = expression.match(line)
            if result is None:
                continue

            suite = result.group(1)
            test = result.group(2)
            failures.add("%s.%s" % (suite, test))

        return failures


logging.basicConfig(level=logging.INFO)
Runner("./utcore.exe").run()
