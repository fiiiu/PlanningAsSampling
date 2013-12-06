

import HouseWorldSimulation
import houseWorldAnalysis
import parameters
import random
import matplotlib.pyplot as plt
import numpy as np
import time
import scipy.optimize

def simulated_performance(sim):
    
    perfos=[0,0,0,0,0,0]
    realizations=[0,0,0,0,0,0]
        
    for trial in range(parameters.trial_amount):
        initial_state=random.choice(range(20))+4 #choose among all but goal state and states at distance 1 from goal
        steps=sim.simulate_trial(initial_state)
        distance=sim.world.distance_to_goal(initial_state)
        realizations[distance-2]+=1
        
        if steps==distance:
            perfos[distance-2]+=1
    
    perf=[float(p)/realizations[i] for i,p in enumerate(perfos)]    
    
    return realizations, perf

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
    
    
def optimize_brute():
    
    #model optimization
    gammas=[0.01,0.05,0.1,0.11,0.12,0.13,0.14,0.15,0.16,0.2,0.3,0.5,0.75,0.9,0.99]
    inertias=[0,0.1,0.2,0.5,1,1.2,1.4,1.5,1.6,2,5]
    #etas=[0,0.01,0.05,0.1,0.5,0.75,0.8,0.85,1,2,5]
    etas=[0,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.5,0.75,0.9,1]
    # for testing:
    #~ gammas=[0.13, 0.4]
    #~ inertias=[0.5]
    #~ etas=[0.8]
   
    hwd=houseWorldAnalysis.load_data()
    realsd,perfsd=data_performance(hwd)
    
    kink_pars=[]
    distances=[]
    for gamma in gammas:
        for inertia in inertias:
            for eta in etas:
                
                sim=HouseWorldSimulation.HouseWorldSimulation((gamma,inertia,eta,parameters.agent_kind))
                realsm, perfsm = sim.simulate_performance()
                
                if perfsm[2]-0.03> perfsm[3] <perfsm[4]-0.03:
                    kink_pars.append((gamma,inertia,eta))
                
                distance=np.linalg.norm(np.array(perfsd)-np.array(perfsm))
                penalty = max(0,10*(np.exp(perfsm[4]-perfsm[2])-1))+max(0,30*(np.exp(perfsm[3]-perfsm[4])-1))
                distance=distance+penalty
         
                distances.append(distance)
                if distance<=min(distances):
                    min_pars=(gamma,inertia,eta)
                    
                
    #print chosen_pars
    #print "distances: " + str(distances) 
    print "kink parameters: " + str(kink_pars)
    print "minimizing pars: " + str(min_pars)
    return min_pars

def difference(pars, perfsd):
    sim=HouseWorldSimulation.HouseWorldSimulation((pars[0], pars[1], pars[2], parameters.agent_kind))
    _, perfsm = sim.simulate_performance()
    if len(perfsm)<6:
        perfsm.extend([0]*(6-len(perfsm)))
    dif=np.array(perfsd)-np.array(perfsm)
    #penalize form of curve:
    #penalty = float(perfsm[2]<perfsm[4])+float(perfsm[3]>perfsm[4])
    penalty = max(0,10*(np.exp(perfsm[4]-perfsm[2])-1))+max(0,30*(np.exp(perfsm[3]-perfsm[4])-1))
    return np.dot(dif,dif)+penalty


def vecdif(pars, perfsd):
    sim=HouseWorldSimulation.HouseWorldSimulation((pars[0], pars[1], pars[2], parameters.agent_kind))
    _, perfsm = sim.simulate_performance()
    return [(i-j) for i,j in zip(perfsd,perfsm)] 
    #dif=np.array(perfsd)-np.array(perfsm)
    #return dif[0], dif[1], dif[2], dif[3], dif[4], dif[5]
    

def single_sim(params=None):
    
    if params is None:
        pars=(0.2812,1.2956,0.2752,'single_crosser')
        #pars=(0.4526,0.3286,0.1255,'single_crosser')
        #pars=(0.3888,0.2903,0.1052,'single_crosser')
        #pars=(0.22743923,  0.87411748,  0.59006621, 'single_crosser')
        pars=(0.13033507,  3.61081327,  0.75980129, 'single_crosser')
        #pars=( 1.00000005e-02,   6.41943575e-08,   9.99999764e-03, 'single_crosser')
        #pars=(0.19563459,  0.08862393,  0.0206292, 'single_crosser')
        pars=(0.15,1.1616,0.1323,parameters.agent_kind)
        pars=(0.1,  0.5,  0.2, parameters.agent_kind)
    else:
        pars=(params[0],params[1],params[2],parameters.agent_kind)    
    
    sim=HouseWorldSimulation.HouseWorldSimulation(pars)
    realsm, perfsm = sim.simulate_performance()
    if len(perfsm)<6:
        perfsm.extend([0]*(6-len(perfsm)))
    
    penalty = max(0,100*(np.exp(perfsm[4]-perfsm[2])-1))+max(0,300*(np.exp(perfsm[3]-perfsm[4])-1))
    print 'penalty: ' + str(penalty)
    
    hwd=houseWorldAnalysis.load_data()
    realsd,perfsd=data_performance(hwd)
    
    levels=range(2,8)
    plt.plot(levels,perfsd,'-bx')
    dif=np.array(perfsd)-np.array(perfsm)
    print np.dot(dif,dif)
    plt.plot(levels,perfsm,'-ko')
    plt.show()


def optimize_scipy(method='Powell'):
    
    print method + ' minimization'
    
    #DATA
    hwd=houseWorldAnalysis.load_data()
    realsd,perfsd=data_performance(hwd)
    
    #INITIALIZE
    #ranges=((0.01,0.99),(0,3),(0,3))
    #ranges=np.s_[0.01:0.99:0.05, 0:3:0.25, 0:3:0.25]
    x0=np.array((0.15,0.16,0.13))

    #MINIMIZE
    #minimizing_parameters=scipy.optimize.brute(difference,ranges,args=[perfsd])#, finish=None)
    #minimizing_parameters=scipy.optimize.anneal(difference,x0,args=[perfsd],maxeval=3, lower=(0.001,0,0),\
    #upper=(0.99,5,5))#, finish=None)
    minimizing_parameters=scipy.optimize.fmin_powell(difference,x0,args=[perfsd])#, finish=None)
    #minimizing_parameters=scipy.optimize.leastsq(vecdif, x0, args=perfsd)
    minimizing_parameters=scipy.optimize.minimize(difference,x0,args=[perfsd],\
                            method=method, bounds=[(0.001,0.999),(0,5),(0,5)], tol=0.001 )#, finish=None)
    
    #print minimizing_parameters
    return minimizing_parameters['x']

stime=time.time()

#single_sim()
#pars=optimize_scipy('L-BFGS-B')
#pars=optimize_brute()
#pars=(0.13,1,0.4)
#print pars

single_sim()



print "elapsed time: " + str(time.time()-stime)




