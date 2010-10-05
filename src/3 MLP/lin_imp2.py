# lin_imp2.py
from lin_imp import *

def stogradesc(X,y):

    i=1
    derror=sys.maxint
    error=0
    
    # initialize the weight vector
    featnum=shape(X)[1]
    w=zeros((featnum+1,1),'float')

    X_ext=addx0feat(X)
    step=0.001
    dthresh=0.1

    while derror>dthresh:

        # for every training example
        for j in range(0,shape(X_ext)[0]):            
            # update the weight vector
            w=w+step*(y[j]-predict(X_ext[j:j+1,:],w))*X_ext[j:j+1,:].transpose()
    
        mse=sum((y-predict(X_ext,w))**2)/shape(X)[0]
        derror=abs(error-mse)
        error=mse
        print 'iteration: %d, error: %s' % (i,error)
        
        i+=1

    return w
