def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    # Swap replace the pivot to its proper index
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def quicksort_helper(arr, low, high):
    if len(arr) == 1:
        return

    if low < high:
        pivot_index = partition(arr, low, high)
        quicksort_helper(arr, low, pivot_index - 1)
        quicksort_helper(arr, pivot_index + 1, high)

def quicksort(arr):
    n = len(arr)
    quicksort_helper(arr, 0, n - 1)
  
def main():
    from random import randint
    arr = [randint(-1000, 1000) for _ in range(randint(10, 100))]
    print(arr)
    quicksort(arr)
    print("Sorted array is:")
    print(arr)

if __name__ == '__main__':
    main()