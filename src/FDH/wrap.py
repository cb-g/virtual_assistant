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
        """
        style docs:
        https://graphviz.gitlab.io/doc/info/shapes.html
        https://graphviz.gitlab.io/doc/info/colors.html
        https://graphviz.gitlab.io/doc/info/attrs.html
        https://graphviz.gitlab.io/doc/info/arrows.html
        """
        if choose_node_design == 'node_design_0':
            node_design = {
                'shape': 'box', 
                'style': 'solid',
                'color': 'darkgray',
                'fontcolor': 'black',
                }
        if choose_node_design == 'node_design_1':
            node_design = {
                'shape': 'box', 
                'style': 'filled',
                'color': 'lightgray',
                'fontcolor': 'black',
                }

        self.digraph.attr(
            'node', 
            shape=node_design['shape'], 
            style=node_design['style'], 
            color=node_design['color'], 
            fontcolor=node_design['fontcolor']
            )

    def make_node(self, choose_node_design: str = 'node_design_0', node_content: str = 'empty'):
        self.design_node(choose_node_design)
        self.digraph.node(self.autolinebreak(node_content))

    def make_edge(self, start_node: str, end_node: str):
        self.digraph.edge(self.autolinebreak(start_node), self.autolinebreak(end_node))

    def viz(self):
        self.digraph.render(directory=self.filepath, view=False)