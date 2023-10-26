from wrap import wrapper

def main():

    w = wrapper(
        filename='digraph_01.gv', 
        # fileformat='svg',
        )
    
    w.make_node('node_design_0', 'node 00')
    w.make_node('node_design_0', 'node 01')

    w.make_node('node_design_1', 'node 02')
    w.make_node('node_design_1', 'node 03')

    w.make_edge('node 00', 'node 02')
    w.make_edge('node 00', 'node 01')
    w.make_edge('node 01', 'node 03')

    w.viz()

if __name__ == "__main__":
    main()