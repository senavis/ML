# lin_inter2.py
from lin_inter import *

testdata=loaddata('housing_data_test')
featnum=shape(testdata)[1]-1

X_test=testdata[:,0:featnum]
y_test=testdata[:,featnum:]

X_test=normalize(X_test,attrmean,attrstd)
X_test=addx0feat(X_test)

y_pred=predict(X_test,w)

mse=sum((y_test-y_pred)**2)/shape(X_test)[0]

print 'MSE=%s'%mse
