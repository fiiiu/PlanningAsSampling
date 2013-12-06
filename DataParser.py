

import HouseWorld
import HouseWorldData
import parameters

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
            return -1, -1

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



