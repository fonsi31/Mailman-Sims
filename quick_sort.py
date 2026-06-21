def quick_sort(arr, low, high):
    if low >= high:
        return arr
    pv = low #pivot index
    i = pv + 1
    j = high
    while i <= j:
        if arr[i] > arr[pv]:
            if arr[j] < arr[pv]:
                temp = arr[i]
                arr[i] = arr[j]
                arr[j] = temp
                i += 1
                j -= 1
            else:
                j -= 1
        else:
            i += 1
    temp1 = arr[pv]
    arr[pv] = arr[j]
    arr[j] = temp1 #the array is now divided into 2 ends
    quick_sort(arr, low, j-1) #left side
    quick_sort(arr, j+1, high) #right side

arr = [5,5,1,5,5]
quick_sort(arr, 0, len(arr)-1)
print(arr)