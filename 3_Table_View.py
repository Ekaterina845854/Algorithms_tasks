def quicksort(arr, values):
    if len(arr) <= 1:
        return arr, values
    pivot = arr[len(arr) // 2]
    left = [(arr[i], values[i]) for i in range(len(arr)) if arr[i] < pivot]
    middle = [(arr[i], values[i]) for i in range(len(arr)) if arr[i] == pivot]
    right = [(arr[i], values[i]) for i in range(len(arr)) if arr[i] > pivot]
    
    left_sorted, left_values = quicksort([x[0] for x in left], [x[1] for x in left])
    middle_sorted, middle_values = [x[0] for x in middle], [x[1] for x in middle]
    right_sorted, right_values = quicksort([x[0] for x in right], [x[1] for x in right])
    
    return left_sorted + middle_sorted + right_sorted, left_values + middle_values + right_values

def downsample(times, values, N):

    if len(times) != len(values):
        raise ValueError("Длины times и values должны совпадать")
    if N < 2:
        raise ValueError("N >= 2")
    
    times, values = quicksort(times, values)

    step = (len(times) - 1) / (N - 1)
    indices = [round(i * step) for i in range(N)]
    new_times = [times[i] for i in indices]

    new_values = [values[0]]
    for i in range(1, N - 1):
        start, end = indices[i-1], indices[i + 1] 
        avg_value = sum(values[start : end + 1]) / (end - start + 1)  
        new_values.append(avg_value)
    new_values.append(values[-1]) 

    return new_times, new_values