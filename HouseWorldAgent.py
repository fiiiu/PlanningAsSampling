
import HouseWorld
import parameters
import numpy as np

class HouseWorldAgent():

    """
    Agent for the HouseWorld.
    knows world he lives in. 
    """
    
    def __init__(self, world, params=None):
        
        self.world=world
        
        if params is not None:
            self.set_parameters(params)
        else:
            self.inertia=parameters.inertia
            self.gamma=parameters.gamma
            self.eta=parameters.eta
            self.kind=parameters.agent_kind
            
        self.previous_state=-1
        self.current_state=-1
        self.have_crossed=False
        
        if parameters.verbose:
            print(str.format("Agent {0} initialized with parameters: {1}, {2}, {3}", self.kind,\
                    self.gamma, self.inertia, self.eta))
        
    def set_parameters(self, params):
        self.gamma=params[0]
        self.inertia=params[1]
        self.eta=params[2]
        self.kind=params[3]
        
    def set_start(self, state):
        self.previous_state=state
        self.current_state=state
        self.have_crossed=False
        
    def move(self, action):
        new_state=self.world.next_state(self.current_state, action)
        if new_state != -1:
            self.previous_state=self.current_state
            self.current_state=new_state
            if self.kind=='single_crosser':
                if self.world.action_type(action)=='crossing':
                    self.have_crossed=True
                    
    def choose_action(self):
        """
        Choose action by sampling according to value
        """
        #actual_value=self.world.value(self.current_state)
        actions=self.world.legal_actions(self.current_state)
        values=[self.valuate_action(act) for act in actions]
        #values=[max(self.world.value(self.world.next_state(self.current_state, act))\
        #            -self.inertia*float(self.world.next_state(self.current_state, act)\
        #            ==self.previous_state),0) for act in actions]
                    
        if sum(values)>0:            
            probs=[value/sum(values) for value in values]
        else:
            probs=[1./len(values) for value in values]
            
        if parameters.verbose:
            print probs
        action_to_perform=actions[list(np.random.multinomial(1,probs)).index(1)]
        return action_to_perform
        
        
    def valuate_action(self, action):
        """
        Valuates actions according to agent kind:
        'distancer': discounted function of true distance to goal
        'inertial': as distancer, but downvalueing actions towards previous state
        'crosser': as distancer, but preferring permutations to circulations
        'wise': inertial+crosser. wisest around.
        'single_crosser': inertial, preferring crossing ONCE.
        'heuristic': incorporates heuristic misplaced, not counting the hole. no inertia.
        'heuristic_inertia': same as heuristic, incorporating inertia.
        """
        
        next_state=self.world.next_state(self.current_state, action)
        
        if self.kind == 'distancer':
            value=self.gamma**self.world.distance_to_goal(next_state)
        
        elif self.kind == 'inertial':
            value=max(
                    self.gamma**self.world.distance_to_goal(next_state)-\
                    self.inertia*float(next_state==self.previous_state)\
                    ,0)
            
        elif self.kind == 'crosser':
            value=self.gamma**self.world.distance_to_goal(next_state)+\
                    self.eta*float(self.world.action_type(action)=='crossing')
        
        elif self.kind == 'wise':
            value=max(
                    self.gamma**self.world.distance_to_goal(next_state)-\
                    self.inertia*float(next_state==self.previous_state)+\
                    self.eta*float(self.world.action_type(action)=='crossing')\
                    ,0)
        
        elif self.kind == 'single_crosser': 
            value=max(
                    self.gamma**self.world.distance_to_goal(next_state)-\
                    self.inertia*float(next_state==self.previous_state)+\
                    self.eta*float(self.world.action_type(action)=='crossing' and\
                    self.have_crossed is False)\
                    ,0)
                    
        elif self.kind == 'heuristic':
            value=max(
                    self.gamma**(self.eta*self.world.distance_to_goal(next_state)+\
                    (1-self.eta)*self.world.misplaced[next_state]),\
                    0)
            
        elif self.kind == 'heuristic_inertial':
            value=max(
                    self.gamma**(self.eta*self.world.distance_to_goal(next_state)+\
                    (1-self.eta)*self.world.misplaced[next_state])-\
                    self.inertia*float(next_state==self.previous_state),\
                    0)
            
        
        
        return value
    
