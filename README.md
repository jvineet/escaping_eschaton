# escaping_eschaton  

The problem was solved using a DFS search on states with backtracking. A state is defined is a tupule of (position, velocity, time) or (p, v, t). For each state we explore all next possible states that don't result in  death by blast, by asteroind collision or collision into the planet, backtracking appropriately if we arrive at a state we had previously exhausted or if our current solution is already longer than the best solution so far. For visitng next states, we visit them in otder of acceleration 1, 0 and -1. We can expect a more optimal solution to have a lot of a=1 so this order is likely to converge to optimal solution faster. Hitting a relatively smaller solution early on in our search improves our ablitity to backtrack quicker. Also, as time is always going forward, there are going to be no cycles in the state  graph.

The DFS state traversal here is implemented iteratively since functions in python have a high overhead that can can cause stack overflow if the recursion depth goes too high. Python also caps recursion to a depth of 1000, which can be increased but still doesn't address the problem of stack overflow with recursion in Python.

The optimal route for escape is stored as a json file 'course.json' in a specified output folder (default folder 'escape_result' is created inside the path where the executible is run, if no output path is supplied)

To Run:
    $ ./escape_eschaton.py <chart.json> [optional args] 
        or 
    $ python<3.x> escape_eschaton.py <chart.json> [optional args] 
      (if the first command doesn't resolve for some reason)

For a detailed list of all arguements, run:

    $ ./escape_eschaton.py -h