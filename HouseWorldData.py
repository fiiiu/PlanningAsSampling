
import HouseWorld
import HouseWorldTrial
import DemographicData
import CBQData
import parameters

import datetime
import scipy.io
import platform


class HouseWorldData:

    __shared_state = {}
    
    def __init__(self):
        self.__dict__ = self.__shared_state
        
        self.house_world=HouseWorld.HouseWorld()
        self.data_directory=parameters.data_directory
        self.data_filename=parameters.data_filename

        #self.demographic_filename=parameters.demographic_filename
        self.demographic_data=DemographicData.DemographicData()
        self.cbq_data=CBQData.CBQData()

        self.subject_ids=[]
        self.dates=[]
        self.successes=[]
        self.min_movess=[]
        self.n_movess=[]
        self.initial_states=[]
        self.statess=[]
        self.movess=[]
        
        self.trial_amount=0
        self.datadict={}
        self.data_loaded=False


    def load(self, filename=None):

        if self.data_loaded:
            return

        #load game data
        if filename is None:
            filename=self.data_directory+self.data_filename
        data=scipy.io.loadmat(filename)
        #iterate. data is in key 'dat'.
        self.trial_amount=len(data['dat'][0])
        for trial in range(self.trial_amount):
            subject_id=data['dat'][0,trial][0][0]
            date=datetime.datetime.strptime(data['dat'][0,trial][1][0],'%d-%b-%Y %X')
            #success=data['dat'][0,trial][2][0,0]
            min_moves=data['dat'][0,trial][3][0,0]
            n_moves=data['dat'][0,trial][4][0,0]
            initial_state=data['dat'][0,trial][5][0,0][0][0,0]
            states=data['dat'][0,trial][5][0,0][0]
            moves=data['dat'][0,trial][5][0,0][1]
            
            success=int(states[-1]==[1230] and n_moves==min_moves)
            
            self.subject_ids.append(subject_id)
            self.dates.append(date)
            self.successes.append(success)
            self.min_movess.append(min_moves)
            self.n_movess.append(n_moves)
            self.initial_states.append(initial_state)
            self.statess.append(states)
            self.movess.append(moves)

            trial=HouseWorldTrial.HouseWorldTrial(subject_id, date, success, min_moves, n_moves, initial_state, states, moves)

            if subject_id in self.datadict.keys():
                self.datadict[subject_id][3].append(trial)
            else:
                self.datadict[subject_id]=[0,0,0,[trial]]

        #load demographics
        self.demographic_data.load()

        #load CBQ
        self.cbq_data.load()

        #maybe i don't need this.. 
        for subject in self.demographic_data.get_subjects():
            self.datadict[subject][0]=self.demographic_data.get_sex(subject)
            self.datadict[subject][1]=self.demographic_data.get_age(subject)
        for subect in self.cbq_data.get_subjects():
            self.datadict[subject][2]=self.cbq_data.get_scores(subject)

        self.data_loaded=True


    def get_age(self, subject):
        return self.demographic_data.get_age(subject)

    def get_sex(self, subject, boolean=False):
        return self.demographic_data.get_sex(subject, boolean)

    def get_scores(self, subject):
        return self.cbq_data.get_scores(subject)
        
         
    def select_actions(self, initial_state, subjects=None, filter_correct=False):

        """
        Selects action for given initial state and subjects, possibly filtering successful trials.

        Args:
            initial_state: initial state.
            subjects (list): subjects to include.
            filter_correct (bool): whether to filter for successful trials.
        Returns:
            dates (list): list of selected dates.
            moves (list): list of selected moves.
        """
     
        dates=[]
        moves=[]
        
        if subjects is None:
            subjects=set(self.subject_ids)
        
        for trial in range(self.trial_amount):
            if self.subject_ids[trial] in subjects and\
             self.initial_states[trial]==initial_state:
                if filter_correct:
                    if self.successes[trial]==1:
                        dates.append(self.dates[trial])
                        moves.append(tuple(self.movess[trial][0]))
                else:
                    dates.append(self.dates[trial])
                    moves.append(tuple(self.movess[trial][0]))

        return dates, moves
            

    
    def get_subjects(self):
        
        return list(set(self.subject_ids))
                
                

