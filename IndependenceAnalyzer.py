
import DataParser
import parameters
import utils
import numpy as np
from scipy import stats

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
            return None, None, None


    def modal_play(self, subject):
        _, choices=self.parser.parsed_choices(subject, self.initial_state)
        #compute marginal distribution of choices and total amount of choices
        if choices is not None:
            marginal=np.sum(choices,0)
            return utils.H(marginal)
        else:
            return None

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


    def markov_intraday(self, consecutives=False):
        all_choices=[self.parser.world.action_descriptions[action]
         for action in self.parser.world.legal_actions(self.initial_state)]
        nchoices=len(all_choices)
        table=np.zeros((nchoices, nchoices))

        for subject in self.parser.data.get_subjects():
            days, move_choices=self.parser.intraday_choices(subject, self.initial_state, filter_consecutives=consecutives)
            if move_choices is not None:
                for daily_moves in move_choices:
                    for move_pair in zip(daily_moves, daily_moves[1:]):
                        rowind=all_choices.index(move_pair[0])
                        colind=all_choices.index(move_pair[1])
                        table[rowind, colind]+=1

        return table, utils.G_independence(table)


    def alternance_analysis(self, consecutives=False):
        all_choices=[self.parser.world.action_descriptions[action]
         for action in self.parser.world.legal_actions(self.initial_state)]
        nchoices=len(all_choices)
        table=np.zeros((2, 2))
        subjects=self.parser.data.get_subjects()
        G=np.zeros(len(subjects))
        pval=np.zeros(len(subjects))
        dof=np.zeros(len(subjects))
        
        for ind, subject in enumerate(subjects):
            days, move_choices=self.parser.intraday_choices(subject, self.initial_state, filter_consecutives=consecutives)
            if move_choices is not None:
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
                
                #stats=utils.G_independence(np.array([actual_p, independent_p]))
                #use goodness of fit instead of independence
                results=utils.G_goodness_of_fit(actual_p, independent_p)

                G[ind],pval[ind],dof[ind]=results
                table+=np.array([actual_p, independent_p])

        #global statistics
        #Gt,pt,doft=utils.G_independence(table)
        Gt=sum(G)
        doft=sum(dof)
        pvalt=1-stats.chi2.cdf(Gt,doft)
        return table, (Gt,pvalt,doft), (G, pval, dof)


    def kid_alternance(self, subject):
        all_choices=[self.parser.world.action_descriptions[action]
         for action in self.parser.world.legal_actions(self.initial_state)]
        
        nchoices=len(all_choices)

        days, move_choices=self.parser.intraday_choices(subject, self.initial_state)
        #compute marginal
        kid_marginal=np.zeros(nchoices)
        if move_choices is not None:
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
            
            #use goodness of fit!
            #G, pval, dof=utils.G_independence(np.array([actual_p, independent_p]))
            G, pval, dof=utils.G_goodness_of_fit(actual_p, independent_p)
            table=np.array([actual_p, independent_p])
            phi=table[0,0]/table[0,1]-table[1,0]/table[1,1]

            #surrogate for statistics on phi.
            #sample from binomial with n=data amount of choices, theta=independent ratio of one choice over total amount.
            n_samples=1000
            phi_MC=np.zeros(n_samples)
            if sum(actual_p)>0:  
                for i in range(n_samples):
                    RD=np.random.binomial(sum(actual_p), independent_p[1]/sum(independent_p))
                    AD=sum(actual_p)-RD
                    phi_MC[i]=float(RD)/AD-independent_p[0]/independent_p[1] 
            else:
                phi_MC[i]=0

            p_phi=float(sum(phi<np.abs(phi_MC)))/n_samples
            return phi, p_phi, G, pval, dof
        
        else:
            return None, None, None, None, None
            