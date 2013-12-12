
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


    def markov_intraday(self):
        all_choices=[self.parser.world.action_descriptions[action]
         for action in self.parser.world.legal_actions(self.initial_state)]
        nchoices=len(all_choices)
        table=np.zeros((nchoices, nchoices))

        for subject in self.parser.data.get_subjects():
            days, move_choices=self.parser.intraday_choices(subject, self.initial_state)
            for daily_moves in move_choices:
                for move_pair in zip(daily_moves, daily_moves[1:]):
                    rowind=all_choices.index(move_pair[0])
                    colind=all_choices.index(move_pair[1])
                    table[rowind, colind]+=1

        return table, utils.G_independence(table)


    def alternance_analysis(self):
        all_choices=[self.parser.world.action_descriptions[action]
         for action in self.parser.world.legal_actions(self.initial_state)]
        nchoices=len(all_choices)
        table=np.zeros((2, 2))
        subjects=self.parser.data.get_subjects()
        G=np.zeros(len(subjects))
        pval=np.zeros(len(subjects))
        dof=np.zeros(len(subjects))
        
        for ind, subject in enumerate(subjects):
            days, move_choices=self.parser.intraday_choices(subject, self.initial_state)
            #compute marginal
            kid_marginal=np.zeros(nchoices)
            for daily_moves in move_choices:
                for move in daily_moves:
                    kid_marginal[all_choices.index(move)]+=1
            #normalize
            kid_marginal=kid_marginal/np.sum(kid_marginal)

            #compute repetitions
            kid_table=np.zeros((nchoices, nchoices))
            for daily_moves in move_choices:
                for move_pair in zip(daily_moves, daily_moves[1:]):
                    rowind=all_choices.index(move_pair[0])
                    colind=all_choices.index(move_pair[1])
                    kid_table[rowind, colind]+=1

            independent_p=np.zeros(2) #independent distribution. [0] is Repeat, [1] is Alternate.
            actual_p=np.zeros(2) #same from actual data. 
            for i in range(len(kid_marginal)):
                for j in range(len(kid_marginal)):
                    independent_p[i!=j]+=kid_marginal[i]*kid_marginal[j]
                    actual_p[i!=j]+=kid_table[i,j]
            
            #scale to data counts
            independent_p=independent_p*sum(actual_p)
            
            stats=utils.G_independence(np.array([actual_p, independent_p]))
            G[ind],pval[ind],dof[ind]=stats
            table+=np.array([actual_p, independent_p])

        #global statistics
        Gt,pt,doft=utils.G_independence(table)
        return table, (Gt,pt,doft), (G, pval, dof)

