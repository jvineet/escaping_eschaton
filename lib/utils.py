import sys
import os
import json
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

def load_json_chart(chartfile):
    """
        Inputs:
            chartfile: contains the initial state and propogation information 
            for the event including blast velocity, asteroid velocity and 
            asteroid location at t=0.

        Returns:
            asteroids:
            blast_time_step:
    """
    with open(chartfile) as json_data:
        state = json.load(json_data)

    blast_time_step = state["t_per_blast_move"]
    if not isinstance(blast_time_step, int):
        ValueError('Blast time step must be an Integer')

    asteroids = state["asteroids"]
    for i, asteroid in enumerate(asteroids, 1):
        check_asteroid(asteroid, i)
    return blast_time_step, asteroids


def check_asteroid(asteroid, ind):
    """
    """
    cycle_time = asteroid.get('t_per_asteroid_cycle')
    offset = asteroid.get('offset')
    if not cycle_time or not isinstance(cycle_time, int):
        buf = "Asteroid Cycle Time must be present and has an integer value > 0 for asteroid at p={0}"
        raise ValueError(buf.format(ind))
    if offset is None or not isinstance(offset, int):
        buf = "Asteroid Cycle Offset must be present for and have an integer value at p={0}"
        raise ValueError(buf.format(ind))


def death_by_blast(blast_time_step, t, p):
    """
    """
    if not blast_time_step:
        return False
    if t // blast_time_step - 1 >= p:
        return True
    return False


def death_by_asteroid(asteroid, t):
    """
    """
    cycle_time = asteroid['t_per_asteroid_cycle']
    offset = asteroid['offset']
    if (t + offset) % cycle_time == 0:
        return True
    return False


def get_nxt_state(state, blast_time_step, asteroids):
    """
    """
    acc = [-1, 0 ,1]
    p, v, t = state

    for next_a in acc:
        next_v = v + next_a
        next_p = p + next_v
        next_t = t + 1

        # deth by collison into eschaton
        if next_p < 0:
            continue

        if death_by_blast(blast_time_step, next_t, next_p):
            continue
        
        if 0 < next_p <= len(asteroids) and death_by_asteroid(asteroids[next_p - 1], next_t):
            continue

        yield next_a, (next_p, next_v, next_t)        




