
import IndependenceAnalyzer
import matplotlib.pyplot as plt

ia=IndependenceAnalyzer.IndependenceAnalyzer()


table, Gstats, Kstats=ia.alternance_analysis(consecutives=False, incorrect=False)

print table
print Gstats

plt.imshow(table, interpolation='none')
plt.colorbar()
plt.show()


plt.subplot(1,3,1)
plt.hist(Kstats[0])
plt.subplot(1,3,2)
plt.hist(Kstats[1])
plt.subplot(1,3,3)
plt.hist(Kstats[2])
plt.show()






table, stats=ia.markov_intraday(consecutives=False, incorrect=False)
G,p,dof=stats

print table
print G, p, dof

plt.imshow(table, interpolation='none')
plt.colorbar()
plt.show()

