from Queue import *
import copy
import sys


def sat(chosen_var, asg, hm1, hm2):
    # Decision Variable Assignment
    hm3 = Queue(maxsize=0)
    for app in hm1[chosen_var]:
        if app == asg:
            for clause in hm1[chosen_var][app]:
                for v in range(0, 2):
                    for var in hm2[clause][v]:
                        if var == chosen_var:
                            continue
                        hm1[var][v].remove(clause)
                del hm2[clause]
        else:
            for clause in hm1[chosen_var][app]:
                hm2[clause][app].remove(chosen_var)
                if len(hm2[clause][0]) + len(hm2[clause][1]) == 0:
                    return False
    del hm1[chosen_var]
    for clause in hm2:
        if len(hm2[clause][0]) + len(hm2[clause][1]) == 1:
            hm3.put(clause)
    # Check if true
    if len(hm2) == 0:
        return True
    # BCP
    while not hm3.empty():
        unit = hm3.get()
        if unit not in hm2.keys():
            continue
        if len(hm2[unit][1]) != 0:
            pos_neg = 1
            var = hm2[unit][1][0]
        else:
            pos_neg = 0
            var = hm2[unit][0][0]
        for clause in hm1[var][pos_neg]:
            for v in range(0, 2):
                for term in hm2[clause][v]:
                    if term == var:
                        continue
                    hm1[term][v].remove(clause)
            del hm2[clause]
        for clause in hm1[var][(pos_neg + 1) % 2]:
            hm2[clause][(pos_neg + 1) % 2].remove(var)
            if len(hm2[clause][0]) + len(hm2[clause][1]) == 0:
                return False
            elif len(hm2[clause][0]) + len(hm2[clause][1]) == 1:
                hm3.put(clause)
        del hm1[var]
    # Check if true
    if len(hm2) == 0:
        return True
    # Set pure true
    pure_literals = Queue(maxsize=0)
    for lit in hm1:
        if len(hm1[lit][0]) != 0 and len(hm1[lit][1]) == 0:
            v = 0
        elif len(hm1[lit][0]) == 0 and len(hm1[lit][1]) != 0:
            v = 1
        else:
            continue
        for clause in hm1[lit][v]:
            for var in hm2[clause][0]:
                if var == lit:
                    continue
                hm1[var][0].remove(clause)
            for var in hm2[clause][1]:
                if var == lit:
                    continue
                hm1[var][1].remove(clause)
            del hm2[clause]
        pure_literals.put(lit)
    while not pure_literals.empty():
        del hm1[pure_literals.get()]
    # Check if true
    if len(hm2) == 0:
        return True
    # Choose variable
    max_times = 0
    chosen_var = 0
    non_exist_var = Queue(maxsize=0)
    for var in hm1:
        if len(hm1[var][0]) + len(hm1[var][1]) == 0:
            non_exist_var.put(var)
        elif len(hm1[var][0]) + len(hm1[var][1]) > max_times:
            max_times = len(hm1[var][0]) + len(hm1[var][1])
            chosen_var = var
    while not non_exist_var.empty():
        del hm1[non_exist_var.get()]
    d_hm1 = copy.deepcopy(hm1)
    d_hm2 = copy.deepcopy(hm2)
    return sat(chosen_var, 0, hm1, hm2) or sat(chosen_var, 1, d_hm1, d_hm2)


file_handle = open(sys.argv[1])
file_lines = file_handle.readlines()
file_handle.close()
hm_1 = dict()
hm_2 = dict()
flag = 0
curr_clause = 0
for line in file_lines:
    args = line.split()
    if not flag:
        if args[0] == 'c':
            continue
        elif args[0] == 'p':
            num_var = int(args[2])
            num_clause = int(args[3])
            flag = 1
            curr_clause = 1
            for i in range(1, num_var + 1):
                hm_1[i] = {0: [], 1: []}
            for i in range(1, num_clause + 1):
                hm_2[i] = {0: [], 1: []}
    else:
        for s_var in args:
            if int(s_var) != 0:
                pos_neg = 1
                if int(s_var) < 0:
                    pos_neg = 0
                var = abs(int(s_var))
                hm_1[var][pos_neg].append(curr_clause)
                hm_2[curr_clause][pos_neg].append(var)
            else:
                curr_clause += 1
d_hm_1 = copy.deepcopy(hm_1)
d_hm_2 = copy.deepcopy(hm_2)
result = sat(1, 0, hm_1, hm_2) or sat(1, 1, d_hm_1, d_hm_2)
if result:
    print 's SATISFIABLE'
else:
    print 's UNSATISFIABLE'
