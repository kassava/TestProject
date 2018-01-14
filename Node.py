class Node:

    def __init__(self, states, tests):
        self.states = states
        self.tests = tests
        self.value_J = 0
        self.value_S = 0
        self.value_P = 0
        self.value_PJ = self.value_P * self.value_J

    def get_valuePJ(self):
        return self.value_P * self.value_J