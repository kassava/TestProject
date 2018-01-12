import math

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from graphviz import Digraph

from Node import Node

fname = "input1.txt"
input_data = np.loadtxt(fname, dtype=None, delimiter='\t')
modes = input_data[:, 0:-1]  # массив режимов (количество состояний на количество признаков)
probabilities = input_data[:, -1]  # массив вероятностей состояний
states_list = list()
init_test_set = list(range(1, len(modes[0]) + 1))  # множество проверок
init_state_set = list(range(1, len(modes[:]) + 1))  # множество состояний
dot = Digraph(comment='Граф состояний')
node_number = 0

G = nx.Graph()


def check_modes_values(data):  # определение количества различных режимов
    mode = set()
    for i in range(len(data[:])):
        for j in range(len(data[0])):
            mode.add(data[i][j])
    return mode


def delete_list(a, b):
    for x in b:
        try:
            a.remove(x)
        except ValueError:
            pass
    return a


def state_set_to_string(v):
    return ' '.join(str(s) for s in v)


def the_first_modes_separation(modes):
    mode_set = check_modes_values(modes)  # определение количества режимов
    test_set = list(range(0, len(modes[0])))
    for j in test_set:  # разделение на группы состояний по режимам по каждому признаку
        d = dict()
        for m in mode_set:
            d[m] = set()
        for i in range(len(modes[:])):
            d[modes[i, j]].add(i + 1)
        t_set = list(range(1, len(modes[0]) + 1))
        t_set.remove(j + 1)
        for v in d.values():
            if len(v) == 0:
                continue
            if len(t_set) > 1 and len(v) > 1:
                node = Node(t_set, v)
                # print(node.state_list, node.modes)
                tmp_set = init_test_set.copy()
                tmp_set = delete_list(tmp_set, t_set)
                print(tmp_set, v)
                states_list.append(node)
                mode_separation(modes, t_set, v)
            else:
                node = Node(t_set, v)
                # print(node.state_list, node.modes)
                tmp_set = init_test_set.copy()
                tmp_set = delete_list(tmp_set, t_set)
                print(tmp_set, v)
                states_list.append(node)


def mode_separation(parent_node, test_list, state_set):
    global node_number
    mode_set = check_modes_values(modes)  # определение количества режимов
    custom_test_list = delete_list(init_test_set.copy(), test_list) # проверки, которые ещё не проводились
    for j in custom_test_list:  # разделение на группы состояний по режимам по каждому признаку
        d = dict() # состояния, разделённые по режимам
        for m in mode_set:
            d[m] = set()
        for i in state_set:
            d[modes[i - 1, j - 1]].add(i)
        t_list = test_list.copy()
        t_list.append(j)
        for state in d.values():
            if len(state) == 0:
                continue
            if len(t_list) < 6 and len(state) > 1:
                node = Node(state, t_list)

                dot.node(str(hash(node)), state_set_to_string(state))
                dot.edge(str(hash(parent_node)), str(hash(node)), str(j), constraint='true')

                G.add_node(str(hash(node)))
                G.add_edge(str(hash(parent_node)), str(hash(node)))

                print(t_list, state)
                states_list.append(node)
                mode_separation(node, t_list, state)
            else:
                node = Node(state, t_list)

                dot.node(str(hash(node)), state_set_to_string(state))
                dot.edge(str(hash(parent_node)), str(hash(node)), str(j), constraint='true')

                G.add_node(str(hash(node)))
                G.add_edge(str(hash(parent_node)), str(hash(node)))

                print(t_list, state)
                states_list.append(node)


def state_count(state):  # определение количества групп состояний в множестве групп, соответствующему признаку
    count = 0
    for st in state.values():
        if len(st) > 0:
            count += 1
    return count


def get_total_probilities_sum(state):
    total = 0
    for values in state.state_list:
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


start_node = Node(init_state_set, list())
print(str(hash(start_node)), '-',state_set_to_string(init_state_set))
dot.node(str(hash(start_node)), state_set_to_string(init_state_set))

mode_separation(start_node, list(), init_state_set)
print(len(states_list))
# dot.format = 'png'
dot.render('test-output/round-table.gv', view=True)

# for s in states_list:
#     formula(s)


# nx.draw(G,pos=nx.spring_layout(G), nodecolor='r',edge_color='b')
# plt.figure(figsize=(8, 6))
# nx.draw(g, pos=node_positions, edge_color=edge_colors, node_size=10, node_color='black')
# plt.title('Graph Representation of Sleeping Giant Trail Map', size=15)
# plt.show()
