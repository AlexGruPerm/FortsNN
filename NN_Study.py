import numpy as np
from decimal import *



def nonlin(x, deriv=False):
    if (deriv == True):
        return x * (1 - x)
    return 1 / (1 + np.exp(-x))

def get_syns(xinp, yinp, syn0_var, syn1_var):
    X = xinp
    y = yinp
    np.random.seed(1)
    syn0 = syn0_var
    syn1 = syn1_var
    l2 = None
    for j in range(80000):
        # Feed forward through layers 0, 1, and 2
        l0 = X
        l1 = nonlin(np.dot(l0, syn0))
        l2 = nonlin(np.dot(l1, syn1))

        # how much did we miss the target value?
        l2_error = y - l2

        if (j % 10000) == 0:
            print("Error:" + str(np.mean(np.abs(l2_error))))

        # in what direction is the target value?
        # were we really sure? if so, don't change too much.
        l2_delta = l2_error * nonlin(l2, deriv=True)

        # how much did each l1 value contribute to the l2 error (according to the weights)?
        l1_error = l2_delta.dot(syn1.T)

        # in what direction is the target l1?
        # were we really sure? if so, don't change too much.
        l1_delta = l1_error * nonlin(l1, deriv=True)

        syn1 += l1.T.dot(l2_delta)
        syn0 += l0.T.dot(l1_delta)

    syn0_var = syn0
    syn1_var = syn1

    # make round to l2
    #for k in range(l2.size()-1):
    #    print("k=",k)
    err_cnt = 0
    for elm_res,elm_y in zip(l2, yinp):
        if int(round(elm_res[0])) != int(elm_y[0]):
            err_cnt += 1
            print("*   ", int(round(elm_res[0])), " ", int(elm_y[0]))
        else:
            print("   ", int(round(elm_res[0])), " ", int(elm_y[0]))
    print("err_cnt=",err_cnt)
    if err_cnt != 0:
        return 0
    else:
        return 1

def predict_output(xinp, syn0_var, syn1_var):
    '''
    :return: predicted value as a function of input vector.
    '''
    X = xinp
    syn0 = syn0_var
    syn1 = syn1_var
    l2 = None
    l0 = X
    l1 = nonlin(np.dot(l0, syn0))
    l2 = nonlin(np.dot(l1, syn1))
    return l2

