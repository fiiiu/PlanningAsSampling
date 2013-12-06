
import parameters
import numpy as np

class HouseWorld:
  
  """
  Class describing the World.
  Provides a common language for analysis.
  (Should be a Singleton, not implemented)
  """
    
  def __init__(self):
    
    self.state_descriptions = [[1,2,3,0],[0,2,3,1],[1,0,3,2],[1,2,0,3],
      [0,1,3,2],[0,2,1,3],[2,0,3,1],[3,2,0,1],[2,0,1,3],[2,1,3,0],
      [3,1,0,2],[3,2,1,0],[2,1,0,3],[2,3,1,0],[3,0,1,2],
      [3,1,2,0],[0,1,2,3],[0,3,1,2],[2,3,0,1],[3,0,2,1],
      [0,3,2,1],[1,0,2,3],[1,3,0,2],[1,3,2,0]]

    self.state_names = [('1230', '0231', '1032', '1203', 
      '0132', '0213', '2031', '3201', '2013', '2130',
      '3102', '3210', '2103', '2310', '3012',
      '3120', '0123', '0312', '2301', '3021',
      '0321', '1023', '1302', '1320')]
    
    self.distances = [0,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5,6,6,6,7]
    self.misplaced = [0,1,1,1,2,2,2,2,3,2,3,2,3,3,3,3,3,3,3,3,3,2,2,2]
    
    self.action_descriptions = [(1,2),(1,3),(1,4),(2,1),(2,4),(3,1),(3,4),(4,1),(4,2),(4,3)]
    
    self.generate_transition_matrix()
    
      
  def distance_to_goal(self, state):
    return self.distances[state]
    
  
  def action_id(self, action):
    """ Returns action ID """
    #if type(action) is tuple and action in self.action_names:
    #  action_id=self.action_names.index(action)
    if type(action) is tuple and action in self.action_descriptions:
      action_id=self.action_descriptions.index(action)
    elif type(action) is int and 0 <= action < 10:
      action_id=action
    else:
      action_id=-1
    return action_id
    
  
  def state_id(self, state):
    """ Returns state ID """
    if type(state) is str and state in self.state_names:
      state_id=self.state_names.index(state)
    elif type(state) is list and state in self.state_descriptions:
      state_id=self.state_descriptions.index(state)
    elif type(state) is int and 0 <= state < 10:
      state_id=state
    else:
      state_id=-1
    return state_id
    
      


  def action_type(self, action):
    """ Returns action type. Whether good or bad depends on action """
    action_id=self.action_id(action)
    if action_id in [2,7]:
      return 'crossing'
    elif action_id in [0,4,5,9]:
      return 'clockwise'
    elif action_id in [1,3,6,8]:
      return 'counterclockwise'
    
    
  def legal_actions(self, state):
    """ Return list of actions that can be performed in a given state"""
    return [ind for ind, act in enumerate(self.transition_matrix) if act[state] != -1]
    
        
  def generate_transition_matrix(self):
    self.transition_matrix=[[0 for x in range(len(self.state_descriptions))] for x in range(len(self.action_descriptions))]
    for action_id,action in enumerate(self.action_descriptions):
      for state_id,state in enumerate(self.state_descriptions):
          pick=action[0]
          drop=action[1]
          new_state=[i for i in state]
          new_state[drop-1]=state[pick-1]
          new_state[pick-1]=0
          if new_state in self.state_descriptions:
            transition=self.state_descriptions.index(new_state)
          else:
            transition=-1
          self.transition_matrix[action_id][state_id]=transition
          

  def next_state(self, state, action):
    """ Compute next state. Accepts both descriptions and indices for actions """
    action_id=self.action_id(action)
    if action_id != -1:
      return self.transition_matrix[action_id][state]
    else:
      return -1
      
      
    
    
    
    
    ####################
    #
    # OLD CODE BELOW,
    # now split in HouseWorld, HouseWorldAgent & HouseWorldSimulation classes
    #
    #
    
    #~ 
  #~ def value(self, state):
    #~ return parameters.gamma**self.distance_to_goal(state)
      #~ 
    
    #~ 
  #~ def simulate_trial(self, initial_state):
    #~ if 0 <= initial_state < 24:
      #~ self.current_state=initial_state
    #~ else:
      #~ return
    #~ steps=0
    #~ #print self.current_state
    #~ while self.current_state != 0 and steps<10:
      #~ self.simulate_move()
      #~ steps+=1
      #~ #print self.current_state
    #~ 
    #~ #print "number of steps: " + str(steps)
    #~ return steps 
      #~ 
      
      
        #~ def move(self, action):
    #~ new_state=self.next_state(action)
    #~ if new_state != -1:
      #~ self.previous_state=self.current_state
      #~ self.current_state=new_state  
    #~ else:
      #~ pass
      #~ #print "illegal move"
      
      
      #~ 
  #~ def simulate_move(self):
    #~ #simulate move by sampling according to value
    #~ actual_value=self.value(self.current_state)
    #~ actions=self.legal_actions(self.current_state)
    #~ 
    #~ # I could use this for perfo?
    #~ # if inertia:
      #~ # values=[self.value(self.next_state(act))-self.inertia*int(self.next_state(act)==self.previous_state)
            #~ #for act in actions]
    #~ # else:
      #~ # values=[self.value(self.next_state(act)) for act in actions]
    #~ 
    #~ values=[max(self.value(self.next_state(act))-self.inertia*float(self.next_state(act)==self.previous_state),0)
            #~ for act in actions]
    #~ probs=[value/sum(values) for value in values]
    #~ 
    #~ #print probs
      #~ 
    #~ #print "actions: " + str(actions) + " with probabilities: " + str(probs)
    #~ action_to_perform=actions[list(np.random.multinomial(1,probs)).index(1)]
    #~ #print "performing: " + str(action_to_perform)
    #~ self.move(action_to_perform)
    #~ 
    
    
    
    
