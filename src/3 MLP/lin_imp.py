# lin_imp.py
# get scitools from
# http://vefur.simula.no/~hpl/scripting/
import scitools.filetable as ft
import random
import sys
from numpy import *

def initfiles():
    
    fulldata=file('housing_data','r')
    traindata=file('housing_data_train','w')
    testdata=file('housing_data_test','w')

    # allow reproducible train/test generation
    random.seed(123)
    prob=2.0/3.0
    
    # reserve 2/3 for training and 1/3 for testing
    for line in fulldata.readlines():
        if random.random()>prob:
            testdata.write(line)
        else:
            traindata.write(line)

    fulldata.close()
    traindata.close()
    testdata.close()
    
def loaddata(filename):
    
    datafile=open(filename,'r')
    data=ft.read(datafile)
    datafile.close()
    return data

def normalize(data,attrmean,attrstd):

    # http://en.wikipedia.org/wiki/Standard_score
    # transform all variables so that they all have 0 mean and 1 stdev

    # for every column/attribute
    for j in range(0,shape(data)[1]):
        # replace entire old column vector with normalized data 
        data[:,j]=(data[:,j]-attrmean[j])/attrstd[j]

    return data

def predict(X,w):

    return dot(X,w)
    
def addx0feat(X):

    # create x0 feature (1 by convention)
    rows=shape(X)[0]
    x0=ones((rows,1),'float')

    return concatenate((x0,X),1)

def batchgradesc(X,y):

    # housekeeping
    i=1
    derror=sys.maxint
    error=0
    
    # initialize the weight vector
    featnum=shape(X)[1]
    w=zeros((featnum+1,1),'float')

    X_ext=addx0feat(X)
    step=0.0001
    dthresh=0.1

    while derror>dthresh:

        diff=y-predict(X_ext,w)

        # update weight vector, element by element
        for j in range(0,shape(X_ext)[1]):
            # numpy arrays do element-wise mult. with *
            w[j]=w[j]+step*sum(diff*X_ext[:,j:j+1])

        # housekeeping
        hserror=sum(diff**2)/shape(X)[0]
        derror=abs(error-hserror)
        error=hserror
        print 'iteration: %d, error: %s' % (i,error)
        i+=1

    return w
