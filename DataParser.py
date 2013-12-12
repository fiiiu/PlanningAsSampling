

import HouseWorld
import HouseWorldData
import parameters
import numpy as np

class DataParser:

    def __init__(self):

        self.world=HouseWorld.HouseWorld()
        self.data=HouseWorldData.HouseWorldData()
        self.data.load()
        
    def parsed_choices(self, subject_id, initial_state):
        """
        Parses subject choices by day.
        """
        dates, moves=self.data.select_actions(initial_state, subjects=[subject_id], filter_correct=False)
        if len(dates)>0:
            days, move_choices=self.parse_in_days(dates, moves, initial_state, surrogate=False)
            return days, move_choices
        else:
            print "No dates/moves selected, can't parse."
            return None, None

    def parse_in_days(self, dates, moves, initial_state, surrogate=False):

        """
        Takes a list of dates and a list of chosen moves
        and parses them in a list of DAYS and moves.
        that is, groups moves according to day.

        Args:
            dates: list of dates.
            moves: list of moves.
            surrogate: whether to shuffle date/move correspondence.
        Returns:
            days: list of days in which moves were parsed.
            move_choices: list of distributions of moves for each day.

        """

        if len(dates)==0:
            print "No selected dates"
            return

        #This is cumbersome. Fix with HouseWorld
        all_moves=[self.world.action_descriptions[action]
         for action in self.world.legal_actions(self.world.state_id(str(initial_state)))]

        different_moves=len(all_moves)
        earliest_date=min(dates)
        counter=-1
        days=[]
        move_choices=[]
        
        if surrogate:
            random.shuffle(moves)
        
        for ind, date in enumerate(dates):
            interval=(date.date()-earliest_date.date())
            if interval not in days:
                counter+=1
                days.append(interval)
                move_choices.append([0 for i in range(len(all_moves))])
            choice=all_moves.index(moves[ind])
            move_choices[counter][choice]+=1
           
        return days, move_choices



    def play_distribution(self, initial_state):
        """
        
        """
        total_events=np.zeros(len(self.data.get_subjects()), dtype=int)
        session_amount=np.zeros(len(self.data.get_subjects()), dtype=int)
        for index,subject_id in enumerate(self.data.get_subjects()):
            dates, moves=self.data.select_actions(initial_state, subjects=[subject_id], filter_correct=False)
            total_events[index]=len(dates)
            session_amount[index]=len(set(dates))

        return total_events, session_amount



    def parse_by_quantiles(self, dates, moves, initial_state, nquantiles):
        """
        Takes a list of dates and a list of chosen moves
        and parses them according to date in quantiles.
        that is, groups moves according to their nquantiles quantiles.

        Args:
            dates: list of dates.
            moves: list of moves.
        Returns:
            move_choices: length nquantiles list of distributions of moves for quantiles.
        """

        if len(dates)==0:
            print "No selected dates"
            return

        #This is cumbersome. Fix with HouseWorld
        all_moves=[self.world.action_descriptions[action]
         for action in self.world.legal_actions(self.world.state_id(str(initial_state)))]

        different_moves=len(all_moves)
        earliest_date=min(dates)
        counter=-1
        days=[]
        move_choices=[[0 for i in range(len(all_moves))] for i in range(nquantiles)]
                
        for ind, date in enumerate(dates):
            choice=all_moves.index(moves[ind])
            move_choices[ind*nquantiles/len(dates)][choice]+=1
            
        return move_choices


    def quantile_parsed_choices(self, subject_id, initial_state, nquantiles):
        """
        Parses subject choices by quantiles.
        """
        dates, moves=self.data.select_actions(initial_state, subjects=[subject_id], filter_correct=False)
        if len(dates)>0:
            move_choices=self.parse_by_quantiles(dates, moves, initial_state, nquantiles)
            return move_choices
        else:
            print "No dates/moves selected, can't parse."
            return None



    def check_sessions(self):
        """
        Checks whether sessions == days, that is whether any kid plays different sessions on the same day.
        """
        total=[]
        subjects=self.data.get_subjects()
        for subject in subjects:
            dates, moves=self.data.select_actions(parameters.starting_state, subjects=[subject], filter_correct=False)
            for i in range(1,len(dates)):
                delta=dates[i]-dates[i-1]
                if delta.days==0 and delta.seconds>0:
                    print 'double play found for subject {0} on day {1}'.format(subject, dates[i])
                    total.append((subject, dates[i], delta.seconds))

        return total


         
    def parse_in_days_correct(self, dates, moves, initial_state, surrogate=False):

        """
        Takes a list of dates and a list of chosen moves
        and parses them in a list of DAYS and moves.
        that is, groups moves according to day.

        Args:
            dates: list of dates.
            moves: list of moves.
            surrogate: whether to shuffle date/move correspondence.
        Returns:
            days: list of days in which moves were parsed.
            move_choices: list of distributions of moves for each day.

        """

        if len(dates)==0:
            print "No selected dates"
            return

        #This is cumbersome. Fix with HouseWorld
        #all_moves=[self.world.action_descriptions[action]
        # for action in self.world.legal_actions(self.world.state_id(str(initial_state)))]

        #use correct/incorrect parsing
        all_moves=[True, False]

        different_moves=len(all_moves)
        earliest_date=min(dates)
        counter=-1
        days=[]
        move_choices=[]
        
        if surrogate:
            random.shuffle(moves)
        
        for ind, date in enumerate(dates):
            interval=(date.date()-earliest_date.date())
            if interval not in days:
                counter+=1
                days.append(interval)
                move_choices.append([0 for i in range(len(all_moves))])
            print initial_state, moves[ind]
            choice=all_moves.index(self.world.action_correct(initial_state, moves[ind]))

            move_choices[counter][choice]+=1
           
        return days, move_choices


    def parsed_choices_correct(self, subject_id, initial_states):
        """
        Parses subject choices by day.
        """
        days=[]
        move_choices=[]
        for state in initial_states:
            dates, moves=self.data.select_actions(state, subjects=[subject_id], filter_correct=False)
            if len(dates)>0:
                these_days, these_move_choices=self.parse_in_days_correct(dates, moves, state, surrogate=False)
                days.extend(these_days)
                move_choices.extend(these_move_choices)
                print days, moves

        return days, move_choices

