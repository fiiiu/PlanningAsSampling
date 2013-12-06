
import HouseWorld
import HouseWorldData
import houseWorldAnalysis
import plotting
import utils
import sys
import random
import matplotlib.pyplot as plt
import scipy.io
import numpy as np

def main():

    #~ #basic test
    #~ if len(sys.argv) > 1:
        #~ state_id = int(sys.argv[1])
    #~ else:
        #~ state_id=3
    #~ print "state " + str(state_id) + " distance to goal is: " + str(hw.distance_to_goal(state_id))

    #plt.show()

#~ 
    #~ hwd=houseWorldAnalysis.load_data()
        #~ 
    #~ #subjects=['181']
    #~ subjects=hwd.get_subjects()#[0:16]
#~ 
    #~ 
    #~ cps=houseWorldAnalysis.consecutive_ps(hwd, subjects)
    #~ splitavs, splitdevs, splitps=houseWorldAnalysis.split_todays(cps)
    #~ 
    #~ plt.bar([-0.5,1.5],[splitavs[0],splitavs[1]], color='r', yerr=splitdevs)
    #~ print len(splitps[0]), len(splitps[1])
    #~ plt.show()
    
    #print cps
    #avs, bins, nums=utils.binned_average(cps,2)
    #plt.plot(bins, nums, 'rx')
    #plt.show()
    #plt.plot(bins, avs, 'ko')
    #plt.ylim([0,1])
    #plt.show()
    #~ 
    #~ plt.plot([cp[0] for cp in cps], [cp[1] for cp in cps], 'ko')
    #~ plt.ylim([-0.1,1.1])
    #~ plt.show()
    #~ return
    
    hwd=houseWorldAnalysis.load_data()
    subs=hwd.get_subjects()[0:3]

    
    print houseWorldAnalysis.single_G(hwd,subs)


    #return
    # kbs,choices=houseWorldAnalysis.subject_kullbacks(hwd,subs)
    # skbs=houseWorldAnalysis.surrogate_subject_kullbacks(hwd,subs)
    # pvs=houseWorldAnalysis.subject_pvals(hwd, subs)
    
    gs,pvs,choices=houseWorldAnalysis.subject_Gs(hwd,subs)

    ## SNIPPET
    for sub in subs:
        try:
            if len(choices[sub][0])>1:
                print sub, len(choices[sub][0]), gs[sub], pvs[sub]
        except:
            KeyError
    
    #####
    
        
    print pvs
    print str.format("mean p: {0}, median p: {1}", np.mean(pvs.values()), np.median(pvs.values()))
    
    return
    plt.hist(pvs.values())
    plt.xlim([0, 1])
    #plt.hist(gs.values())
    plt.show()
    return
   
    for i,sub in enumerate(subs):
        if sub in kbs.keys():
            print str.format("subject {0}, D={1}. Days: {2}; total choices: {3}\n entropy={4}, p={5}",
                             sub,kbs[sub],len(choices[sub]), np.sum(choices[sub]),
                             utils.H([sum(choice) for choice in choices[sub]]), pvs[sub])
            plt.subplot(4,4,i+1)
            plt.hist(skbs[sub])
            plt.axvline(x=kbs[sub], linewidth=2, color='r')
            plt.xlim([0,1])
        
    plt.show()
    return
    
    
    pvs=houseWorldAnalysis.subject_pvals(hwd)#, subject)
    
    print pvs
    print str.format("mean p: {0}, median p: {1}", np.mean(pvs), np.median(pvs))
    plt.hist(pvs.values())
    plt.show()
    return
    
     ## pvals vs entropies
    #~ entropies=[]
    #~ pvls=[]
    #~ 
    #~ for sub in subs:
        #~ entropies.append(utils.H([sum(choice) for choice in choices[sub]]))
        #~ pvls.append(pvs[sub])
    #~ 
    #~ plt.plot(entropies,pvls,'ko')
    #~ plt.show()
    #~ return
    
    
    #test move choice
    hw=HouseWorld.HouseWorld()
    hwd=HouseWorldData.HouseWorldData()
    hwd.load_from_mat()
    dates,moves=hwd.select_actions(312, '181')
    
    days,choices,multiplicities=houseWorldAnalysis.parse_in_days(dates,moves)
    kullbacks=houseWorldAnalysis.compute_kullbacks(choices)
    
    seconds=[(day-min(days)).total_seconds() for day in days]
    
    #plt.plot(seconds, kullbacks)
    print np.mean(kullbacks)
    print multiplicities
    print kullbacks
    plt.hist(kullbacks)
    plt.show()
    
    return
    
    
    #choices=[hw.action_to_id(move) for move in moves]
    
    #print dates
    #print moves
    #~ 
    #~ plotting.running_plot(dates, choices)
    #~ plt.hist(choices)
    #~ plt.show()
    #~ 
    plotting.joint_plot(dates, choices)
    plotting.show()
    
    
    return
    
    all_moves=list(set(moves)) # I do this before to prevent altering the ordering
    print all_moves
    move_codes=[all_moves.index(move) for move in moves]
    plt.hist(move_codes)
    plt.show()
    
    #intervals, choices=running_bar_plot(dates,moves)
    #print intervals
    #print choices
    
    choicesT=map(list, zip(*choices))
    bot2=[choicesT[0][i]+choicesT[1][i] for i in range(len(choicesT[0]))]
    
    #width=100000
    width=0.5
    plt.bar(intervals, choicesT[0], width, color='b')
    plt.bar(intervals, choicesT[1], width, color='r', bottom=choicesT[0])
    plt.bar(intervals, choicesT[2], width, color='y', bottom=bot2)
    plt.show()
    
