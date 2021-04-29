def merge(arr1, arr2):        
    m = len(arr1)
    n = len(arr2)
    merged = [0] * (m + n)
    i = j = k = 0

    while (i < m) and (j < n):
        if arr1[i] < arr2[j]:
            merged[k] = arr1[i]
            i += 1
            k += 1
        else:
            merged[k] = arr2[j]
            j += 1
            k += 1

    # Add remaining elements of arr1
    while i < m:    
        merged[k] = arr1[i]
        i += 1
        k += 1

    # Add remaining elements of arr2
    while j < n:
        merged[k] = arr2[j]
        j += 1
        k += 1

    return merged

def mergesort(arr):
    if len(arr) == 1:
        return arr

    n = len(arr) // 2
    left = mergesort(arr[:n])
    right = mergesort(arr[n:])
    return merge(left, right)

def main():
    from random import randint
    arr = [randint(-1000, 1000) for _ in range(randint(10, 100))]
    print(arr)
    arr = mergesort(arr)
    print("Sorted array is:")
    print(arr)

if __name__ == '__main__':
    main()
