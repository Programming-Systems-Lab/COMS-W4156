#!/usr/bin/python

import csv
import sys
import urllib2

def query_assignment(url, expected, port=9000):
    '''
    Queries the service at the given url and compares the response to the
    expected parameter.
    '''
    base_url = 'http://localhost:' + str(port) + url
    ret_val = urllib2.urlopen(base_url).read()
    return (ret_val == expected, ret_val, expected)

if len(sys.argv) != 2:
    err_msg = 'Expected: ./assignment_test.py <input file>.'
    print err_msg
    sys.exit(1)

total_tests = 0
total_correct = 0
with open(sys.argv[1]) as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        total_tests += 1
        is_correct, actual, expected = query_assignment(row[0], row[1])
        if is_correct:
            total_correct += 1
        else:
            print 'TEST FAIL: %s != %s' % (actual, expected)
print 'Final Grade: %f' % (float(total_correct) / total_tests)
