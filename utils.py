
import numpy as np
from scipy import stats


def sigmoid(z):
    """
    Sigmoid function.
    """
    return 1.0 / (1.0 + np.exp(-z))


def binned_average(pairs, nbins=10):
    
    xs=[pair[0] for pair in pairs]
    ys=[pair[1] for pair in pairs]
    start=np.floor(min(xs))
    stop=np.ceil(max(xs)+0.001)
    bins=np.linspace(start,stop,nbins+1)
    inds=np.digitize(xs,bins)#,right=True)
    sums=np.zeros(nbins)
    nums=np.zeros(nbins)
    for i in range(len(ys)):
        sums[inds[i]-1]+=ys[i]
        nums[inds[i]-1]+=1
    bave=np.where(nums>0, sums/nums, 0)
    bcenters=[(bins[i+1]+bins[i])/2 for i in range(len(bins)-1)]
    return bave, bcenters, nums
    
    
def H(p):
    
    """
    Return the entropy of a distribution
    """
    
    #normalize & convert to numpy arrays
    pn=np.array([float(el)/np.linalg.norm(p) for el in p])
    
    h=0
    for pi in pn:
        if pi != 0:
            h-=np.log2(pi)*pi
            
    return h


def kullback_leibler(p, q):

    """
    Computes D(P||Q).
    p and q need not be normalized, what about number of entries?!? --FOR NOW, I DONT CARE
    DO check equal length
    """
    #~ 
    #~ pnp=np.array(p, dtype=float)
    #~ qnp=np.array(q, dtype=float)
    #~ 
        
    if len(p) != len(q):
        print('distributions should have identical domains')
        return -1
        
    #normalize & convert to numpy arrays
    pn=np.array([float(el)/sum(p) for el in p])
    qn=np.array([float(el)/sum(q) for el in q])
    
    #compute divergence
    Dpq=0
    for i in range(len(pn)):
        #return if p has probability where q doesn't
        if qn[i]==0 and pn[i]!=0:
            print('Kullback Leibler Divergence not defined')
            return -1
        #p's equal to 0 contribute 0
        if pn[i]!=0:
            Dpq+=np.log(pn[i]/qn[i])*pn[i]
            
    
    return Dpq



def G_OLD(P, Q):

    """
    Computes G statistic for distribution P respect to distribution Q.
    differs from D_KL in normalization, depends on the total counts on P. 
    P and Q need not be normalized.
    Checks equal length.
    """
        
    if len(P) != len(Q):
        print('distributions should have identical domains')
        return -1
        
    #convert to numpy arrays, normalize for calculation.
    Pn=np.array([float(el)/sum(P) for el in P])
    Qn=np.array([float(el)/sum(Q) for el in Q])
    
    #compute G
    G=0
    for i in range(len(Pn)):
        #return if f has counts where fhat doesn't
        if Qn[i]==0 and Pn[i]!=0:
            print('G not defined')
            return -1
        #f's equal to 0 contribute 0
        if Pn[i]!=0:
            G+=np.log(Pn[i]/Qn[i])*Pn[i]
            
    G=2*sum(P)*G

    return G



def G_goodness_of_fit(P, Q):

    """
    Computes G statistic for distribution P respect to distribution Q.
    differs from D_KL in normalization, depends on the total counts on P. 
    P and Q need not be normalized.
    Checks equal length.
    """
        
    if len(P) != len(Q):
        print('distributions should have identical domains')
        return -1
        
    #convert to numpy arrays.
    O=np.array(P, dtype=float)
    E=np.array(Q, dtype=float)
    
    #compute G
    G=0
    for i in range(len(E)):
        #return if f has counts where fhat doesn't
        if E[i]==0 and O[i]!=0:
            print('G not defined')
            return -1
        #f's equal to 0 contribute 0
        if O[i]!=0:
            G+=2*O[i]*np.log(O[i]/E[i])
    
    dof=len(E)-1      
    pvalue=1-stats.chi2.cdf(G,dof)
    return G, pvalue, dof




def G_independence(rctable):

    """
    Computes G for independence test.

    Args:
        rctable: RxC table of counts.
    Returns:
        G: statistic.
        pvalue: p-value, from chi2 with dof.
        dof: degrees of freedom.
    """

    nptable=np.array(rctable, dtype=float)

    nonzeros=nptable!=0
    g1=np.sum(nptable[nonzeros]*np.log(nptable[nonzeros]))

    rowsum=np.sum(nptable,0)
    rownonzeros=rowsum!=0
    g2=np.sum(rowsum[rownonzeros]*np.log(rowsum[rownonzeros]))

    colsum=np.sum(nptable,1)
    colnonzeros=colsum!=0
    g3=np.sum(colsum[colnonzeros]*np.log(colsum[colnonzeros]))

    g4=np.sum(nptable)*np.log(np.sum(nptable))
    
    G=2*(g1-g2-g3+g4)

    dof=(nptable.shape[0]-1)*(nptable.shape[1]-1)
    pvalue=1-stats.chi2.cdf(G,dof)
    return G, pvalue, dof

