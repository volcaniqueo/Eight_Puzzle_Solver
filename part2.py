from queue import PriorityQueue
import sys

astar_explored = set()  # The set of states that have been explored.
astar_queue = set()  # The set of states that are in the queue.
# The dictionary of costs of states that are in the queue. The costs are the f(n) values, i.e. the path cost + heuristic.
# The reason for me to use a dictionary is that accessing and deleting f(n) value of a given state in the fringe is very costly since PriortyQueue is not directly support such operations.
# If there is a child whose f(n) is lower than the node of a fringe (having same states of course), I also add the child to the fringe. So, fringe can have multiple nodes with same states but different f(n) values.
# But after exploring one with the lowest f(n) value, with the help of the check in the line 167, others directly popped without having any effect on the result.
astar_state_fn_cost = {}   

# The class that represents the 8-puzzle problem.
class Eight_Puzzle_Problem_3_Blanks:

    def __init__(self, initial, goal=None):
        self.initial = initial  # Initial state.
        self.goal = goal  # Goal state.

    # Since we have multiple blank tiles, we should also specify the index of 0 along with the action.
    def actions(self, state):
        actions_list = []
        blanks = [i for i in range(len(state)) if state[i] == "0"]
        for index in blanks:
            if index == 0:
                actions = [0, 'R', 'D']
            elif index == 1:
                actions = [1, 'R', 'D', 'L']
            elif index == 2:
                actions = [2, 'D', 'L']
            elif index == 3:
                actions = [3, 'U', 'R', 'D']
            elif index == 4:
                actions = [4, 'U', 'R', 'D', 'L']
            elif index == 5:
                actions = [5, 'U', 'D', 'L']
            elif index == 6:
                actions = [6, 'U', 'R']
            elif index == 7:
                actions = [7, 'U', 'R', 'L']
            elif index == 8:
                actions = [8, 'U', 'L']
            actions_list.append(actions)
        return actions_list
    
    @staticmethod
    def result(state, action, index):
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
    

class Node_Astar:

    # Action proirty is implemented as requested in the project description.
    action_priority = {'U': 0, 'R': 1, 'D': 2, 'L': 3}

    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.heuristic = self.manhattan_distance(self.state) + (self.linear_conflicts(self.state) * 2)  # Heuristic is explained in the pdf.

    def __eq__(self, other):
        return self.state == other.state
    
    def expand(self, problem):
        childs = []
        action_list = problem.actions(self.state)
        for actions in action_list:
            index = actions.pop(0)
            for action in actions:
                next_state = Eight_Puzzle_Problem_3_Blanks.result(self.state, action, index)
                next_node = Node_Astar(next_state, self, [action, index], self.path_cost + 1)
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
    
    # For the PriorityQueue (fringe), the f(n) function is the sum of the heuristic value and the path cost. Then
    # actions are prioritized according to the project description.
    def __lt__(self, other):
        if self.path_cost + self.heuristic < other.path_cost + other.heuristic:
            return True
        elif self.path_cost + self.heuristic == other.path_cost + other.heuristic:
            return self.action_priority[self.action[0]] < self.action_priority[other.action[0]]
        else:
            return False
    
    # Function to check the given action list is indeed a solution.
    @staticmethod
    def check_actions_path(state, actions, file):
        file.write("States: " + "\n")
        Node_Astar.print_states(state, file)
        for action in actions:
            next_state = Eight_Puzzle_Problem_3_Blanks.result(state, action[0], action[1])
            state = next_state
            Node_Astar.print_states(state, file)
        return state
    
    # Manhattan distance heuristic function.
    @staticmethod
    def manhattan_distance(state):
        goal = "123456780"
        distance = 0
        for i in range(1, 7):
            dx = abs(state.index(str(i)) % 3 - goal.index(str(i)) % 3)
            dy = abs(state.index(str(i)) // 3 - goal.index(str(i)) // 3)
            distance += (dx + dy)
        return distance
    
    # Linear conflicts heuristic function.
    @staticmethod
    def linear_conflicts(state):
        conflicts = 0
        if state.index("1") == 1:
            if state.index("2") == 0:
                conflicts += 1
        if state.index("1") == 3:
            if state.index("4") == 0:
                conflicts += 1
        if state.index("2") == 4:
            if state.index("5") == 1:
                conflicts += 1
        if state.index("2") == 2:
            if state.index("3") == 1:
                conflicts += 1
        if state.index("3") == 5:
            if state.index("6") == 2:
                conflicts += 1
        if state.index("4") == 4:
            if state.index("5") == 3:
                conflicts += 1
        if state.index("5") == 5:
            if state.index("6") == 4:
                conflicts += 1
        return conflicts
    
    # Function to print the states in a 3x3 grid.
    @staticmethod
    def print_states(state, file):
        file.write(state[0] + " " + state[1] + " " + state[2] + "\n")
        file.write(state[3] + " " + state[4] + " " + state[5] + "\n")
        file.write(state[6] + " " + state[7] + " " + state[8] + "\n")
        file.write("\n")
    
# Classical A* search implementation. It is the exact implementation of the pseudo-code in the course textbook. One difference is the extra check in the line 177.
# The reasoning for this check is explained in the astar_state_fn_cost variable's comment.
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

Eight_Puzzle = Eight_Puzzle_Problem_3_Blanks(input_state, "123456000")

astar_result = astar(Eight_Puzzle)

with open(sys.argv[2], 'w') as file:
    Node_Astar.check_actions_path(input_state, astar_result.actions(), file)
    file.write("Path Cost: " + str(astar_result.path_cost) + "\n")
    file.write("Expanded Nodes: " + str(len(astar_explored) + len(astar_queue)) + "\n")


    

    
    


