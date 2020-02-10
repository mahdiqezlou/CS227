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
    
    ## From here is just for trees
    def treecalibrate(self):
        """ Find the ready clusters. While there exist some un informed clusters,
        keep beleif update the uninfomed edjes (having mu of 1)"""
        
        ## get the ready clusters and edjes to pass messgae through
        r_Cs, ed_j = self._ready_Cs()
        while len(r_Cs) != 0:
            for i in r_Cs:
                self._BU_Message(r_Cs, ed_j)
            r_Cs, ed_j = self._ready_Cs()
          
    def _ready_Cs(self):
        """ Find ready Clusters : Those have only one uninformed edje (mu = 1) """
        # enumerate over all clusters and get each one's neighbors
        for i,a in enumerate(self._U._adj) :
            r_Cs = []
            ed_j = []
            num_non_ready_mess = 0
            # enumerate on edjes for every cluster
            for j in a:
                if self.getmu(i, j) == 1:
                    num_non_ready_mess += 1
                    # non-ready neighbor index
                    non_ready_neib = j
            if num_non_ready_mess == 1:
                r_Cs.append(i)
                ed_j.append(non_ready_neib)

        return (r_Cs, ed_j)

    def _BU_Message(self, i, j):
        """Belief update the clusters i and j
        i is sending clique
        j is receiving clique
        """
        sigma_i_j = self._beta[i].marginalize(self._U.clusters[i].vars - self._sep_set(i,j))
        self._beta[j] = self._beta[j] * (sigma_i_j / self.getmu(i,j))
        self._mu[(i, j)] = sigma_i_j

    def _sep_set(self, i, j):
        """ Get the separating set between clusters i and j
        It is just the common set between varaibles of factors in cluster i and cluster j
        """

        return self._U.Clusters.vars[i] & self._U.clusters.vars[j]







            


