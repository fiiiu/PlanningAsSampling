import Age
import parameters
import xlrd
import numpy as np

class CBQData:

    """
    questions->indices:

    surgency
    direct [1,4,7,16,22,25,28,34] -> [0,3,5,17,20,26]
    invert [10,13,19,31] -> [7,9,14,23]

    negative affect
    direct [2 5 8 11 17 32 35] -> [1, 4, 8, 12, 24]
    inverse [14 20 23 26 29] -> [10, 15, 18, 21]

    effortful control
    direct [3 6 9 12 15 18 21 24 27 30 33 36] -> [2, 6, 11, 13, 16, 19, 22, 25]

    """

    def __init__(self):
        
        self.data_fullfilename=parameters.data_directory+parameters.CBQ_filename
        self.data={}
        self.data_loaded=False


    def load(self):
        
        if self.data_loaded:
            return

        book=xlrd.open_workbook(self.data_fullfilename)
        datasheet=book.sheet_by_index(0)
        rawdata={}
        
        for rownum in range(datasheet.nrows)[1:]:
            row=datasheet.row_values(rownum)
            results=[0 if res=='NA' else np.nan if res=='' else int(res) for res in row[4:]]
            rawdata[str(int(row[0]))]=np.array(results)


        #compute CBQ summaries
        for subject in rawdata.keys():
            
            sur_plus=rawdata[subject][[0,3,5,17,20,26]]
            sur_neg=[self.invert(score) for score in rawdata[subject][[7,9,14,23]]]
            surgency=sum(sur_plus)+sum(sur_neg)

            naffect_plus=rawdata[subject][[1, 4, 8, 12, 24]]
            naffect_neg=[self.invert(score) for score in rawdata[subject][[10, 15, 18, 21]]]
            naffect=sum(naffect_plus)+sum(naffect_neg)

            effcontrol_plus=rawdata[subject][[2, 6, 11, 13, 16, 19, 22, 25]]
            effcontrol=sum(effcontrol_plus)

            self.data[subject]=(surgency, naffect, effcontrol)

        self.data_loaded=True


    def invert(self, score):
        return -score+8


    def get_subjects(self):
        return self.data.keys()


    def get_scores(self, subject):
        if subject in self.get_subjects():
            return self.data[subject]
        else:
            print 'no CBQ data for subject {0}'.format(subject)
            return (-1,-1,-1)