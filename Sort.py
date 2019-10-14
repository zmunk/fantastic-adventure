import random
import time

def disp(inp_list):
    print("".join(inp_list))

def selection_sort(inp):
    """ Selection Sort """
    inp_list = inp[:]
    # disp(inp_list)
    for i in range(len(inp_list) - 1):
        # find index of item with smallest value
        min_val = inp_list[i]
        min_ind = i
        for ind, val in enumerate(inp_list[i:], start=i):
            if val < min_val:
                min_ind, min_val = ind, val
        if i == min_ind:
            continue
        # swap i-th item with next smallest item
        inp_list[i], inp_list[min_ind] = inp_list[min_ind], inp_list[i]
        # disp(inp_list)

def insertion_sort(inp):
    """ Insertion Sort """
    inp_list = inp[:]
    # disp(inp_list)
    for i in range(1, len(inp_list)):
        for j in range(i, 0, -1):
            if inp_list[j] < inp_list[j - 1]:
                # swap i - 1 and 5
                inp_list[j - 1], inp_list[j] = inp_list[j], inp_list[j - 1]
            # disp(inp_list)

def shell_sort(inp):
    """ Shell Sort """
    inp_list = inp[:]
    # disp(inp_list)
    n = len(inp_list)
    h = 1
    while h < n // 3: h = 3 * h + 1
    while h > 0:
        border = h
        while border < n:
            ind_b = border
            ind_a = border - h
            while ind_a >= 0:
                if inp_list[ind_b] < inp_list[ind_a]:
                    # swap a and b
                    inp_list[ind_b], inp_list[ind_a] = inp_list[ind_a], inp_list[ind_b]
                    # disp(inp_list)
                ind_a -= h
                ind_b -= h
            border += 1
        h //= 3

def merge(arr_a, arr_b):
    # merges two ordered arrays
    output = []
    while True:
        if len(arr_a) == 0:
            arr = arr_b
            break
        if len(arr_b) == 0:
            arr = arr_a
            break
        arr = arr_a if arr_a[0] < arr_b[0] else arr_b
        output.append(arr.pop(0))
    output.extend(arr)
    return output

def merge_sort(inp):
    """ Merge Sort """
    inp_list = inp[:]
    n = len(inp_list)
    if n <= 1:
        return inp_list
    split = n // 2
    return merge(merge_sort(inp_list[:split]), merge_sort(inp_list[split:]))

def quick_sort_sort(inp_list):
    n = len(inp_list)
    if n <= 1:
        return inp_list
    v = inp_list[0]
    i, j = 1, len(inp_list) - 1
    while True:
        while i < n - 1 and inp_list[i] < v: i += 1
        while j > 0     and inp_list[j] > v: j -= 1
        if i >= j:
            break
        inp_list[i], inp_list[j] = inp_list[j], inp_list[i]
        i += 1
        j -= 1
    inp_list[0], inp_list[j] = inp_list[j], inp_list[0]
    return quick_sort_sort(inp_list[:j]) + [v] + quick_sort_sort(inp_list[j + 1:])

def quick_sort(inp):
    """ Quick Sort """
    inp_list = inp[:]
    random.shuffle(inp_list)
    return quick_sort_sort(inp_list)

if __name__ == "__main__":
    a = "S O R T I N G A L G O R I T H M S C O M P A R I S O N W I T H T I M E R".split()

    # t = time.time()
    # sel = selection_sort(a)
    # print("selection sort took: {}".format(time.time() - t))

    # t = time.time()
    # ins = insertion_sort(a)
    # print("selection sort took: {}".format(time.time() - t))

    # t = time.time()
    # shell = shell_sort(a)
    # print("selection sort took: {}".format(time.time() - t))

    # t = time.time()
    # merge = merge_sort(a)
    # print("selection sort took: {}".format(time.time() - t))
    
    t = time.time()
    quick = quick_sort(a)
    print("selection sort took: {:.15f}".format(time.time() - t))

    # if (sel == ins and ins == shell and shell == merge and merge == quick):
    #     disp(sel)
