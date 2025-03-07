import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram

def load_data(filepath):
    toReturn = []
    with open (filepath, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            toReturn.append(row)
    return toReturn

def calc_features(row):
    x = np.zeros((9,), dtype = float)
    for i, key in enumerate(row.keys()):
        if i > 0:
            x[i-1] = float(row[key])
    return x

def hac(features):

    arr = np.array(features, dtype=float)
    arr_length = len(arr)

    distance_matrix = np.zeros((2*arr_length - 1, 2*arr_length - 1))
    for i in range(arr_length):
        for j in range(arr_length):
            distance_matrix[i,j] = np.linalg.norm(arr[i] - arr[j])

    found = []
    for i in range(arr_length):
        found.append(True)
    
    arr_sizes = []
    for i in range(arr_length):
        arr_sizes.append(1)

    toReturn = np.zeros((arr_length - 1, 4))
    curr = arr_length

    for iter in range(arr_length - 1):
        optimal = float('inf')
        left_index = -1
        right_index = -1
        for i in range(curr):
            if found[i] and i < len(found):
                for j in range(i + 1, curr):
                    if found[j] and j < len(found):
                        distance = distance_matrix[i,j]

                        if distance < optimal:
                            left_index, right_index = i, j
                            optimal = distance
                        
                        elif abs(distance - optimal) < 1e-12:
                            if i < left_index or (i == left_index and j < right_index):
                                left_index, right_index = i, j
        
        if left_index > right_index: 
            left_index, right_index = right_index, left_index

        toReturn[iter,0] = left_index
        toReturn[iter,1] = right_index

        toReturn[iter,2] = optimal
        toReturn[iter,3] = arr_sizes[left_index] + arr_sizes[right_index]

        found[left_index] = False
        found[right_index] = False

        arr_sizes.append(toReturn[iter,3])

        for t in range(curr):
            if t < len(found) and found[t]:
                distance = max(distance_matrix[left_index,t], distance_matrix[right_index,t])
                distance_matrix[curr,t] = distance
                distance_matrix[t,curr] = distance

        left_index = curr
        curr += 1

        found.append(True)

    return toReturn

def normalize_features(features):
    toReturn = []
    arr = np.array(features, dtype=float)
    standard_deviation = np.std(arr, axis=0)

    mean = np.mean(arr, axis=0)
    
    for i in range(len(arr)):
        toReturn.append((arr[i] - mean) / standard_deviation)

    return toReturn

def fig_hac(Z, names):
    figure = plt.figure()
    plt.tight_layout()
    dendrogram(Z, labels=names, leaf_rotation=90)
    return figure

if __name__ == "__main__":
    data = load_data("Country-data.csv")
    features = [calc_features(row) for row in data]
    names = [row["country"] for row in data]
    features_normalized = normalize_features(features)
    np.savetxt("output.txt", features_normalized)
    n = 20
    Z = hac(features[:n])
    fig = fig_hac(Z, names[:n])
    plt.show()
