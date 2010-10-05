# lin_inter.py
from lin_imp import *

# separate into test/train files
initfiles()

traindata=loaddata('housing_data_train')

# last column in file is the target vector
featnum=shape(traindata)[1]-1

# slicing i:j -> select where index k is i<=k<j
# and min/max defaults are 0/sys.maxint, for [:]
# http://docs.python.org/reference/expressions.html#slicings
X_train=traindata[:,0:featnum]
y_train=traindata[:,featnum:]

# get vectors with the mean/std for each column/attribute
attrmean=X_train.mean(0)
attrstd=X_train.std(0)

# we normalize data in the X_train matrix so that
# the scale of features with larger ranges do not
# overshadow those with smaller ranges.
X_train=normalize(X_train,attrmean,attrstd)

# calculate the weight/parameter vector
w=batchgradesc(X_train,y_train)

print '\nweight vector: \n%s'%w

inst=array([0.04741,0.00,11.930,0,0.5730,6.0300,80.80,2.5050,1,273.0,21.00,396.90,7.88])
inst.shape=(1,inst.size)

inst=normalize(inst,attrmean,attrstd)
inst=addx0feat(inst)

print '\nnormalized and extended instance vector: \n%s'%inst.transpose()

y=predict(inst,w)

print '\npredicted MEDV:%s'%y
