from queue import PriorityQueue
import sys
from collections import deque

bfs_explored = set()
dfs_explored = set()
uni_explored = set()
greedy_explored = set()
astar_explored = set()

bfs_queue = set()
dfs_queue = set()
uni_queue = set()
greedy_queue = set()
astar_queue = set()

# The dictionaries of costs of states that are in the queue. The costs are the f(n) values, i.e. the path cost + heuristic (for greedy, only the heuristic).
# The reason for me to use a dictionary is that accessing and deleting f(n) value of a given state in the fringe is very costly since PriortyQueue is not directly support such operations.
# If there is a child whose f(n) is lower than the node of a fringe (having same states of course), I also add the child to the fringe. So, fringe can have multiple nodes with same states but different f(n) values.
# But after exploring one with the lowest f(n) value, with the help of the checks in the lines 261/289/317, others directly popped without having any effect on the result.
uni_state_fn_cost = {}
greedy_state_fn_cost = {}
astar_state_fn_cost = {}

# The class that represents the 8-puzzle problem.
class Eight_Puzzle_Problem:

    def __init__(self, initial, goal=None):
        self.initial = initial  # Initial state.
        self.goal = goal  # Goal state.

    def actions(self, state):
        actions = []
        index = state.index('0')
        if index == 0:
            actions = ['R', 'D']
        elif index == 1:
            actions = ['R', 'D', 'L']
        elif index == 2:
            actions = ['D', 'L']
        elif index == 3:
            actions = ['U', 'R', 'D']
        elif index == 4:
            actions = ['U', 'R', 'D', 'L']
        elif index == 5:
            actions = ['U', 'D', 'L']
        elif index == 6:
            actions = ['U', 'R']
        elif index == 7:
            actions = ['U', 'R', 'L']
        elif index == 8:
            actions = ['U', 'L']
        return actions
    
    @staticmethod
    def result(state, action):
        index = state.index('0')
        new_state = list(state)
        if action == 'U':
            new_state[index], new_state[index-3] = new_state[index-3], new_state[index]
        elif action == 'R':
            new_state[index], new_state[index+1] = new_state[index+1], new_state[index]
        elif action == 'D':
            new_state[index], new_state[index+3] = new_state[index+3], new_state[index]
        elif action == 'L':
            new_state[index], new_state[index-1] = new_state[index-1], new_state[index]
        return ''.join(new_state)
    
    def goal_test(self, state):
        return state == self.goal
    

