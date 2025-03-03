import os

def compare(file1: str, file2: str) -> bool:
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        while True:
            chunk1 = f1.read()
            chunk2 = f2.read()
            if chunk1 > chunk2:
                return False
            if not chunk1:  
                return True
                

def natural_merge_sort(arr):
    runs = []
    start = 0
    while start < len(arr):
        end = start + 1
        while end < len(arr) and compare(arr[end - 1], arr[end]):
            end +=1
        runs.append(arr[start:end])
        start = end
    
    while len(runs) > 1:
        new_runs = []
        for i in range(0, len(runs), 2):
            if i + 1 < len(runs):
                new_runs.append(merge(runs[i], runs[i+1]))
            else:
                new_runs.append(runs[i])
        runs = new_runs 
    return runs[0] if runs else []


def merge(left, right):
    sorted_arr = []
    i = 0
    j = 0
    while i < len(left) and j< len(right):
        if compare(left[i], right[j]):
            sorted_arr.append(left[i])
            i+=1
        else:
            sorted_arr.append(right[j])
            j+=1
    sorted_arr.extend(left[i:])
    sorted_arr.extend(right[j:])
    return sorted_arr

path1 = "D:/Infotecs/file1.txt"
path2 = "D:/Infotecs/file2.txt"
path3 = "D:/Infotecs/file3.txt"


file1 = os.path.basename(path1)
file2 = os.path.basename(path2)
file3 = os.path.basename(path3)

arr = [file1, file2, file3]

natural_merge_sort(arr)