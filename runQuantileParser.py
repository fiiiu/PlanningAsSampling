

import IndependenceAnalyzer
import numpy as np
import matplotlib.pyplot as plt

ia=IndependenceAnalyzer.IndependenceAnalyzer()

subjects=ia.parser.data.get_subjects()

Gi=np.zeros(len(subjects))
pvali=np.zeros(len(subjects))
dofi=np.zeros(len(subjects))

for ind, subject in enumerate(subjects):
    resi=ia.G(subject)
    if resi is not None:
        Gi[ind],pvali[ind],dofi[ind]=resi


print 'p median={0}'.format(np.median(pvali))

plt.hist(pvali[np.isfinite(pvali)])
plt.title('pvali')

plt.show()



#MULTISTATE
# states=['1302', '1023']
# states=['1320']
# Gi=np.zeros(len(subjects))
# pvali=np.zeros(len(subjects))
# dofi=np.zeros(len(subjects))
# for ind, subject in enumerate(subjects):
#     resi=ia.multistate_G(subject, states)
#     if resi is not None:
#         Gi[ind],pvali[ind],dofi[ind]=resi


# print 'p median={0}'.format(np.median(pvali))

# plt.hist(pvali[np.isfinite(pvali)])
# plt.title('pvali')

# plt.show()

# G2=np.zeros(len(subjects))
# pval2=np.zeros(len(subjects))
# dof2=np.zeros(len(subjects))

# G4=np.zeros(len(subjects))
# pval4=np.zeros(len(subjects))
# dof4=np.zeros(len(subjects))


# for ind,subject in enumerate(subjects):
#     res2=ia.quantile_G(subject, 2)
#     res4=ia.quantile_G(subject, 4)
#     resi=ia.G(subject)
#     if res2 is not None:
#         G2[ind],pval2[ind],dof2[ind]=res2
#     if res4 is not None:
#         G4[ind],pval4[ind],dof4[ind]=res4
#     if resi is not None:
#         Gi[ind],pvali[ind],dofi[ind]=resi
#     #print subject, pvali[ind]

# print 'p median={0}'.format(np.median(pvali))





# plt.subplot(2,3,1)
# plt.hist(G2)
# plt.title('G2')

# plt.subplot(2,3,4)
# plt.hist(pval2)
# plt.title('p2')

# plt.subplot(2,3,2)
# plt.hist(G4)
# plt.title('G4')

# plt.subplot(2,3,5)
# plt.hist(pval4)
# plt.title('pval4')

# plt.subplot(2,3,3)
# plt.hist(Gi)
# plt.title('Gi')

# plt.subplot(2,3,6)

# plt.hist(pvali[np.isfinite(pvali)])
# plt.title('pvali')

# plt.show()

