from factor import *
from factorset import *
from naiveinf import *

def buildrobotex(commandfailrate,stickprob,fpr,fnr):

    c = discretevariable("c",2)
    x0 = discretevariable("x0",3)
    x1 = discretevariable("x1",3)
    r0 = discretevariable("r0",2)
    l0 = discretevariable("l0",2)
    r1 = discretevariable("r1",2)
    l1 = discretevariable("l1",2)

    px0 = discretefactor({x0})
    px0[{x0:0}] = 1.0/3.0
    px0[{x0:1}] = 1.0/3.0
    px0[{x0:2}] = 1.0/3.0

    pc = discretefactor({c})
    pc[{c:0}] = 0.5
    pc[{c:1}] = 0.5

    px1x0c = discretefactor({x1,x0,c})
    px1x0c[{}] = 0.0 # initialize to all zeros
    for oldx in range(0,3):
        for cval in range(0,2):
            newx = oldx-1 if cval else oldx+1
            newx = min(max(newx,0),2)
            px1x0c[{x0:oldx,x1:newx,c:cval}] += 1.0-commandfailrate
            px1x0c[{x0:oldx,x1:oldx,c:cval}] += commandfailrate

    def initsensorcpd(pos,sen,walls):
        f = discretefactor({pos,sen})
        for posval in range(0,3):
            w = walls[posval]
            notw = 1-w
            errrate = fnr if w else fpr
            f[{pos:posval,sen:w}] = 1.0-errrate
            f[{pos:posval,sen:notw}] = errrate
        return f


    pr0x0 = initsensorcpd(x0,r0,[0,1,0])
    pl0x0 = initsensorcpd(x0,l0,[1,0,0])

    def nextsensorcpd(pos,oldsen,sen,walls):
        f = discretefactor({pos,oldsen,sen})
        f[{}] = 0.0
        for posval in range(0,3):
            for oldsenval in range(0,2):
                f[{pos:posval,oldsen:oldsenval,sen:oldsenval}] += stickprob
                w = walls[posval]
                notw = 1-w
                errrate = fnr if w else fpr
                f[{pos:posval,oldsen:oldsenval,sen:w}] += (1.0-stickprob)*(1.0-errrate)
                f[{pos:posval,oldsen:oldsenval,sen:notw}] += (1.0-stickprob)*errrate

        return f

    pr1r0x1 = nextsensorcpd(x1,r0,r1,[0,1,0])
    pl1l0x1 = nextsensorcpd(x1,l0,l1,[1,0,0])
                
    robotbn = factorset()
    robotbn.addfactor(pc)
    robotbn.addfactor(px0)
    robotbn.addfactor(px1x0c)
    robotbn.addfactor(pr0x0)
    robotbn.addfactor(pl0x0)
    robotbn.addfactor(pr1r0x1)
    robotbn.addfactor(pl1l0x1)

    return robotbn,(c,x0,x1,r0,r1,l0,l1)

def buildstudentex():
    # note you will need to have g have values of 0,1,2
    # (not 1,2,3 as in the text)

    # remove line below when you write your code
    # it is okay just to "hard code" all of the values in here
    
    ## Defining variables
    d = discretevariable("d", 2)
    i = discretevariable("i", 2)
    g = discretevariable("g", 3)
    s = discretevariable("s", 2)
    l = discretevariable("l", 2)
    
    ## Hard coding the facotrs
    ## I guess the order of defenition matters or may not check the result of student test

    phi_d = discretefactor({d})
    phi_d[{d:0}] = 0.6
    phi_d[{d:1}] = 0.4

    phi_i = discretefactor({i})
    phi_i[{i:0}] = 0.7
    phi_i[{i:1}] = 0.3

    phi_d_i_g = discretefactor({d,i,g})
    phi_d_i_g[{d:0,i:0,g:0}] = 0.3
    phi_d_i_g[{d:0,i:0,g:1}] = 0.4
    phi_d_i_g[{d:0,i:0,g:2}] = 0.3
    phi_d_i_g[{d:1,i:0,g:0}] = 0.05
    phi_d_i_g[{d:1,i:0,g:1}] = 0.25
    phi_d_i_g[{d:1,i:0,g:2}] = 0.7
    phi_d_i_g[{d:0,i:1,g:0}] = 0.9
    phi_d_i_g[{d:0,i:1,g:1}] = 0.08
    phi_d_i_g[{d:0,i:1,g:2}] = 0.02
    phi_d_i_g[{d:1,i:1,g:0}] = 0.5
    phi_d_i_g[{d:1,i:1,g:1}] = 0.3
    phi_d_i_g[{d:1,i:1,g:2}] = 0.2

    phi_i_s = discretefactor({i,s})
    phi_i_s[{i:0,s:0}] = 0.95
    phi_i_s[{i:0,s:1}] = 0.05
    phi_i_s[{i:1,s:0}] = 0.2
    phi_i_s[{i:1,s:1}] = 0.8

    phi_g_l = discretefactor({g,l})
    phi_g_l[{g:0,l:0}] = 0.1
    phi_g_l[{g:0,l:1}] = 0.9
    phi_g_l[{g:1,l:0}] = 0.4
    phi_g_l[{g:1,l:1}] = 0.6
    phi_g_l[{g:2,l:0}] = 0.99
    phi_g_l[{g:2,l:1}] = 0.01

    studentbn = factorset()
    studentbn.addfactor(phi_d)
    studentbn.addfactor(phi_i)
    studentbn.addfactor(phi_d_i_g)
    studentbn.addfactor(phi_i_s)
    studentbn.addfactor(phi_g_l)

    return studentbn, (d,i,g,s,l)




    # will need to return your factorset (studentbn below) as the 
    # variables in the order d,i,g,s,l (as below)
    # return studentbn,(d,i,g,s,l)


#### below is the testing code

def runrobot():
    robotex,(c,x0,x1,r0,r1,l0,l1) = buildrobotex(0.1,0.2,0.05,0.1)
    robotquery = naiveinfval(robotex,{c},{r0:1,l0:1,r1:1,l1:1})
    return (robotquery,c)

def runstudent():
    studentex,(d,i,g,s,l) = buildstudentex()
    studentquery1 = naiveinf(studentex,{i},{l,s})
    studentquery2 = naiveinfval(studentex,{s},{d:0,l:1})
    return (studentquery1,studentquery2,(d,i,g,s,l))

if __name__ == '__main__':
    # note that rounding used in PS1 solutions will cause the answer to differ
    # from this one (computed without as much rounding) by a bit
    robotquery,_ = runrobot()
    print(robotquery)
    ## should return a factor where c=0 => 0.39676 and c=1 -> 0.603239


    ## it is up to you to figure out if these examples return the right values
    studentquery1,studentquery2,_ = runstudent()
    print(studentquery1)
    print(studentquery2)

## you should probably write your own tests, as we will be testing your
## code on different factorsets as well!
## but don't put them in here, or they will mess up the automatic
## testing -- write them on your own, but don't submit them!
