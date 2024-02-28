# Eight_Puzzle_Solver
This project was my 1st Homework for the course CMPE 480 (Introduction to Artificial Intelligence) at Bogazici University.

## About the Project
The project consists of two different parts. In the first part, the classical eight puzzle is solved with five different search algorithms (Breadth First Search, Depth First Search, Uniform Cost Search, Greedy Search, A* Search).
The Manhattan Distance is used as heuristic for Greedy & A* Search. In the second part, classical eight puzzle problem is modified such that the number of blanks is now three. Then A* search is used to find a solution. The heuristic that is used for 
A* search can be found in the 'heuristic.pdf' file. Please refer to the project description or example inputs folder for the formatting of the input. Also, for the output format, please refer to the project description.

## To Run the Code
One just need Python 3 to run the code. The program expects two arguments (as .txt files) whose formats are explicity written in the project description.

So, simply run:

```python3 part1.py <input_file> <output_file>```   (for the part 1)

```pyhton3 part2.py <input_file> <output_file>```   (for the part 2)

## Final Remarks
For the heuristics in the part 2, pattern database type heuristics would be better in performance for the A* search; but this was forbidden for this project.
