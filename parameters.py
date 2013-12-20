
import platform

#####
#
# General
#
verbose=False
if platform.system() == 'Darwin':
    data_directory='/Users/alejo/Neuro/Planning/Data/'
else:
    data_directory='/home/alejo/Neuro/Planning/Data/'

data_filename='data_AS.mat'
demographic_filename='Genero_Edad.txt'
group_filename='Grupos_experimentales.txt'
CBQ_filename='CBQ_MM2010.xls'


#####
#
# Data analysis
#
n_realizations=3         #realizations for kullback monte carlo
filter_correct=False        #post select winning trials
starting_state='2301'#1320'#0123'#3012'#2301'#Cou1320'#1302'# '0321'#1302#1320#312#3210#3021#312#3210 #312    #for data analysis


#####
#
# Simulations
#
initial_state=[17]*10       #for simulations
gamma=0.2                   #discount factor
inertia=2                   #avoids returning to previous states
eta=2                       #ponderates crossings more. 
agent_kind='heuristic_inertial'           #agent kind
trial_amount=10000        #amount of simulated trials
