from factor import *
import copy

# describes a distribution over a cluster graph
# as parameterized by betas (factors over the clusters)
# and mus (factors over the sep-sets)
class clusterdist:
    # U is the clustergraph on which this distribution is based
    # alpha is a mapping from factors to cluster indexes in U
    def __init__(self,U,alpha):
        self._U = copy.copy(U) # so that the original can change
        self._beta = [] # list of local factors, _beta[i] matches cluster i in U
        self._mu = {} # dictionary mapping (i,j) to factor for edge i-j
                # note that (3,5) and (5,3) are the same, so we only
                # keep (3,5) -- because 3<5
        self._initializegraph(alpha)

    # assumes that sep-set is intersection of scopes of either side
    def _initializegraph(self,alpha):
        for i in range(len(self._U.clusters)):
            self._beta.append(discretefactor(self._U.clusters[i],1.0))
        for i in range(len(self._U.clusters)):
            for j in self._U.adj(i):
                if i<j:
                    self._mu[(i,j)] = discretefactor(self._U.clusters[i] & self._U.clusters[j],1.0)
        for f,i in alpha.items():
            self._beta[i] = self._beta[i] * f

    @property
    def graph(self):
        return self._U

    # after calibration, should be the marginal over the cluster i
    def getbeta(self,i):
        return self._beta[i]

    # after calibration, should be the marginal over the sep-set btwn i&j
    def getmu(self,i,j):
        return self._mu[(i,j)] if i<j else self._mu[(j,i)]

    # calibrates, assuming that the clustergraph is a *forest*
    # (not necessarily a tree, despite the name -- it might be
    #  multiple disconnected trees -- this happens often once
    #  evidence is introduced)
    def treecalibrate(self):
        ### For you to write (along with any helper methods you wish)
        while
        for i in len(self._U.clusters):
            for j in self._U._adj:
                if getmu(i,j) == 1:
                    _BU_Message(i,j)

        retutn self._beta         
            


    def _BU_Message(self, i, j):

        #i sending clique
        #j receibing clique
        if i<j :
            sigma_i_j = self.beta[i].marginalize(self._U.clusters[i] - S_i_j)
            self._beta[j] = self._beta[j] * (sigma_i_j / getmu(i,j))
            self._mu[(i, j)] = sigma_i_j

        else :

            reverse




            


