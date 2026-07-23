"""
This is the python script for question 2. In this script, you are required to implement a multi agent path-finding algorithm
"""

from lib_piglet.utils.tools import eprint
import glob, os, sys


# import necessary modules that this python scripts need.
try:
    from flatland.core.transition_map import GridTransitionMap
    from flatland.utils.controller import (
        get_action,
        Train_Actions,
        Directions,
        check_conflict,
        path_controller,
        evaluator,
        remote_evaluator,
        VisualiserOptions,
    )
except Exception as e:
    eprint("Cannot load flatland modules!", e)
    exit(1)

#########################
# Debugger and visualiser options
#########################

# Set debug to True for a step-by-step account of the run: what was planned,
# which agents malfunctioned or were blocked, and why each episode ended.
debug = False

# Controls the visualiser:
#   False                  -> run headless (fastest)
#   True                   -> watch the run with the default settings
#   VisualiserOptions(...) -> watch the run with your own settings, e.g.
#       VisualiserOptions(
#           delay=0.3,      # seconds to pause between timesteps; 0 runs at full speed
#           headless=False, # True: no window, serve to your browser instead
#           wait=True,      # hold the first frame until you are watching
#           port=8080,      # serve on a fixed port (headless mode)
#           cell_size=40,   # pixels per grid cell
#       )
visualizer = False

# Stop each episode after this many timesteps. None uses the test case's own
# limit.
max_steps = None

# If you want to test on specific instance, turn test_single_instance to True and specify the level and test number
test_single_instance = False
level = 0
test = 0

#########################
# Reimplementing the content in get_path() function.
#
# Return a list of (x,y) location tuples which connect the start and goal locations.
# The path should avoid conflicts with existing paths.
#########################


# This function return a list of location tuple as the solution.
# @param start A tuple of (x,y) coordinates
# @param start_direction An Int indicate direction.
# @param goal A tuple of (x,y) coordinates
# @param rail The flatland railway GridTransitionMap
# @param agent_id The id of given agent
# @param existing_paths A list of lists of locations indicate existing paths. The index of each location is the time that
# @param max_timestep The max timestep of this episode.
# @return path A list of (x,y) tuple.
def get_path(
    start: tuple,
    start_direction: int,
    goal: tuple,
    rail: GridTransitionMap,
    agent_id: int,
    existing_paths: list,
    max_timestep: int,
):
    ############
    # Below is an dummy path finding implementation,
    # which always choose the first available transition of current state.
    #
    # Replace these with your implementation and return a list of (x,y) tuple as your plan.
    # Your plan should avoid conflicts with paths in existing_paths.
    ############

    # initialize path list
    path = []
    loc = start
    direction = start_direction

    for t in range(0, int(max_timestep / 10)):
        # add loc to path list
        path.append(loc)
        if loc == goal:
            break

        # get available transitions from Rail_Env object.
        valid_transitions = rail.get_transitions(loc[0], loc[1], direction)
        for i in range(0, len(valid_transitions)):
            if valid_transitions[i]:
                new_x = loc[0]
                new_y = loc[1]
                action = i
                if action == Directions.NORTH:
                    new_x -= 1
                elif action == Directions.EAST:
                    new_y += 1
                elif action == Directions.SOUTH:
                    new_x += 1
                elif action == Directions.WEST:
                    new_y -= 1

                conflict = False
                for p in existing_paths:
                    if t + 1 < len(p) and p[t + 1] == (new_x, new_y):
                        conflict = True
                    if (
                        t + 1 < len(p)
                        and p[t + 1] == (loc[0], loc[1])
                        and p[t] == (new_x, new_y)
                    ):
                        conflict = True
                if conflict:
                    continue

                loc = (new_x, new_y)
                direction = action
                break
    return path


#########################
# You should not modify codes below, unless you want to modify test_cases to test specific instance. You can read it know how we ran flatland environment.
########################
if __name__ == "__main__":
    if len(sys.argv) > 1:
        remote_evaluator(get_path, sys.argv)
    else:
        script_path = os.path.dirname(os.path.abspath(__file__))
        test_cases = glob.glob(
            os.path.join(script_path, "multi_test_case/level*_test_*.pkl")
        )
        if test_single_instance:
            test_cases = glob.glob(
                os.path.join(
                    script_path,
                    "multi_test_case/level{}_test_{}.pkl".format(level, test),
                )
            )
        test_cases.sort()
        evaluator(
            get_path,
            test_cases,
            debug=debug,
            visualizer=visualizer,
            question_type=2,
            max_steps=max_steps,
        )