class Node:

    # Action proirty is implemented as requested in the project description.
    action_priority = {'U': 0, 'R': 1, 'D': 2, 'L': 3}

    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

    def __eq__(self, other):
        return self.state == other.state
    
    def expand(self, problem):
        childs = []
        for action in problem.actions(self.state):
            next_state = Eight_Puzzle_Problem.result(self.state, action)
            next_node = Node(next_state, self, action, self.path_cost + 1)
            childs.append(next_node)
        return childs
    
    def __hash__(self):
        return hash(self.state)
    
    def actions(self):
        actions = []
        node = self
        while node.parent is not None:
            actions.append(node.action)
            node = node.parent
        actions.reverse()
        return actions
    
    @staticmethod
    def check_actions_path(state, actions):
        for action in actions:
            next_state = Eight_Puzzle_Problem.result(state, action)
            state = next_state
        return state


    
    @staticmethod
    def manhattan_distance(state):
        goal = "123456780"
        distance = 0
        for i in range(1, 9):
            dx = abs(state.index(str(i)) % 3 - goal.index(str(i)) % 3)
            dy = abs(state.index(str(i)) // 3 - goal.index(str(i)) // 3)
            distance += (dx + dy)
        return distance
    
    @staticmethod
    def print_states(state):
        print(state[0] + " " + state[1] + " " + state[2])
        print(state[3] + " " + state[4] + " " + state[5])
        print(state[6] + " " + state[7] + " " + state[8])
        print()
        
class Node_Astar(Node):

    def __init__(self, state, parent=None, action=None, path_cost=0):
        super().__init__(state, parent, action, path_cost)
        self.heuristic = self.manhattan_distance(state)
    
    # For the PriorityQueue (fringe), the f(n) function is the sum of the heuristic value and the path cost. Then
    # actions are prioritized according to the project description.
    def __lt__(self, other):
        if self.path_cost + self.heuristic < other.path_cost + other.heuristic:
            return True
        elif self.path_cost + self.heuristic == other.path_cost + other.heuristic:
            return self.action_priority[self.action] < self.action_priority[other.action]
        else:
            return False
        
    def expand(self, problem):
        childs = []
        for action in problem.actions(self.state):
            next_state = problem.result(self.state, action)
            next_node = Node_Astar(next_state, self, action, self.path_cost + 1)
            childs.append(next_node)
        return childs
    
class Node_Greedy(Node):

    def __init__(self, state, parent=None, action=None, path_cost=0):
        super().__init__(state, parent, action, path_cost)
        self.heuristic = self.manhattan_distance(state)
    
    # For the PriorityQueue (fringe), the f(n) function is the heuristic value. Then
    # prioritization is made according to the project description. First path cost, then action priority.
    def __lt__(self, other):
        if self.heuristic < other.heuristic:
            return True
        elif self.heuristic == other.heuristic:
            if self.path_cost < other.path_cost:
                return True
            elif self.path_cost == other.path_cost:
                return self.action_priority[self.action] < self.action_priority[other.action]
            else:
                return False
        else:
            return False

    def expand(self, problem):
        childs = []
        for action in problem.actions(self.state):
            next_state = problem.result(self.state, action)
            next_node = Node_Greedy(next_state, self, action, self.path_cost + 1)
            childs.append(next_node)
        return childs
    
class Node_Uniform(Node):
    
    def __init__(self, state, parent=None, action=None, path_cost=0):
        super().__init__(state, parent, action, path_cost)
    
    # For the PriorityQueue (fringe), the f(n) function is the path cost. Then
    # actions are prioritized according to the project description.
    def __lt__(self, other):
        if self.path_cost < other.path_cost:
            return True
        elif self.path_cost == other.path_cost:
            return self.action_priority[self.action] < self.action_priority[other.action]
        else:
            return False
        
    def expand(self, problem):
        childs = []
        for action in problem.actions(self.state):
            next_state = problem.result(self.state, action)
            next_node = Node_Uniform(next_state, self, action, self.path_cost + 1)
            childs.append(next_node)
        return childs
    

# Implementation of the classical breadth-first search algorithm.
def bfs(problem):
    initial_node = Node(problem.initial)
    if problem.goal_test(initial_node.state):
        return initial_node
    fringe = deque([initial_node])
    bfs_queue.add(initial_node.state)
    while fringe:
        node = fringe.popleft()
        bfs_explored.add(node.state)
        bfs_queue.remove(node.state)
        if problem.goal_test(node.state):
            return node
        for child in node.expand(problem):
            if (child.state not in bfs_explored) and child.state not in bfs_queue:
                fringe.append(child)
                bfs_queue.add(child.state)
    return None

# Implementation of the classical depth-first search algorithm.
def dfs(problem):
    initial_node = Node(problem.initial)
    if problem.goal_test(initial_node.state):
        return initial_node
    fringe = deque([initial_node])
    dfs_queue.add(initial_node.state)
    while fringe:
        node = fringe.pop()
        if node.state in dfs_explored:
            continue
        dfs_explored.add(node.state)
        dfs_queue.remove(node.state)
        if problem.goal_test(node.state):
            return node
        for child in node.expand(problem):
            if child.state not in dfs_explored:
                fringe.append(child)
                dfs_queue.add(child.state)
    return None

# Implementation of the classical uniform-cost search algorithm. The only difference is the extra check in the line 261 which is explained in the comments for uni_state_fn_cost dictionary.
def ucs(problem):
    initial_node = Node_Uniform(problem.initial)
    if problem.goal_test(initial_node.state):
        return initial_node
    fringe = PriorityQueue()
    fringe.put(initial_node)
    uni_queue.add(initial_node.state)
    uni_state_fn_cost[initial_node.state] = initial_node.path_cost
    while fringe:
        node = fringe.get()
        if node in uni_explored:
            continue
        uni_explored.add(node.state)
        uni_queue.remove(node.state)
        if problem.goal_test(node.state):
            return node
        for child in node.expand(problem):
            if child.state not in uni_explored and child.state not in uni_queue:
                fringe.put(child)
                uni_queue.add(child.state)
                uni_state_fn_cost[child.state] = child.path_cost
            elif child.state in uni_queue:
                if child.path_cost < uni_state_fn_cost[child.state]:
                    fringe.put(child)
                    uni_state_fn_cost[child.state] = child.path_cost
    return None

# Implementation of the classical greedy search algorithm. The only difference is the extra check in the line 289 which is explained in the comments for greedy_state_fn_cost dictionary.
def greedy(problem):
    initial_node = Node_Greedy(problem.initial)
    if problem.goal_test(initial_node.state):
        return initial_node
    fringe = PriorityQueue()
    fringe.put(initial_node)
    greedy_queue.add(initial_node.state)
    greedy_state_fn_cost[initial_node.state] = initial_node.heuristic
    while fringe:
        node = fringe.get()
        if node.state in greedy_explored:
            continue
        greedy_explored.add(node.state)
        greedy_queue.remove(node.state)
        if problem.goal_test(node.state):
            return node
        for child in node.expand(problem):
            if child.state not in greedy_explored and child.state not in greedy_queue:
                fringe.put(child)
                greedy_queue.add(child.state)
                greedy_state_fn_cost[child.state] = child.heuristic
            elif child.state in greedy_queue:
                if child.heuristic < greedy_state_fn_cost[child.state]:
                    fringe.put(child)
                    greedy_state_fn_cost[child.state] = child.heuristic
    return None

# Implementation of the classical A* search algorithm. The only difference is the extra check in the line 317 which is explained in the comments for astar_state_fn_cost dictionary.
def astar(problem):
    initial_node = Node_Astar(problem.initial)
    if problem.goal_test(initial_node.state):
        return initial_node
    fringe = PriorityQueue()
    fringe.put(initial_node)
    astar_queue.add(initial_node.state)
    astar_state_fn_cost[initial_node.state] = initial_node.heuristic + initial_node.path_cost
    while fringe:
        node = fringe.get()
        if node.state in astar_explored:
            continue
        astar_explored.add(node.state)
        astar_queue.remove(node.state)
        if problem.goal_test(node.state):
            return node
        for child in node.expand(problem):
            if child.state not in astar_explored and child.state not in astar_queue:
                fringe.put(child)
                astar_queue.add(child.state)
                astar_state_fn_cost[child.state] = child.heuristic + child.path_cost
            elif child.state in astar_queue:
                if child.heuristic + child.path_cost < astar_state_fn_cost[child.state]:
                    fringe.put(child)
                    astar_state_fn_cost[child.state] = child.heuristic + child.path_cost
    return None

    
# Program excepts three arguments as requested in the project description.
if len(sys.argv) != 3:
    print("Usage: python part1.py <input_file> <output_file>")
    exit(1)

input_state = ''
with open(sys.argv[1], 'r') as file:
    for line in file:
        line_numbers = ''.join(line.split())
        input_state += line_numbers

#print(input_state)

Eight_Puzzle = Eight_Puzzle_Problem(input_state, "123456780")

bfs_result = bfs(Eight_Puzzle)
dfs_result = dfs(Eight_Puzzle)
ucs_result = ucs(Eight_Puzzle)
greedy_result = greedy(Eight_Puzzle)
astar_result = astar(Eight_Puzzle)

print(Node.check_actions_path(input_state, bfs_result.actions()))
print(Node.check_actions_path(input_state, dfs_result.actions()))
print(Node.check_actions_path(input_state, ucs_result.actions()))
print(Node.check_actions_path(input_state, greedy_result.actions()))
print(Node.check_actions_path(input_state, astar_result.actions()))

with open(sys.argv[2], 'w') as file:

    file.write('BFS: ' + '\n')
    file.write('Expanded nodes: ' + str(len(bfs_explored) + len(bfs_queue)) + '\n')
    file.write('Path cost: ' + str(bfs_result.path_cost) + '\n')
    file.write('Actions: ' + str(bfs_result.actions()) + '\n')
    file.write('DFS: ' + '\n')
    file.write('Expanded nodes: ' + str(len(dfs_explored) + len(dfs_queue)) + '\n')
    file.write('Path cost: ' + str(dfs_result.path_cost) + '\n')
    file.write('Actions: ' + str(dfs_result.actions()) + '\n')
    file.write('UCS: ' + '\n')
    file.write('Expanded nodes: ' + str(len(uni_explored) + len(uni_queue)) + '\n')
    file.write('Path cost: ' + str(ucs_result.path_cost) + '\n')
    file.write('Actions: ' + str(ucs_result.actions()) + '\n')
    file.write('Greedy: ' + '\n')
    file.write('Expanded nodes: ' + str(len(greedy_explored) + len(greedy_queue)) + '\n')
    file.write('Path cost: ' + str(greedy_result.path_cost) + '\n')
    file.write('Actions: ' + str(greedy_result.actions()) + '\n')
    file.write('A*: ' + '\n')
    file.write('Expanded nodes: ' + str(len(astar_explored) + len(astar_queue)) + '\n')
    file.write('Path cost: ' + str(astar_result.path_cost) + '\n')
    file.write('Actions: ' + str(astar_result.actions()) + '\n')



'''
print(bfs_result.state)
print(bfs_result.path_cost)


print(dfs_result.state)
print(dfs_result.path_cost)


print(ucs_result.state)
print(ucs_result.path_cost)


print(greedy_result.state)
print(greedy_result.path_cost)


print(astar_result.state)
print(astar_result.path_cost)
'''

