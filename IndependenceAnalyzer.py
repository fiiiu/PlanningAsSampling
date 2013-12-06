
import DataParser
import parameters
import utils

class IndependenceAnalyzer:

    def __init__(self, initial_state=None):
        if initial_state is not None:
            self.initial_state=initial_state
        else:
            self.initial_state=parameters.starting_state

        self.parser=DataParser.DataParser()


    def G(self, subject):
        _, choices=self.parser.parsed_choices(subject, self.initial_state)
        G, pvalue, dof=utils.G_independence(choices)
        return G, pvalue, dof

