from clustergraph import *
from clusterdist import *
from factor import *
from factorset import *
from itertools import product
#from veinf import *

def makefactor(vars,vals):
    phi = discretefactor(set(vars))
    for j,x in enumerate(product(*map((lambda v : [(v,i) for i in range(v.nvals)]),vars))):
        s = {a:b for (a,b) in x}
        phi[s] = vals[j]
    return phi

def buildnewstudentex():
    c = discretevariable("c",2)
    d = discretevariable("d",2)
    t = discretevariable("t",2)
    i = discretevariable("i",2)
    g = discretevariable("g",3)
    s = discretevariable("s",2)
    l = discretevariable("l",2)
    j = discretevariable("j",2)

    studentbn = factorset()

    pc = makefactor([c],[0.5,0.5])
    studentbn.addfactor(pc)
    pd = makefactor([c,d],[0.4,0.6,0.8,0.2])
    studentbn.addfactor(pd)
    pi = makefactor([i],[0.6,0.4])
    studentbn.addfactor(pi)
    pt = makefactor([i,t],[0.9,0.1,0.4,0.6])
    studentbn.addfactor(pt)
    pg = makefactor([t,d,g],
        [0.3,0.4,0.3,
         0.05,0.25,0.7,
         0.9,0.08,0.02,
         0.5,0.3,0.2])
    studentbn.addfactor(pg)
    ps = makefactor([t,s],[0.95,0.05,0.2,0.8])
    studentbn.addfactor(ps)
    pl = makefactor([g,l],[0.1,0.9,0.4,0.6,0.99,0.01])
    studentbn.addfactor(pl)
    pj = makefactor([l,s,j],
        [0.9,0.1,
            0.4,0.6,
            0.3,0.7,
            0.1,0.9])
    studentbn.addfactor(pj)

    cg = clustergraph()
    cd = cg.addcluster({c,d})
    gdt = cg.addcluster({g,d,t})
    gts = cg.addcluster({g,t,s})
    it = cg.addcluster({i,t})
    slg = cg.addcluster({s,l,g})
    jls = cg.addcluster({j,l,s})
    cg.addedge(cd,gdt)
    cg.addedge(gdt,gts)
    cg.addedge(slg,gts)
    cg.addedge(slg,jls)
    cg.addedge(gts,it)
    alpha = {pc : cd, pd : cd, pg : gdt, pi : it, pt : it, ps : gts, pl : slg, pj : jls}

    return studentbn,(c,d,t,i,g,s,l,j),cg,alpha

# needed because str() on a set uses repr(), not str() on underlying elements
def settostr(s):
    return '{'+','.join([str(i) for i in s])+'}'

def printdist(cd):
    cg = cd.graph
    for i,f in enumerate(cg.clusters):
        print("beta for %s:" % settostr(f))
        print(cd.getbeta(i))
    for i in range(len(cg.clusters)):
        for j in cg.adj(i):
            if j>i:
                print("mu for (%s)-(%s):" % (settostr(cg.clusters[i]),settostr(cg.clusters[j])))
                print(cd.getmu(i,j))


## This is just one very simple example.  You'll need to test to 
## make sure your code works on other more complex examples
## including those with disconnected graphs (as often happens after
## conditioning on evidence)
##
##
if __name__ == '__main__':
    studentex,(c,d,t,i,g,s,l,j),cg,alpha = buildnewstudentex()
    cd = clusterdist(cg,alpha)

    print ("before calibration:")
    printdist(cd)
    cd.treecalibrate()
    print ("after calibration:")
    printdist(cd)
