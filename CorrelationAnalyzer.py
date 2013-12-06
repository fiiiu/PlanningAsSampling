
import HouseWorldData
import IndependenceAnalyzer
import matplotlib.pyplot as plt
import numpy as np

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


        for index, subject in enumerate(self.data.get_subjects()):
            self.age[index]=self.data.get_age(subject).as_number()
            self.sex[index]=self.data.get_sex(subject, boolean=True)
            self.G[index]=self.independence.G(subject)[0]
            surgency, naffect, effcontrol=self.data.get_scores(subject)

            self.surgency[index]=surgency
            self.naffect[index]=naffect
            if not np.isnan(effcontrol):
                self.effcontrol[index]=effcontrol



  
    def filter_oldie(self):
        ind=self.age.index(116)
        del self.G[ind]
        del self.age[ind]


    def G_vs_age(self):
        plt.plot(self.age, self.G, 'o')
        plt.show()


    def G_vs_sex(self):
        boys=self.G[self.sex]
        girls=self.G[-self.sex]
        plt.bar([0,1],[np.mean(girls), np.mean(boys)])
        plt.show()


    def G_vs_surgency(self):
        plt.plot(self.G, self.surgency, 'o')
        plt.show()

    def G_vs_naffect(self):
        plt.plot(self.G, self.naffect, 'o')
        plt.ylim([20,50])
        plt.show()
            
    def G_vs_effcontrol(self):
        plt.plot(self.G, self.effcontrol, 'o')
        plt.ylim([20,55])
        plt.show()
        

