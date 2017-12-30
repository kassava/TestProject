import math

import numpy as np

from Node import Node

fname = "input1.txt"
input_data = np.loadtxt(fname, dtype=None, delimiter='\t')
init_modes = input_data[:, 0:-1]  # массив режимов (количество состояний на количество признаков)
probabilities = input_data[:, -1]  # массив вероятностей состояний
states_list = list()
init_test_set = set(range(1, len(init_modes[0]) + 1))


def check_modes_values(data):  # определение количества различных режимов
    mode = set()
    for i in range(len(data[:])):
        for j in range(len(data[0])):
            mode.add(data[i][j])
    return mode


def the_first_modes_separation(modes):
    mode_set = check_modes_values(modes)  # определение количества режимов
    test_set = list(range(0, len(modes[0])))
    for j in test_set:  # разделение на группы состояний по режимам по каждому признаку
        d = dict()
        for m in mode_set:
            d[m] = set()
        for i in range(len(modes[:])):
            d[modes[i, j]].add(i + 1)
        t_set = set(range(1, len(modes[0]) + 1))
        t_set.discard(j + 1)
        for v in d.values():
            if len(v) == 0:
                continue
            if len(t_set) > 1 and len(v) > 1:
                node = Node(t_set, v)
                # print(node.state_list, node.modes)
                tmp_set = init_test_set.copy().difference(t_set)
                print(tmp_set, v)
                states_list.append(node)
                mode_separation(modes, t_set, v)
            else:
                node = Node(t_set, v)
                print(node.state_list, node.modes)
                states_list.append(node)


def mode_separation(modes, test_set, state_set):
    mode_set = check_modes_values(modes)  # определение количества режимов
    print("state: ", state_set)
    for j in test_set:  # разделение на группы состояний по режимам по каждому признаку
        d = dict()
        for m in mode_set:
            d[m] = set()
        for i in state_set:
            d[modes[i - 1, j - 1]].add(i)
        t_set = test_set.copy()
        t_set.discard(j)
        test_set = t_set
        for v in d.values():
            if len(v) == 0:
                continue
            if len(t_set) > 1 and len(v) > 1:
                node = Node(t_set, v)
                # print(node.state_list, node.modes)
                tmp_set = init_test_set.copy().difference(t_set)
                print(tmp_set, v)
                states_list.append(node)
                mode_separation(modes, t_set, v)
            else:
                node = Node(t_set, v)
                # print(node.state_list, node.modes)
                tmp_set = init_test_set.copy().difference(t_set)
                print(tmp_set, v)
                states_list.append(node)


def state_count(state):  # определение количества групп состояний в множестве групп, соответствующему признаку
    count = 0
    for st in state.values():
        if len(st) > 0:
            count += 1
    return count


def get_total_probilities_sum(state):
    total = 0
    for values in state.values():
        for v in values:
            total += probabilities[v - 1]
    return total


def formula(state):  # вычисление значений по формулам
    summa = 0
    total_probabilities_sum = get_total_probilities_sum(state)
    for values in state.values():
        probabilities_sum = 0
        for v in values:
            probabilities_sum += probabilities[v - 1]
        if probabilities_sum == 0:
            continue
        value = state_count(state) * probabilities_sum / total_probabilities_sum - 1
        log = math.log(probabilities_sum, 2)
        summa += (value * log)
    print(summa)


the_first_modes_separation(init_modes)
print(len(states_list))
# print(np.array(states))
# for s in states:
#     formula(s)
