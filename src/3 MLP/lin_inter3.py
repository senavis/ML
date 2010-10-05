# lin_inter3.py
from lin_imp2 import *

traindata=loaddata('housing_data_train')

featnum=shape(traindata)[1]-1

X_train=traindata[:,0:featnum]
y_train=traindata[:,featnum:]

attrmean=X_train.mean(0)
attrstd=X_train.std(0)

X_train=normalize(X_train,attrmean,attrstd)

w=stogradesc(X_train,y_train)

print '\nweight vector: \n%s'%w

testdata=loaddata('housing_data_test')
featnum=shape(testdata)[1]-1

X_test=testdata[:,0:featnum]
y_test=testdata[:,featnum:]

X_test=normalize(X_test,attrmean,attrstd)
X_test=addx0feat(X_test)

y_pred=predict(X_test,w)

mse=sum((y_test-y_pred)**2)/shape(X_test)[0]

print '\nMSE=%s'%mse
