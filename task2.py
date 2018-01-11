from graphviz import Digraph

dot = Digraph(comment='The Round Table')

dot.node('1', '1-2-3-4')
dot.node('2', '1')
dot.node('3', '2-3')
dot.node('4', '4')
dot.node('5', '2')
dot.node('6', '3')

# dot.edges(['AB', 'AL', 'AC', 'BC'])
dot.edge('1', '2', constraint='true')
dot.edge('1', '3', constraint='true')
dot.edge('1', '4', constraint='true')
dot.edge('3', '5', constraint='true')
dot.edge('3', '6', constraint='true')
print(dot)
dot.render('test-output/round-table.gv', view=True)
