
import HouseWorldData
import HouseWorld
import utils
import parameters
import numpy as np
import random
import datetime
from scipy import stats

def load_data():
    
    hwd=HouseWorldData.HouseWorldData()
    hwd.load_from_mat()
    return hwd


def parse_in_days(dates, moves, surrogate=False):

    """
    Takes a list of dates and a list of chosen moves
    and parses them in a list of DAYS and moves.
    that is, groups moves according to day.
    """

    #all_moves=list(set(moves))
    # bad, take common reference instead!
    hw=HouseWorld.HouseWorld()
    all_moves=[hw.action_descriptions[action] for action in hw.legal_actions(hw.state_id(str(parameters.starting_state)))]

    different_moves=len(all_moves)
    earliest_date=min(dates)
    counter=-1
    days=[]
    choices=[]
    
    if surrogate:
        random.shuffle(moves)
    
    for ind,date in enumerate(dates):
        
        interval=(date.date()-earliest_date.date())
        if interval not in days:
            counter+=1
            days.append(interval)
            choices.append([0 for i in range(len(all_moves))])
            
      
        choice=all_moves.index(moves[ind])
        choices[counter][choice]+=1
       
    #normalize?
    #choices=[[float(val)/sum(vec) for val in vec] for vec in choices]
    
    return days,choices
    
    

def compute_kullbacks(choices):
    
    """
    Compute Kullback Leibler divergences for all distributions of choices
    with respect to average distribution.
    choices: list of lists (choice distributions)
    returns: list (divergences)
    """
    
    #compute marginal distribution
    parent_distribution=sum(np.array(choices))
        
    kullbacks=[utils.kullback_leibler(choice, parent_distribution) for choice in choices]
    
    return kullbacks
    


def compute_mean_kullback(choices):
    
    """
    Compute mean Kullback Leibler divergence for all distributions of choices
    with respect to average distribution
    """
    return np.mean(compute_kullbacks(choices))
    
    
    

def subject_kullbacks(hwd, subjects=None):
    
    if subjects is None:
        subjects=set(hwd.subject_ids)
    
    kullbacks={}
    sub_choices={}
    
    for subject_id in subjects:
        dates,moves=hwd.select_actions(parameters.starting_state, subject_id, parameters.filter_correct)
        if dates==[]:
            continue
        days,choices=parse_in_days(dates,moves)
        if len(choices[0])>1:
            kullbacks[subject_id]=compute_mean_kullback(choices)
            sub_choices[subject_id]=choices
    
    return kullbacks, sub_choices
    
    
def surrogate_subject_kullbacks(hwd, subjects=None, n_realizations=parameters.n_realizations):
    
    if subjects is None:
        subjects=set(hwd.subject_ids)
    
    kullbacks={}
    
    for subject_id in subjects:
        kullbacks[subject_id]=[]
        dates,moves=hwd.select_actions(parameters.starting_state, subject_id, parameters.filter_correct)
        if dates==[]:
            continue
        for realization in range(n_realizations):
            days,choices=parse_in_days(dates,moves,surrogate=True)
            if len(choices[0])>1:
                kullbacks[subject_id].append(compute_mean_kullback(choices))
    
    return kullbacks
        
        
        
def subject_pvals(hwd, subjects=None, n_realizations=parameters.n_realizations):
    
    if subjects is None:
        subjects=set(hwd.subject_ids)
    
    kullbacks,_=subject_kullbacks(hwd, subjects)
    surrogate_kullbacks=surrogate_subject_kullbacks(hwd, subjects, n_realizations)
    
    pvalues={}
    for sub in kullbacks.keys():
        if len(set(surrogate_kullbacks[sub]))>1: #filter equal averages
            pvalues[sub]=float(sum(kullbacks[sub]<np.array(surrogate_kullbacks[sub])))/n_realizations
    
    return pvalues
    
    
    
