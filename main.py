#
from scoring import Scoring
import argparse
import json

def grade(file, test):
    scoring = Scoring(file, test, 1)
    passed_tests, total_tests, wrong_tests, message = scoring.grade()
    print(json.dumps({
        "passed_tests": passed_tests,
        "total_tests": total_tests,
        "wrong_tests": wrong_tests,
        "message": message
    }))


def grade_test():
    basedir = 'submission/'
    file = basedir + 'source.cpp'
    testcase = basedir + 'testcase/'
    print(grade(file, testcase))


if __name__ == '__main__':
    # grade_test()
    parser = argparse.ArgumentParser(description="Grading service")

    parser.add_argument("--file", help="Submission file")
    parser.add_argument("--testcase", help="Testcase folder")
    parser.add_argument("--timeout", help="Timeout")

    args = parser.parse_args()

    file = args.file
    test_folder = args.testcase
    grade(file, test_folder)
