import math
import numpy as np
import time
from graphviz import Digraph
from Node import Node


fname = "input2.txt"  # имя файла с исходными данными
input_data = np.loadtxt(fname, dtype=None, delimiter='\t')
modes = input_data[:, 0:-1]  # массив режимов (количество состояний на количество признаков)
probabilities = input_data[:, -1]  # массив вероятностей состояний
states_list = list()
init_test_list = list(range(1, len(modes[0]) + 1))  # исходное множество проверок
init_state_list = list(range(1, len(modes[:]) + 1))  # исходное множество состояний
dot = Digraph(comment='Граф состояний')


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


def calculate_graph(parent_node):
    test_list = parent_node.tests
    state_set = parent_node.states
    if len(state_set) < 2:
        return
    custom_test_list = delete_list(init_test_list.copy(), test_list)  # проверки, которые ещё не проводились
    local_state_list = list()
    total_j = dict()
    for j in custom_test_list:  # разделение на группы состояний по режимам по каждому признаку
        d = dict()  # состояния, разделённые по режимам
        for m in mode_set:
            d[m] = set()
        for i in state_set:
            d[modes[i - 1, j - 1]].add(i)
        t_list = test_list.copy()
        t_list.append(j)
        one_test_state_list = list()
        for state in d.values():
            if len(state) == 0:
                continue
            node = Node(state, t_list)
            # print(t_list, state)
            one_test_state_list.append(node)
            local_state_list.append(node)
        calculate_s(one_test_state_list)
        calculate_j(one_test_state_list)
        total_j[j] = node_value_s_sum(one_test_state_list)
    best_test = key_with_max_value(total_j)

    print("Вычисление номера лучшей проверки", sep=' ', end='', flush=True)
    for number in range(3):
        print("...", sep=' ', end='', flush=True)
        time.sleep(0.3)

    print("the best number: ", best_test)
    for node in local_state_list:
        if best_test in node.tests:
            states_list.append(node)
            if node.states == parent_node.states:
                parent_node.tests = node.tests
                calculate_graph(parent_node)
                continue
            dot.node(str(hash(node)), state_set_to_string(node.states))
            dot.edge(str(hash(parent_node)), str(hash(node)), str(best_test), constraint='true')

            print("Список состояний:", node.states, "Список необходимых проверок: ", node.tests)
            calculate_graph(node)


def node_value_s_sum(state_list):
    total_s_sum = 0
    total_pj_sum = 0
    for node in state_list:
        total_s_sum += node.value_S
        total_pj_sum += node.get_valuePJ()
    return total_s_sum + total_pj_sum


def calculate_p(one_test_state_list):
    state_list_probabilities_sum = 0
    for node in one_test_state_list:
        state_list_probabilities_sum += get_total_probilities_sum(node.states)
    for node in one_test_state_list:
        node.value_P = get_total_probilities_sum(node.states) / state_list_probabilities_sum


def calculate_s(one_test_state_list):
    calculate_p(one_test_state_list)
    for node in one_test_state_list:
        node.value_S = (math.log(node.value_P, 2)) * (node.value_P * len(one_test_state_list) - 1)
        # print(node.value_S)


def calculate_j(local_state_list):
    for node in local_state_list:
        p_at_pi = [probabilities[state - 1] / get_total_probilities_sum(node.states) for state in node.states]
        p_at_pi = [math.log(x, 2) * (len(p_at_pi) * x - 1) for x in p_at_pi]
        node.value_J = sum(p_at_pi)
        # print(node.states, node.tests, node.value_J)


def key_with_max_value(d):
    v = list(d.values())
    k = list(d.keys())
    return k[v.index(max(v))]


def get_total_probilities_sum(state):
    total = 0
    for v in state:
        total += probabilities[v - 1]
    return total


mode_set = check_modes_values(modes)  # определение количества режимов
start_node = Node(init_state_list, list())
dot.node(str(hash(start_node)), state_set_to_string(init_state_list))
states_list.append(start_node)
calculate_graph(start_node)
print("Количество вычисленных состояний: ", len(states_list))
print("Формиование графа состояний", sep=' ', end='', flush=True)
for number in range(3):
    print("...", sep=' ', end='', flush=True)
    time.sleep(1)
dot.format = 'png'
dot.render('test-output/round-table.gv', view=True)
