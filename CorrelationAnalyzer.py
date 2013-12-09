
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
        self.modalplay=np.zeros(len(self.data.get_subjects()), dtype=float)


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
        

    def modal_hist(self):
        plt.hist(self.modalplay)
        plt.show()


    def explore_modalplay(self):
        for index, subject in enumerate(self.data.get_subjects()):
            if self.modalplay[index] > 1.3:
                choices=np.sum(self.independence.get_choices(subject),0)
                print 'subject {0}, H={1}, choices={5}, G={2}, Age={3}, Sex={4}'.format(subject, self.modalplay[index],
                    self.G[index], self.age[index], self.sex[index], choices)

