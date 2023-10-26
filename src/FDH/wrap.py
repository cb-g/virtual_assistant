from graphviz import Digraph

class wrapper:
    def __init__(
            self, 
            max_char: int = 20,
            filepath: str = 'src/FDH/viz',
            filename: str = 'digraph_00.gv',
            fileformat: str = 'pdf', # 'png', 'svg'
            ):
        self.filepath = filepath
        self.max_line_len = max_char # maximal amount of characters per line before linebreak

        self.digraph = Digraph(
            'G',
            format=fileformat,
            filename=filename,
            )

    def autolinebreak(self, string: str) -> str:
        x = self.max_line_len
        lst = string.split()
        line = ''
        str_final = ''
        for word in lst:
            if len(line + ' ' + word) <= x:
                str_final += word + ' '
                line += word + ' '
            else:
                str_final += '\n' +  word + ' '
                line = word + ' '
        return str_final

    def design_node(self, choose_node_design: str = 'node_design_0'):
        if choose_node_design == 'node_design_0':
            node_design = {
                'shape': 'egg', # https://graphviz.gitlab.io/doc/info/shapes.html#polygon
                'style': 'solid', # https://graphviz.gitlab.io/doc/info/shapes.html#styles-for-nodes
                'color': 'darkgray', # https://graphviz.gitlab.io/doc/info/colors.html#x11
                'fontcolor': 'black', # https://graphviz.gitlab.io/doc/info/colors.html#x11
                'fontname': 'Times-Roman', # https://graphviz.gitlab.io/faq/font/#default-fonts-and-postscript-fonts
                }
        if choose_node_design == 'node_design_1':
            node_design = {
                'shape': 'trapezium', 
                'style': 'filled',
                'color': 'bisque2',
                'fontcolor': 'black',
                'fontname': 'Times-Roman',
                }

        self.digraph.attr(
            'node', 
            shape=node_design['shape'], 
            style=node_design['style'], 
            color=node_design['color'], 
            fontcolor=node_design['fontcolor'],
            fontname=node_design['fontname'],
            )
        
    def design_edge(self, choose_edge_design: str = 'edge_design_0'):
        if choose_edge_design == 'edge_design_0':
            edge_design = {
                'color': 'black', # https://graphviz.gitlab.io/doc/info/colors.html#x11
                'arrowhead': 'normal', # https://graphviz.gitlab.io/doc/info/arrows.html#primitive-shapes
                }
        if choose_edge_design == 'edge_design_1':
            edge_design = {
                'color': 'burlywood4',
                'arrowhead': 'diamond',
                }

        self.digraph.attr(
            'edge', 
            color=edge_design['color'], 
            arrowhead=edge_design['arrowhead']
            )

    def make_node(self, node_content: str = 'empty', choose_node_design: str = 'node_design_0'):
        self.design_node(choose_node_design)
        self.digraph.node(self.autolinebreak(node_content))

    def make_nodes(self, *args, choose_node_design: str = 'node_design_0'):
        for i in range(len(args)):
            self.make_node(node_content = args[i], choose_node_design = choose_node_design)

    def make_edge(self, start_node: str = 'empty', end_node: str = 'empty', choose_edge_design: str = 'edge_design_0'):
        self.design_edge(choose_edge_design)
        self.digraph.edge(self.autolinebreak(start_node), self.autolinebreak(end_node))

    def make_chain(self, *args, choose_edge_design: str = 'edge_design_0'):
        for i in range(len(args) - 1):
            self.make_edge(args[i], args[i + 1], choose_edge_design)

    def viz(self):
        self.digraph.render(directory=self.filepath, view=False)