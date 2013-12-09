import DataParser
import parameters
import utils
import numpy as np
import matplotlib.pyplot as plt

class PlayDistributionAnalyzer:

    def __init__(self, initial_state=None):
        if initial_state is not None:
            self.initial_state=initial_state
        else:
            self.initial_state=parameters.starting_state

        self.parser=DataParser.DataParser()

        self.total_events, self.session_amount=self.parser.play_distribution(self.initial_state)


    def total_event_hist(self):
        plt.hist(self.total_events)
        plt.show()

    def session_amount_hist(self):
        plt.hist(self.session_amount)
        plt.show()



