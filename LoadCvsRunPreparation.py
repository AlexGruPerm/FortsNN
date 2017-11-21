import DataPreparer
import pprint
import numpy as np
import NN_Study

fn='test2.csv'
div_y = 40
chain = 7 # no less them 3
out_input_array=[]
out_res_array=[]
lx=[]
ly=[]
idxi=int(0)
with open('test2.csv', 'rb') as f:
        for line in f:
            idxi += 1
            dl = line.decode("utf-8")
            lx.append(idxi)
            ly.append(int(dl.strip().split(";")[1]))

DataPreparer.prepare_data(lx, ly, div_y, chain, out_input_array, out_res_array)

pp = pprint.PrettyPrinter(indent=(chain-1))
pp.pprint(out_input_array)
print(out_res_array)

# now data is prepared, next step is teaching NN.
#======================================================

X = np.array([elm for elm in out_input_array[:]])
#pp.pprint(X)
Y = np.array([[elm] for elm in out_res_array[:]])
#pp.pprint(Y)

syn0 = 2 * np.random.random(((chain-1), 20)) - 1
syn1 = 2 * np.random.random((20, 1)) - 1

res_quality = NN_Study.get_syns(X,Y,syn0,syn1)
print("quality of model =",res_quality)

if res_quality==1:
    print('Good model make real prediction')
    text_input = [1, 0, 1, 0, 1, 1]
    model_input = np.array([elm for elm in text_input[:]])
    pred = NN_Study.predict_output(model_input, syn0, syn1)
    print("Predicted value = ",int(round(pred[0])))
else:
    print('Fail model')

