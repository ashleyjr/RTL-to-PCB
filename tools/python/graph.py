import pickle

with open('test.pkl', 'rb') as f:
    cells = pickle.load(f)

for cell in cells:
    print(cell)
    print(cells[cell])

import pydot

graph = pydot.Dot('my_graph', graph_type='digraph', bgcolor='white', overlap="false")

# Add nodes
for cell in cells:
    if cell[0] == "D":
        c = "red"
    if cell[0] == "P":
        c = "green"
    if cell[0] == "N":
        c = "cyan"
    node = pydot.Node(f'{cell}', label=f'{cell}', color=c)
    graph.add_node(node)


## Add edges
for cell_a in cells:
    if cell_a[0] == "N":
        print(cells[cell_a][2]['Y'])
        for cell_b in cells:
            if cell_b[0] == "N":
                if (cells[cell_a][2]['Y'] == cells[cell_b][0]['A']) or\
                   (cells[cell_a][2]['Y'] == cells[cell_b][1]['B']):
                    edge = pydot.Edge(cell_a, cell_b, color='black')
                    graph.add_edge(edge)
            if cell_b[0] == "D":
                if (cells[cell_a][2]['Y'] == cells[cell_b][1]['D']):
                    edge = pydot.Edge(cell_a, cell_b, color='black')
                    graph.add_edge(edge)

    if cell_a[0] == "D":
        print(cells[cell_a][2]['Q'])
        for cell_b in cells:
            if cell_b[0] == "N":
                if (cells[cell_a][2]['Q'] == cells[cell_b][0]['A']) or\
                   (cells[cell_a][2]['Q'] == cells[cell_b][1]['B']):
                    edge = pydot.Edge(cell_a, cell_b, color='black')
                    graph.add_edge(edge)
            if cell_b[0] == "D":
                if (cells[cell_a][2]['Q'] == cells[cell_b][1]['D']):
                    edge = pydot.Edge(cell_a, cell_b, color='black')
                    graph.add_edge(edge)

    if cell_a[0] == "P":
        print(cells[cell_a][0]['A'])
        for cell_b in cells:
            if cell_b[0] == "N":
                if (cells[cell_a][0]['A'] == cells[cell_b][0]['A']) or\
                   (cells[cell_a][0]['A'] == cells[cell_b][1]['B']):
                    edge = pydot.Edge(cell_a, cell_b, color='black')
                    graph.add_edge(edge)
            if cell_b[0] == "D":
                if (cells[cell_a][0]['A'] == cells[cell_b][1]['D']):
                    edge = pydot.Edge(cell_a, cell_b, color='black')
                    graph.add_edge(edge)
                if (cells[cell_a][0]['A'] == cells[cell_b][0]['C']):
                    edge = pydot.Edge(cell_a, cell_b, color='black')
                    graph.add_edge(edge)



#for cell in cells:
#my_edge = pydot.Edge('a', 'b', color='blue')
#graph.add_edge(my_edge)
## Or, without using an intermediate variable:
#graph.add_edge(pydot.Edge('b', 'c', color='blue'))

graph.write_png('output.png')
