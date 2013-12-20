
import HouseWorldData
import IndependenceAnalyzer
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import parameters

class CorrelationAnalyzer:

    """
    Class for analyzing correlations between sample independence measures in House World and Demographics/CBQ
    """
    def __init__(self):

        self.data=HouseWorldData.HouseWorldData()
        self.data.load()
        self.independence=IndependenceAnalyzer.IndependenceAnalyzer()


    def compute(self):

        self.G=np.zeros(len(self.data.get_subjects()), dtype=float)
        self.age=np.zeros(len(self.data.get_subjects()), dtype=int)
        self.sex=np.zeros(len(self.data.get_subjects()), dtype=bool)
        self.surgency=np.zeros(len(self.data.get_subjects()), dtype=int)
        self.naffect=np.zeros(len(self.data.get_subjects()), dtype=int)
        self.effcontrol=np.zeros(len(self.data.get_subjects()), dtype=int)
        self.modalplay=np.zeros(len(self.data.get_subjects()), dtype=float)
        self.phi=np.zeros(len(self.data.get_subjects()), dtype=float)
        self.phi_p=np.zeros(len(self.data.get_subjects()), dtype=float)
        self.alt_G=np.zeros(len(self.data.get_subjects()), dtype=float)
        self.alt_p=np.zeros(len(self.data.get_subjects()), dtype=float)
        self.alt_dof=np.zeros(len(self.data.get_subjects()), dtype=float)
        self.perfo=np.zeros(len(self.data.get_subjects()), dtype=float)
        self.state_perfo=np.zeros(len(self.data.get_subjects()), dtype=float)

        for index, subject in enumerate(self.data.get_subjects()):
            self.age[index]=self.data.get_age(subject).as_number()
            self.sex[index]=self.data.get_sex(subject, boolean=True)
            self.G[index]=self.independence.G(subject)[0]
            surgency, naffect, effcontrol=self.data.get_scores(subject)
            self.modalplay[index]=self.independence.modal_play(subject)

            self.surgency[index]=surgency
            self.naffect[index]=naffect
            if not np.isnan(effcontrol):
                self.effcontrol[index]=effcontrol

            self.phi[index], self.phi_p[index], self.alt_G[index], self.alt_p[index], self.alt_dof[index]=\
            self.independence.kid_alternance(subject)
            self.perfo[index]=self.data.get_performance(subject)
            self.state_perfo[index]=self.data.get_performance(subject, parameters.starting_state)


  
    def filter_oldie(self):
        ind=self.age==116
        self.G[ind]=0
        self.age[ind]=0


    def G_vs_age(self):
        plt.plot(self.age, self.G, 'o')
        plt.xlim([75, 90])
        plt.show()


    def G_vs_grade(self):
        young=self.G[self.age<82]
        old=self.G[self.age>=82]
        plt.bar([0,1],[np.mean(young), np.mean(old)])
        plt.show()


    def G_vs_sex(self):
        boys=self.G[self.sex]
        girls=self.G[-self.sex]
        plt.bar([0,1],[np.mean(girls), np.mean(boys)])
        plt.show()


    def G_vs_surgency(self):
        #plt.plot(self.G, self.surgency, 'o')
        #plt.show()
        x=self.G[np.isfinite(self.G) & (self.surgency > 0)]
        y=self.surgency[np.isfinite(self.G) & (self.surgency > 0)]
        self.plot_and_correlate(x,y)


    def G_vs_naffect(self):
        plt.plot(self.G, self.naffect, 'o')
        plt.ylim([20,50])
        plt.show()
            
    def G_vs_effcontrol(self):
        plt.plot(self.G, self.effcontrol, 'o')
        plt.ylim([20,55])
        plt.show()
        

    def modal_hist(self):
        plt.hist(self.modalplay)
        plt.show()


    def explore_modalplay(self):
        for index, subject in enumerate(self.data.get_subjects()):
            if self.modalplay[index] > 1.3:
                choices=np.sum(self.independence.get_choices(subject),0)
                print 'subject {0}, H={1}, choices={5}, G={2}, Age={3}, Sex={4}'.format(subject, self.modalplay[index],
                    self.G[index], self.age[index], self.sex[index], choices)


    def alt_vs_age(self, phi=False):
        if not phi:
            x=self.age[np.isfinite(self.alt_G) & (self.age<100)]
            y=self.alt_G[np.isfinite(self.alt_G)& (self.age<100)]
        else:
            #or use phi:       
            x=self.age[np.isfinite(self.phi)& (self.age<100)]
            y=self.phi[np.isfinite(self.phi)& (self.age<100)]
        
        self.plot_and_correlate(x,y)



    def alt_vs_sex(self):
        boys=self.alt_G[self.sex]
        girls=self.alt_G[-self.sex]
        
        #use this instead for phi measure
        #boys=self.phi[np.isfinite(self.phi) & self.sex]
        #girls=self.phi[np.isfinite(self.phi) & -self.sex]

        ttest=stats.ttest_ind(boys, girls)
        print "boys/girls t:{0}, p:{1}".format(ttest[0],ttest[1])

        plt.bar([0,1],[np.mean(girls), np.mean(boys)])
        plt.show()
        plt.bar


    def alt_vs_surgency(self, phi=False):
        
        if not phi:
            x=self.alt_G[np.isfinite(self.alt_G) & (self.surgency > 0)]
            y=self.surgency[np.isfinite(self.alt_G) & (self.surgency > 0)]
        else:
            #or use phi:       
            x=self.phi[np.isfinite(self.phi) & (self.surgency > 0)]
            y=self.surgency[np.isfinite(self.phi) & (self.surgency > 0)]
        
        self.plot_and_correlate(x,y)


    def alt_vs_naffect(self, phi=False):
        if not phi:
            x=self.alt_G[np.isfinite(self.alt_G) & (self.naffect > 0)]
            y=self.naffect[np.isfinite(self.alt_G) & (self.naffect > 0)]
        else:
            #or
            x=self.phi[np.isfinite(self.phi) & (self.naffect > 0)]
            y=self.naffect[np.isfinite(self.phi) & (self.naffect > 0)]
        
        self.plot_and_correlate(x,y)
            
    def alt_vs_effcontrol(self, phi=False):
        if not phi:
            x=self.alt_G[np.isfinite(self.alt_G) & (self.effcontrol > 0)]
            y=self.effcontrol[np.isfinite(self.alt_G) & (self.effcontrol > 0)]
        else:
            #or
            x=self.phi[np.isfinite(self.phi) & (self.effcontrol > 0)]
            y=self.effcontrol[np.isfinite(self.phi) & (self.effcontrol > 0)]
        
        self.plot_and_correlate(x,y)


    def plot_and_correlate(self, x, y):
        rtest=stats.pearsonr(x, y)
        print "correlation r:{0}, p:{1}".format(rtest[0],rtest[1])
        plt.plot(x, y, 'o')
        plt.show()


    def phi_hist(self):
        print "one sample t-test for mean different from 0, p={0}".format(stats.ttest_1samp(self.phi[np.isfinite(self.phi)], 0))
        plt.hist(self.phi[np.isfinite(self.phi)])
        plt.show()

    def phi_ps(self):
        print self.phi_p
        print np.median(self.phi_p)
        plt.hist(self.phi_p[np.isfinite(self.phi_p)])
        plt.show()

    def phi_vs_phip(self):
        x=self.phi[np.isfinite(self.phi)]
        y=self.phi_p[np.isfinite(self.phi)]
    
        self.plot_and_correlate(x,y)

    def phi_vs_perfo(self):
        x=self.phi[np.isfinite(self.phi)]
        y=self.perfo[np.isfinite(self.phi)]
        self.plot_and_correlate(x,y)

    def phi_vs_stateperfo(self):
        x=self.phi[np.isfinite(self.phi)]
        y=self.state_perfo[np.isfinite(self.phi)]
        self.plot_and_correlate(x,y)


    
