
import Age

import parameters
import csv

class DemographicData:


    def __init__(self):
        
        self.data_fullfilename=parameters.data_directory+parameters.demographic_filename
        self.group_fullfilename=parameters.data_directory+parameters.group_filename
        self.data={}
        self.groups={}
        self.data_loaded=False

    def load(self):
        
        if self.data_loaded:
            return

        with open(self.group_fullfilename) as inputfile:
            groupdata = list(csv.reader(inputfile, delimiter='\t'))
        for line in groupdata[1:]:
            self.groups[line[0].rstrip()]=(line[1]=='Tratado')
            
        with open(self.data_fullfilename) as inputfile:
            rawdata = list(csv.reader(inputfile, delimiter='\t'))
        for line in rawdata[1:]:
            if line[0].rstrip() in self.groups.keys():
                if self.groups[line[0].rstrip()]:
                    self.data[line[0].rstrip()]=(line[2], Age.Age(line[3][0], line[3][2]))

        self.data_loaded=True


    def get_subjects(self):
        return self.data.keys()


    def get_sex(self, subject, boolean=False):
        if subject not in self.data.keys():
            return '?'
        else:
            sex=self.data[subject][0]
            if not boolean:
                return sex
            else:
                if sex=='M':
                    return 1
                elif sex=='F':
                    return 0
                else:
                    return -1
                
            

    def get_age(self, subject):
        if subject in self.data.keys():
            return self.data[subject][1]
        else:
            return '?'
            