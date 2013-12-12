
import DataParser
import parameters
import utils
import numpy as np

class IndependenceAnalyzer:

    def __init__(self, initial_state=None):
        if initial_state is not None:
            self.initial_state=initial_state
        else:
            self.initial_state=parameters.starting_state

        self.parser=DataParser.DataParser()


    def get_choices(self, subject):
        _, choices=self.parser.parsed_choices(subject, self.initial_state)
        return choices


    def G(self, subject):
        _, choices=self.parser.parsed_choices(subject, self.initial_state)
        if choices is not None:
            G, pvalue, dof=utils.G_independence(choices)
            return G, pvalue, dof
        else:
            return None


    def modal_play(self, subject):
        _, choices=self.parser.parsed_choices(subject, self.initial_state)
        #compute marginal distribution of choices and total amount of choices
        marginal=np.sum(choices,0)
        #total=np.sum(marginal)

        return utils.H(marginal)

        ### THIS DID NOT WORK! SHOULD INVERT MARGINAL <-> DELTA
        # #compute reference deltas. one for each possible choice:
        # deltas=[]
        # for i in range(len(marginal)):
        #     newdelta=np.zeros(len(marginal), dtype=int)
        #     newdelta[i]=total
        #     deltas.append(newdelta)
        #     print newdelta

        # #compute G for each delta:
        # Gs=[utils.G(marginal, delta) for delta in deltas]
        
        # return min(Gs)


    def quantile_G(self, subject, nquantiles):
        choices=self.parser.quantile_parsed_choices(subject, self.initial_state, nquantiles)
        if choices is not None:
            G, pvalue, dof=utils.G_independence(choices)
            return G, pvalue, dof
        else:
            return None


    def multistate_G(self, subject, initial_states):
        _, choices=self.parser.parsed_choices_correct(subject, initial_states)
        if choices is not None:
            G, pvalue, dof=utils.G_independence(choices)
            return G, pvalue, dof
        else:
            return None

