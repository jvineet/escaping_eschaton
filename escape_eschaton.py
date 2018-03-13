import sys
import os
import logging
import argparse
import shutil
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
        pv_state (p,v)
    """
    blast_time_step, asteroids = utils.load_json_chart(args.chart)

    state_stack = []
    course_sofar = []
    exhausted_states = {}
    initial_state = (0,0,0)
    state_stack.append((None, False, initial_state))    
    best_course = []

    # perform an iterative DFS on the state space to find the optimal solution
    while state_stack != []:
        curr_a, exhausted, curr_state = state_stack.pop()
        pv_state = curr_state[:-1]
        curr_t = curr_state[-1]

        # store exhausted state to prune and backtrack on the search space later
        if exhausted:
            exhausted_states[pv_state] = curr_t
            course_sofar.pop()
            continue
        
        # backtrack if current pv_state was already exhausted at time less than 
        # or equal to the current time
        if pv_state in exhausted_states and exhausted_states[pv_state] <= curr_t:
            continue
        
        # backtrack if current solution is already longer than best solution so far
        if best_course and len(course_sofar) >= len(best_course):
            continue

        course_sofar.append(curr_a)

        # escape condition
        if curr_state[0] > len(asteroids):
            # if current course is shorter than best course so far, make it best course
            if not best_course or len(course_sofar) < len(best_course):
                best_course = course_sofar.copy()
            course_sofar.pop()
            continue
        
        # add state back to stack with exhaused flag True. When it is popped again, 
        # we will know all states downstream from here were exhausted
        state_stack.append((curr_a, True, curr_state))

        # add all valid downstream states from here (continue DFS)
        for next_a, next_state in utils.get_nxt_states(curr_state, blast_time_step, asteroids):
            state_stack.append((next_a, False, next_state))

    return best_course[1:]

def setup(args):
    """
        Staging area that sets out output folder and logging infoormation
        and then class the 'solve' routine
        Input: Object with Input arguements
        Returns: None
    """
    output_folder = args.output_folder

    if os.path.exists(output_folder) and args.xforce:
        shutil.rmtree(output_folder)
        os.makedirs(output_folder)
    elif not os.path.exists(output_folder):
        os.makedirs(output_folder)
    else:
        print("Output Path already exists.") 
        print("Please use the -x option to overwrite existing path")
        exit(0)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)
    logger.addHandler(console)

    filelog_path = os.path.join(output_folder, args.log)
    filelog = logging.FileHandler(filelog_path, mode="w")
    filelog.setFormatter(formatter)
    logger.addHandler(filelog)

    logger.info('Logging enabled')
    logger.info('Created Output Folder: {}'.format(args.output_folder))
    res = solve(args)
    print(res)

    
def main(argstr=None):
    parser = argparse.ArgumentParser(description='Input Parameters', usage=usage())
    parser.add_argument('chart', help="json file containing state chart for blast velocity and asteroids around Eschaton")
    parser.add_argument("-c", "--config", dest="config", default="", nargs="?",\
        help="configuration file genotype")
    parser.add_argument("-o", "--output-folder", dest="output_folder", default='escape_result',
        help="Output folder for results json and logs")
    parser.add_argument("-x", "--xforce", dest="xforce", action="store_true", \
        help="force overwrite the output, if the folder already exists")
    parser.add_argument("-l", "--log", dest="log", default="escapeing_eschaton.log", nargs="?", \
        help="log to file (Default: escapeing_eschaton.log)")
    parser.add_argument("-v", "--version", action="version", version="Escapeing Eschaton Current version {0}".format(CURVERSION))

    if argstr:
        args = parser.parse_args(argstr)
    else:
        args = parser.parse_args()
        
    return setup(args)


if __name__ == '__main__':
    main()