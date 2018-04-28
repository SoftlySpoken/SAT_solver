# SAT_solver
A satisfiability solver implemented with the DPLL algorithm.

##### Parsing the dimacs-CNF File

`sys.argv()` is used to extract the file name from the command line. I use the `readlines()` function to read the file and store it in a list. Then I parse each line of the file by using the `split()` function.

##### Data Structure

Throughout the program, I use two `dict` objects: the first one stores which clauses each variable is present in and whether the variable is present as a literal (denoted by 1) or the negation of a literal (denoted by 0); the second one stores which variables are present in each clause and whether the variables are present as a literal or the negation of the literal. During BCP, a FIFO queue (imported from the `Queue` module) is used to store the unit clauses.

An example of the two `dict` objects:

    # x1 and (not x1 or x2) and (x2 or not x3) and (x1 or x2)
    hm1 = {1: {0: [2], 1: [1, 4]}, 2: {0: [], 1: [2, 3, 4]}, 3: {0: [3], 1: []}}
    hm2 = {1: {0: [], 1: [1]}, 2: {0: [1], 1: [2]}, 3: {0: [3], 1: [2]}, 4: {0: [], 1: [1, 2]}}

##### The DPLL Algorithm

The DPLL algorithm is implemented as a recursive function that takes four arguments: the decision variable chosen to be assigned a value, the value to be assigned, and the two `dict` objects mentioned in the previous section.

- Decision Variable Assignment
  Given the decision variable and the value to be assigned, for the clauses in which the presence of the variable is denoted by the value to be assigned (meaning the variable is a literal and the value is 1, or the variable is a negation of a literal and the value is 0), the clause becomes true and is deleted; otherwise, this variable is deleted from the clause. Afterwards, check if the formula is empty, and return True if positive.

- BCP
  First, add unit clauses to the FIFO queue. Then for each unit clause, those clauses in which the presence of the variable has the same denotation as in the unit clause (both present as a literal or the negation of a literal) is deleted, while the variable in the unit clause is deleted from those clauses in which the presence of the variable has a denotation that is the complement of that of the unit clause. Each time a variable is deleted from a clause, check if the clause is empty, and return False if positive; also check if the clause is a unit clause, and add it to the queue if positive. Finally, delete the variable in the unit clause. Afterwards, check if the formula is empty, and return True if positive.
- Setting Pure Literals to True
  Find pure literals by calculating if a certain variable's presence is only denoted by 0 or 1. Delete the clauses containing them. Finally, delete the pure literals. Afterwards, check if the formula is empty, and return True if positive.
- Choosing the Decision Variable
  Find the variable that has maximum times of presence and choose it as the decision variable. During the process, also delete the variables that are not present in any clause.
