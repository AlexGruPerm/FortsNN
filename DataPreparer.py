import pprint
from operator import itemgetter



def __get_avg_xw_div_ydh(lx,ly,div_y,results):
    """
    Calculate:
    1) count of intervals in X axis where y changed on dh
    2) each intervals width
    """
    ly0 = ly[0]
    lx0 = lx[0]
    cnt = 0
    for pair in zip(lx,ly):
        if abs(pair[1]-ly0) >= div_y:
            cnt+=1
            if pair[1]> ly0:
                results.append([lx0, pair[0], ly0, pair[1], 1])
            else:
                results.append([lx0, pair[0], ly0, pair[1], 0])
            lx0 = pair[0]
            ly0 = pair[1]


def prepare_data(lx, ly, div_y, chain, out_input_array, out_res_array):
    """
    :param lx: list of X values
    :param ly: list of Y values
    :param div_y : Height of y that take as a block.
    :param chain : How much blocks in chain, Ex. chain=3,
           all blocks [0,1,1,0,1,0,1,1]
           result of division, [0,1,1], [1,1,0], [1,0,1], [0,1,0]...
    :param out_input_array - matrix as list of lists - as input for NN.
    :param out_res_array   - vactor of last column (look this description)
    :return: List of lists - founded parts in source data.
      [0, 0, 0]
      [0, 1, 0]
      [1, 0, 1]
      [1, 1, 1]
     In case when we have different same lists without last elements, like
      ...
      [0, 0, 0]
      [0, 0, 1]
      [0, 0, 0]
      [0, 0, 1]
      [0, 0, 0]
      [0, 0, 0]
      ...
    we calculate counts like:
      [0, 0, 0] - 4
      [0, 0, 1] - 2
    and take list with max - [0, 0, 0]
    Results for prepared data:
     [0, 0, 0]
     [0, 1, 0]
     [1, 0, 1]
     [1, 1, 1]
     -- res 2 lists -- as source data for NN algo
     [[0, 0],
      [0, 1],
      [1, 0],
      [1, 1]]
     [0, 0, 1, 1]
     ------ Full data description ------
     -- all data divided by blocks
     [0, 0, 0, 1]
     [0, 0, 1, 0]
     [0, 1, 0, 1]
     [1, 0, 0, 0]
     [0, 1, 1, 1]
     [1, 1, 0, 1]
     [1, 0, 1, 1]
     [1, 1, 1, 1]
     -- out_input_array ----
    [[0, 0, 0],
     [0, 0, 1],
     [0, 1, 0],
     [1, 0, 0],
     [0, 1, 1],
     [1, 1, 0],
     [1, 0, 1],
     [1, 1, 1]]
    -- out_res_array ----
    [1, 0, 1, 0, 1, 1, 1, 1]
    """

    prep_array = [] # list of blocks where 5-th element (index=4) paint block as 0,1
    __get_avg_xw_div_ydh(lx, ly, div_y, prep_array) # divide source data on blocks

    #pp = pprint.PrettyPrinter(indent=(chain - 1))
    #pp.pprint(prep_array)

    prep_vector = list(map(itemgetter(4), prep_array))# take only 5-th elements of each block

    first_idx = 0
    last_idx = chain
    full_array=[]
    while last_idx <= len(prep_vector):
        full_array.append(prep_vector[first_idx:last_idx])
        first_idx += 1
        last_idx += 1

    arr_wo_last_dim_dict = [] # list without last dimension unique.
    last_elm_dist = [] #just last elmement quniue

    for elm in full_array:
        if elm[:1:-1] not in last_elm_dist:
            last_elm_dist.append(elm[:1:-1])
        if elm[0:chain-1] not in arr_wo_last_dim_dict:
            arr_wo_last_dim_dict.append(elm[0:chain-1])

    final_array = []
    for elm in arr_wo_last_dim_dict:
        arr_last_dim_with_counter = []
        for lem in last_elm_dist:
            arr_last_dim_with_counter.append(lem[0])
            e = elm.copy()
            e.append(lem[0])
            arr_last_dim_with_counter.append(full_array.count(e))
        idx_max = arr_last_dim_with_counter.index(max(arr_last_dim_with_counter[1::2])) #max by no even elements.
        final_array.append(elm)
        final_array[len(final_array)-1].append(arr_last_dim_with_counter[idx_max-1])

    l_internal = len(final_array[0])
    for i in range(len(final_array)):
        out_input_array.append(final_array[i][0:l_internal - 1])
        out_res_array.append(final_array[i][l_internal - 1])