#    
#    #model test
#    hw=HouseWorld.HouseWorld(gamma=0.3, inertia=0.05)
#    realsm,perfsm = simulated_performance(hw)
#    print realsm
#    print perfsm
#    xm=range(2,8)
#    plt.plot(xm,perfsm)
#    
#    #~ 
#    #data test
#    hwd=HouseWorldData.HouseWorldData()
#    hwd.load_from_mat()
#    
#    realsd,perfsd = data_performance(hwd)
#    print realsd
#    print perfsd
#    xd=range(2,8)
#    plt.plot(xd,perfsd)
#
#    plt.show()
    

#    #model optimization
#    gammas=[0.01,0.05,0.1,0.15,0.2,0.3,0.5,0.7,0.8,0.85,0.9,0.95,0.99]
#    inertias=[0,0.01,0.05,0.1,0.2,0.5,1,1.5,2,5]
#    
#    #gammas=[0.5,0.6]
#    #inertias=[0,1]
#    #parameters=[(0.05, 1), (0.1, 1.5), (0.15, 0.1), (0.15, 1.5), (0.2, 1.5), (0.3, 1), (0.5, 2)]
#
#    #parameters=(0,0)
#    parameters=[]
#    min_distance=100
#    chosen_pars=(0,0)
#    distances=[]
#    for gamma in gammas:
#        for inertia in inertias:
#    #for pars in parameters:
#            #gamma=pars[0]
#            #inertia=pars[1]
#            hw=HouseWorld.HouseWorld(gamma=gamma, inertia=inertia)
#            realsm,perfsm = simulated_performance(hw)
#            
#            if perfsm[2]-0.03> perfsm[3] <perfsm[4]-0.03:
#                parameters.append((gamma,inertia))
#                distance=np.linalg.norm(np.array(perfsd)-np.array(perfsm))
#                distances.append(distance)
#            #~ 
#            #~ distance=np.linalg.norm(np.array(perfsd)-np.array(perfsm))
#            #~ if distance<min_distance:
#                #~ min_distance=distance
#                #~ chosen_pars=pars
#    #~ 
#    print parameters
#    #print chosen_pars
#    print distances
#    
#    


def data_performance(hwd):
    
    perfos=[0,0,0,0,0,0]
    realizations=[0,0,0,0,0,0]
    
    for trial in range(hwd.trial_amount):
        initial_state=hwd.statess[trial][0,0]
        realizations[hwd.min_movess[trial]-2]+=1
        if hwd.successes[trial]==1:
            perfos[hwd.min_movess[trial]-2]+=1
            
    perf=[float(p)/realizations[i] for i,p in enumerate(perfos)]
    
    return realizations,perf




def simulated_performance(hw):
    
    trial_amount=10000
    perfos=[0,0,0,0,0,0]
    realizations=[0,0,0,0,0,0]
        
    for trial in range(trial_amount):
        initial_state=random.choice(range(20))+4 #choose among all but goal state and states at distance 1 from goal
        distance=hw.distance_to_goal(initial_state)
        steps=hw.simulate_trial(initial_state)
        realizations[distance-2]+=1
        
        if steps==hw.distance_to_goal(initial_state):
            perfos[distance-2]+=1
    
    perf=[float(p)/realizations[i] for i,p in enumerate(perfos)]    
    
    return realizations, perf
    
    
def running_bar_plot(dates, moves):
    
    start_date=dates[0]
    choices=[[0,0,0]]
    counter=0
#    current_date=dates[0]
    current_interval=0
    intervals=[current_interval]
    
    for ind,date in enumerate(dates):
        
        if moves[ind]==(2,1):
            choice=0
        elif moves[ind]==(3,1):
            choice=1
        elif moves[ind]==(4,1):
            choice=2
        
        #interval=(date-start_date).total_seconds()
        interval=(date.month-start_date.month)
#        if interval == current_interval:
#            pass
#        else:
        if interval not in intervals:
            counter+=1
            intervals.append(interval)
            #current_interval=interval
            choices.append([0,0,0])

        choices[counter][choice]+=1
    
    choices=[[float(val)/sum(vec) for val in vec] for vec in choices]
    
    return intervals, choices
    #plt.bar(
    #plt.show()
    
    
    

if __name__ == "__main__":
    main()
