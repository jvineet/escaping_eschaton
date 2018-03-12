import sys
import os
import logging
import argparse
from lib import utils

CURVERSION = "0.1"
SRCPATH = os.path.dirname(os.path.realpath(__file__))

def usage():
    buf = '''
    Computes an optimal route to escape Eschaton by flying through 
    the gaps in the asteroids and exiting the asteroid belt.

    Run:
        $ python<3.x> escapeing_eschaton.py <chart.json> [optional args]
        '''
    return buf


def solve(args):
    """
        state (p,v,t)
    """
    blast_time_step, asteroids = utils.load_json_chart(args.chart)

    state_stack = []
    course_sofar = []
    exhausted_states = set([])
    initial_state = (0,0,0)
    state_stack.append((None, False, initial_state))    
    best_course = None

    while state_stack != []:
        curr_a, exhausted, curr_state = state_stack.pop()
        if exhausted:
            exhausted_states.add(curr_state)
            course_sofar.pop()
            continue
        
        if curr_state in exhausted_states:
            continue

        if best_course and len(course_sofar) >= len(best_course):
            continue

        course_sofar.append(curr_a)

        if curr_state[0] > len(asteroids):
            # print(len(course_sofar))
            if not best_course or len(course_sofar) < len(best_course):
                best_course = course_sofar.copy()
            course_sofar.pop()
            continue
        
        state_stack.append((curr_a, True, curr_state))

        for next_a, next_state in utils.get_nxt_state(curr_state, blast_time_step, asteroids):
            state_stack.append((next_a, False, next_state))

    return best_course[1:]

    
def main(argstr=None):
    parser = argparse.ArgumentParser(description='Input Parameters', usage=usage())
    parser.add_argument('chart', help="json file containing state chart for blast velocity and asteroids around Eschaton")
    parser.add_argument("-c", "--config", dest="config", default="", nargs="?",\
        help="configuration file genotype")
    parser.add_argument("-l", "--log", dest="log", default="escapeing_eschaton", nargs="?", \
        help="log to file (Default: escapeing_eschaton.log)")
    parser.add_argument("-v", "--version", action="version", version="Escapeing Eschaton Current version {0}".format(CURVERSION))

    if argstr:
        args = parser.parse_args(argstr)
    else:
        args = parser.parse_args()
        
    return solve(args)


if __name__ == '__main__':
    print(main())