from wrap import wrapper

def main():

    w = wrapper(
        filename='digraph_01.gv', 
        # fileformat='svg',
        )
    
    w.make_nodes('1', '3', '5', '7',
        choose_node_design='node_design_0')
    
    w.make_nodes('2', '4', '6',
        choose_node_design='node_design_1')

    w.make_chain('1', '2', '3',
        choose_edge_design='edge_design_0')
    
    w.make_chain('4', '5', '6', '7',
        choose_edge_design='edge_design_1')

    w.viz()

if __name__ == "__main__":
    main()