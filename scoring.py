import os
import subprocess
import re
import multiprocessing

input_extension = '.inp'
output_extension = '.out'
exec_file = 'out'


def compare(output, answer):
    outputs = re.split('\s+', output.strip())
    answers = re.split('\s+', answer.strip())
    return outputs == answers


class Scoring:
    def __init__(self, file, testcase, timeout):
        self.testcases = []
        self.file = file
        self.testcase = testcase
        self.timeout = timeout

    def grade(self):
        self.validate_testcase_folder()
        self.get_list_testcase()

        total_tests = len(self.testcases)
        passed_tests = 0
        wrong_tests = -1
        message = ''

        try:
            self.validate_file()

            self.compile()
            for testcase in self.testcases:
                input_content, answer = self.get_testcase(testcase)
                output_content = self.execute(input_content)
                if compare(output_content, answer):
                    passed_tests += 1
                else:
                    wrong_tests = int(testcase)
        except BaseException as e:
            message = str(e)
        finally:
            if os.path.exists("{file}".format(file=exec_file)):
                os.remove("{file}".format(file=exec_file))
            return passed_tests, total_tests, wrong_tests, message

    def validate_file(self):
        if not os.path.isfile(self.file):
            raise Exception('File not exist')

    def validate_testcase_folder(self):
        if not os.path.isdir(self.testcase):
            raise Exception('Testcase not exist')

    def get_list_testcase(self):
        list_file = list(filter(lambda entry: os.path.isfile(os.path.join(self.testcase, entry)),
                                os.listdir(self.testcase)))

        prefix_list = set(map(lambda entry: os.path.splitext(entry)[0], list_file))

        list_testcase = list(
            filter(lambda prefix: prefix + input_extension in list_file and prefix + output_extension in list_file,
                   prefix_list))
        list_testcase.sort()
        self.testcases = list_testcasgit
    def compile(self):
        command = "g++ -O2 -o ./out {file}".format(file=self.file)
        result = subprocess.run(command, shell=True, stderr=subprocess.PIPE)
        if result.returncode != 0:
            raise Exception('Error when compile: {error}'.format(error=result.stderr))

    def get_testcase(self, testcase):
        input_file = open(os.path.join(self.testcase, testcase + input_extension))
        output_file = open(os.path.join(self.testcase, testcase + output_extension))

        input_content = input_file.read()
        output_content = output_file.read()

        input_file.close()
        output_file.close()
        return input_content, output_content

    def execute(self, input_content):
        command = "./{exec_file}".format(exec_file=exec_file)

        p = subprocess.Popen(command, stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, )

        stdout, stderr = p.communicate(input=input_content.encode())

        if p.wait(self.timeout) != 0:
            raise Exception('Error when run: {error}'.format(error=stderr))
        return stdout.decode()
