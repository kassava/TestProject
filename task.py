import math
import numpy as np
from graphviz import Digraph
from Node import Node


fname = "input1.txt"
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


def separate_modes(parent_node, test_list, state_set):
    mode_set = check_modes_values(modes)  # определение количества режимов
    custom_test_list = delete_list(init_test_list.copy(), test_list)  # проверки, которые ещё не проводились
    for j in custom_test_list:  # разделение на группы состояний по режимам по каждому признаку
        d = dict()  # состояния, разделённые по режимам
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

                print(t_list, state)
                states_list.append(node)
                separate_modes(node, t_list, state)
            else:
                node = Node(state, t_list)

                dot.node(str(hash(node)), state_set_to_string(state))
                dot.edge(str(hash(parent_node)), str(hash(node)), str(j), constraint='true')

                print(t_list, state)
                states_list.append(node)


def calculate_graph(test_list, state_set):
    custom_test_list = delete_list(init_test_list.copy(), test_list)  # проверки, которые ещё не проводились
    local_state_list = list()
    for j in custom_test_list:  # разделение на группы состояний по режимам по каждому признаку
        d = dict()  # состояния, разделённые по режимам
        for m in mode_set:
            d[m] = set()
        for i in state_set:
            d[modes[i - 1, j - 1]].add(i)
        t_list = test_list.copy()
        t_list.append(j)
        for state in d.values():
            if len(state) == 0:
                continue
            node = Node(state, t_list)
            print(t_list, state)
            local_state_list.append(node)
    step2(local_state_list)


def step2(local_state_list):
    values = list()
    for node in local_state_list:
        custom_test_list = delete_list(init_test_list.copy(), node.tests)
        one_state_values = dict()
        for j in custom_test_list:  # разделение на группы состояний по режимам по каждому признаку
            d = dict()  # состояния, разделённые по режимам
            for m in mode_set:
                d[m] = set()
            for i in node.states:
                d[modes[i - 1, j - 1]].add(i)
            t_list = node.tests.copy()
            t_list.append(j)
            sum_probability = list()
            for state in d.values():
                if len(state) == 0:
                    continue
                sum_probability.append(get_total_probilities_sum(state))
            # нормировка вероятности по текущему состоянию
            sum_probability[:] = [x / sum(sum_probability) for x in sum_probability]
            value = 0
            for x in sum_probability:
                value += x * x
            value = value - (1 / len(sum_probability))
            one_state_values[j] = value
        values.append(max(one_state_values))


def state_count(state):  # определение количества групп состояний в множестве групп, соответствующему признаку
    count = 0
    for st in state.values():
        if len(st) > 0:
            count += 1
    return count


def get_total_probilities_sum(state):
    total = 0
    for v in state:
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


mode_set = check_modes_values(modes)  # определение количества режимов
start_node = Node(init_state_list, list())
# dot.node(str(hash(start_node)), state_set_to_string(init_state_list))

# separate_modes(start_node, list(), init_state_list)
print(list(), init_state_list)
states_list.append(start_node)
calculate_graph(list(), init_state_list)
print(len(states_list))
# dot.format = 'png'
# dot.render('test-output/round-table.gv', view=True)
