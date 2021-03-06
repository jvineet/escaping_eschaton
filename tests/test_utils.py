import unittest
import logging
from unittest.mock import patch
import os
import sys

SRCPATH = os.path.dirname(os.path.abspath(__file__))+'/..'
sys.path.append(SRCPATH)

from lib import utils

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class SetupBasicTests(unittest.TestCase):
    """
        Sets up unit tests for basic helper routines inside lib
    """

    @classmethod
    def setUpClass(cls):
        cls.console = logging.StreamHandler()
        cls.console.setLevel(logging.INFO)    
        logger.addHandler(cls.console)

        logger.info('Running unit tests for utils ..')
        cls.json_chart = os.path.join(SRCPATH, 'tests', 'inputs', 'chart_test1.json')


    def test_load_json_chart(self):
        """
            Testing the json chart loading routine
        """
        blast_velocity, asteroids = utils.load_json_chart(SetupBasicTests.json_chart)
        self.assertEqual(blast_velocity, 10)
        self.assertEqual(len(asteroids), 4)
        self.assertEqual(asteroids[2]["offset"], 3)
        self.assertEqual(asteroids[2]["t_per_asteroid_cycle"], 4)


    def test_death_by_blast(self):
        """
            Testing the death_by_blast function 
        """
        self.assertFalse(utils.death_by_blast(10, 9, 0), 
            "position consumed by blast a second before it should")
        self.assertTrue(utils.death_by_blast(10, 10, 0),
            "position not consumed by blast when it should")
        self.assertFalse(utils.death_by_blast(10, 19, 1),
             "position consumed by blast a second before it should")
        self.assertTrue(utils.death_by_blast(10, 20, 1),
            "position not consumed by blast when it should")
        self.assertFalse(utils.death_by_blast(1, 0, 0), 
            "p=0 not safe at t=0 at max blast velocity")
        self.assertTrue(utils.death_by_blast(1, 1, 0),
            "p=0 not consumed by blast at t=1 at max blast velocity")
        
        with self.assertRaises(ZeroDivisionError):
            self.assertFalse(utils.death_by_blast(0, 10000, 0),
            "blast velocity can not be 0")      
    
    def test_death_by_asteroid(self):
        """
            Testing the death_by_asteroid function 
        """
        asteroid = {"t_per_asteroid_cycle": 4, "offset": 2} 

        logger.info('\nCycle Time: {0}, Offset: {1}'.format(asteroid['t_per_asteroid_cycle'],
            asteroid['offset']))
        self.assertTrue(utils.death_by_asteroid(asteroid, 10),
            "Spacship should have collided with asteroid at t=10")
        self.assertFalse(utils.death_by_asteroid(asteroid, 9),
            "Spacship should have no collision with asteroid at t=9")
        self.assertFalse(utils.death_by_asteroid(asteroid, 8),
            "Spacship should have no collision with asteroid at t=9")
        self.assertFalse(utils.death_by_asteroid(asteroid, 7),
            "Spacship should have no collision with asteroid at t=9")

        with patch.dict(asteroid, offset=3):
            logger.info('Cycle Time: {0}, Offset: {1}'.format(asteroid['t_per_asteroid_cycle'],
                asteroid['offset']))
            self.assertFalse(utils.death_by_asteroid(asteroid, 10),
                "Spacship should have no collision with asteroid at t=10")
            self.assertTrue(utils.death_by_asteroid(asteroid, 9),
                "Spacship should have collided with asteroid at t=9")
            self.assertFalse(utils.death_by_asteroid(asteroid, 8),
                "Spacship should have no collision with asteroid at t=9")
            self.assertFalse(utils.death_by_asteroid(asteroid, 7),
                "Spacship should have no collision with asteroid at t=9")

        with patch.dict(asteroid, t_per_asteroid_cycle=1):
            logger.info('Cycle Time: {0}, Offset: {1}'.format(asteroid['t_per_asteroid_cycle'],
                asteroid['offset']))
            self.assertTrue(utils.death_by_asteroid(asteroid, 1),
                "Spacship should always collide with asteriod with cycle time 1")
            self.assertTrue(utils.death_by_asteroid(asteroid, 2),
                "Spacship should always collide with asteriod with cycle time 1")
            self.assertTrue(utils.death_by_asteroid(asteroid, 5),
                "Spacship should always collide with asteriod with cycle time 1")
            self.assertTrue(utils.death_by_asteroid(asteroid, 6),
                "Spacship should always collide with asteriod with cycle time 1")

    def test_check_asteroid(self):
        """
            Testing the check_asteroid function
        """
        asteroid = {"t_per_asteroid_cycle": 3, "offset": 2} 
        self.assertEqual(utils.check_asteroid(asteroid, 1), None)
        logger.info('')

        with patch.dict(asteroid, offset="temp"):
            with self.assertRaises(ValueError):
                utils.check_asteroid(asteroid, 10)
       
        with patch.dict(asteroid, t_per_asteroid_cycle=0):
            with self.assertRaises(ValueError):
                utils.check_asteroid(asteroid, 10)

        with patch.dict(asteroid, t_per_asteroid_cycle='temp'):
            with self.assertRaises(ValueError):
                utils.check_asteroid(asteroid, 10)

        with patch.dict(asteroid):
            asteroid.pop('t_per_asteroid_cycle')
            with self.assertRaises(ValueError):
                utils.check_asteroid(asteroid, 10)

        with patch.dict(asteroid):
            asteroid.pop('offset')
            with self.assertRaises(ValueError):
                utils.check_asteroid(asteroid, 10)

    
    def test_get_nxt_states(self):
        """
            Testing the get_nxt_states function
        """
        asteroid = {"t_per_asteroid_cycle": 1, "offset":0}
        asteroids = [asteroid]*5
        
        state = (0,0,1)
        nxt_states = []
        blast_time_step = 10
        for a, state in utils.get_nxt_states(state, blast_time_step, asteroids):
            nxt_states.append(state)
        self.assertEqual(nxt_states, [(0,0,2)])

        # test edge case when no next state possible
        state = (0,0,9)
        nxt_states = []
        blast_time_step = 10
        for a, state in utils.get_nxt_states(state, blast_time_step, asteroids):
            nxt_states.append(state)
        self.assertEqual(nxt_states, [])


    @classmethod
    def tearDownClass(cls):
        logger.removeHandler(cls.console)


if __name__ == '__main__':
    unittest.main()