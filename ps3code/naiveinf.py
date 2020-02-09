from functools import reduce
import operator

# implements naive inference
# by just forming the joint, then marginalizing out
# and then conditioning

# should return a factor of the distribution of X given Y (X and Y are scopes)
# as calculated from the factorset fs
# returned value will be a factor over the union of X and Y
def naiveinf(fs,X,Y):
    

    unnorm_total_joint = reduce(lambda a, b: a*b, fs.factors)
    normed = unnorm_total_joint / (unnorm_total_joint.marginalize(fs.vars))
    # Marginalize over all other variables except thoe in X U Y, would be P(X,Y)
    marg_keep_X_Y = normed.marginalize(set(T for T in fs.vars if not (T in X.union(Y))))
    # Find P(Y)
    marg_keep_Y = marg_keep_X_Y.marginalize(X)
    
    #return P(X|Y)
    return marg_keep_X_Y/marg_keep_Y

    
    

    

# same as above, but y is an assignment (not just a set of variables)
# and so the returned factor is just over X (the probabilty of X given Y=y)
def naiveinfval(fs,X,y):
    # in case this helps:
    # y is a dictionary (mapping from variables to values)
    # thus y.keys() is the set of variables
    
    # Call previous function to calculate the conditional factors
    cond_prob = naiveinf(fs, X, y.keys())
    
    # reduce the conditional factor by assigning values to Y
    return cond_prob.reduce(y)
