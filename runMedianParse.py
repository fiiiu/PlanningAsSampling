

import IndependenceAnalyzer
import numpy as np
import matplotlib.pyplot as plt

ia=IndependenceAnalyzer.IndependenceAnalyzer()

subjects=ia.parser.data.get_subjects()
G=np.zeros(len(subjects))
pval=np.zeros(len(subjects))
dof=np.zeros(len(subjects))
for ind,subject in enumerate(subjects):
    G[ind],pval[ind],dof[ind]=ia.median_G(subject)

plt.hist(pval)
plt.show()

