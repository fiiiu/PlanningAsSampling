
import HouseWorld
import HouseWorldAgent
import parameters
import random

class HouseWorldSimulation():
        
    def __init__(self, params=None):
        
        self.world=HouseWorld.HouseWorld()
        self.agent=HouseWorldAgent.HouseWorldAgent(self.world, params)
        
        self.current_trial=0
        
        self.world.generate_transition_matrix()
        
        
    def simulate_move(self):
        
        action=self.agent.choose_action()
        if parameters.verbose:
            print(self.agent.current_state)
            print(action,self.world.action_type(action))
        self.agent.move(action)
        
        
    def simulate_trial(self, initial_state=parameters.initial_state):
            
        if 0 <= initial_state < 24:
            self.agent.set_start(initial_state)
        else:
            return
            
        n_steps=0
        while self.agent.current_state != 0 and n_steps<10:
          self.simulate_move()
          n_steps+=1
        
        return n_steps 


    def simulate(self, initial_states=parameters.initial_state):
        
        if type(initial_states)!=list:
            initial_states=[initial_states]
        
        for initial_state in initial_states:
            self.current_trial+=1
            n_steps=self.simulate_trial(initial_state)
            print str.format("Trial {0}, {1} steps performed", self.current_trial, n_steps)
            


    def simulate_performance(self):
        """
        Simlates performance curve.
        Perfo vs distance of starting state. 
        """
        perfos=[0,0,0,0,0,0]
        realizations=[0,0,0,0,0,0]
            
        for trial in range(parameters.trial_amount):
            initial_state=random.choice(range(20))+4 #choose among all but goal state and states at distance 1 from goal
            steps=self.simulate_trial(initial_state)
            distance=self.world.distance_to_goal(initial_state)
            realizations[distance-2]+=1
            
            if steps==distance:
                perfos[distance-2]+=1
            
        perf=[float(p)/realizations[i] for i,p in enumerate(perfos) if realizations[i]>0]    
        
        return realizations, perf