def consecutive_ps(hwd, subjects=None):
    
    if subjects is None:
        subjects=set(hwd.subject_ids)
        
    consecutiveps=[]
    previous_move=[]
    
    for subject_id in subjects:
        dates,moves=hwd.select_actions(parameters.starting_state, \
                    subject_id, parameters.filter_correct)
 
        if dates==[]:
            continue
        earliest_date=min(dates)
    
        for ind,date in enumerate(dates):
            interval=(date-earliest_date).total_seconds()
            current_move=moves[ind] 
            if parameters.verbose:
                print str.format('previous move: {0}', previous_move)
                print str.format('current move: {0}', current_move)
            
            consecutiveps.append((interval, float(current_move==previous_move)))
            previous_move=current_move
            
    consecutiveps.pop(0)
    
    
    #consecutiveps=[(t,p) for (t,p) in consecutiveps if t<1e6]
    
    return consecutiveps
        

def split_todays(ps):
    
    one_day=datetime.timedelta(1).total_seconds()
    one_day=3600. #same HOUR!
    split_ps=[[],[]]
    split_aves=[0,0]
    
    for (t,p) in ps:
        split_ps[t > one_day].append(p)
        split_aves[t > one_day] += p
        
    #split_aves[0]=split_aves[0]/len(split_ps[0])
    split_aves=[split_aves[i]/len(split_ps[i]) for i in [0,1]]
    split_devs=[np.std(split_ps[i]) for i in [0,1]]
    
    return split_aves, split_devs, split_ps
        
        
                
        

def subject_Gs(hwd, subjects=None):
    
    if subjects is None:
        subjects=set(hwd.subject_ids)
    
    Gs={}
    ps={}
    sub_choices={}
    
    for subject_id in subjects:
        dates,moves=hwd.select_actions(parameters.starting_state, subject_id, parameters.filter_correct)
        if dates==[]:
            continue
        days,choices=parse_in_days(dates,moves)
        if len(choices[0])>1:
            Gs[subject_id],ps[subject_id],_=utils.G_independence(choices) #or Gh!
            sub_choices[subject_id]=choices
    
    return Gs, ps, sub_choices



def compute_Gh(choices):
    
    """
    Compute Gh for one subject, as sum of Gs for each choice distribution
    choices: list of lists (choice distributions)
    returns: Gh, pvalue
    """
    
    #compute marginal distribution
    parent_distribution=sum(np.array(choices))
    
    #Gh is sum of G's
    Gh=sum([utils.G(choice, parent_distribution) for choice in choices])
    #Gh is Chi-squared with #_of_choices-1 DoF. Or 2*#ofchoices-1?!? CHECK!
    dofs=sum([(len(choice)-1) for choice in choices])-1
    pvalue=1-stats.chi2.cdf(Gh, dofs) 

    return Gh, pvalue


    

def single_G(hwd, subjects=None):

    """
    Compute single G as sum of kid's Gs, and its p value.
    Distributed according to chi square with dof = sum of dofs.
    """

    if subjects is None:
        subjects=set(hwd.subject_ids)
    
    Gstat={}

    sub_choices={}
    
    for subject_id in subjects:
        dates,moves=hwd.select_actions(parameters.starting_state, subject_id, parameters.filter_correct)
        if dates==[]:
            continue
        days,choices=parse_in_days(dates,moves)
        if len(choices[0])>1:
            Gstat[subject_id]=utils.G_independence(choices)
            #Gs[subject_id],ps[subject_id], dof[subject_id]=utils.G_independence(choices)
            sub_choices[subject_id]=choices

    G=sum([value[0] for value in Gstat.values()])
    dof=sum([value[2] for value in Gstat.values()])
    p=1-stats.chi2.cdf(G,dof)
    
    #Fisher method
    ps=[value[1] for value in Gstat.values()]
    X2_F=-2*sum([np.log(pi) for pi in ps])
    dof_F=2*len(ps)
    p_F=1-stats.chi2.cdf(X2_F,dof_F)

    print dof, dof_F
    return G, p, X2_F, p_F
