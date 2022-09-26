# coding=utf-8


def bubble_sort(nums):
    for i in range(len(nums) - 1):
        for j in range(len(nums) - i - 1):
            if nums[j] > nums[j + 1]:
                nums[j + 1], nums[j] = nums[j], nums[j + 1]


def quick_sort(nums):
    quicksort(nums, 0, len(nums) - 1)


def quicksort(nums, low, high):
    if low >= high:
        return
    i, j = low, high
    key = nums[i]
    while i < j:
        while i < j and nums[j] >= key:
            j = j - 1
        nums[i] = nums[j]
        while i < j and nums[i] <= key:
            i = i + 1
        nums[j] = nums[i]
    nums[i] = key
    quicksort(nums, low, i - 1)
    quicksort(nums, j + 1, high)


def quick_sort2(nums):
    if len(nums) < 2:
        return nums
    else:
        p = nums[0]
        less = [num for num in nums[1:] if num < p]
        greater = [num for num in nums[1:] if num >= p]
        return quick_sort2(less) + [p] + quick_sort2(greater)


def select_sort(nums):
    for i in range(len(nums)):
        min = i
        for j in range(i + 1, len(nums)):
            if nums[min] > nums[j]:
                min = j
        nums[min], nums[i] = nums[i], nums[min]


def insert_sort(nums):
    for i in range(len(nums)):
        ins, signal = nums[i], i - 1
        while signal >= 0 and ins < nums[signal]:
            nums[signal + 1] = nums[signal]
            signal -= 1
        nums[signal + 1] = ins


def heap_sort(nums):
    for start in range((len(nums) - 2) / 2, -1, -1):
        heap_adjust(nums, start, len(nums) - 1)

    for end in range(len(nums) - 1, 0, -1):
        nums[0], nums[end] = nums[end], nums[0]
        heap_adjust(nums, 0, end - 1)
    return nums


def heap_adjust(nums, start, end):
    root = start
    while True:
        child = 2 * root + 1
        if child > end:
            break
        if child + 1 <= end and nums[child] < nums[child + 1]:
            child += 1
        if nums[root] < nums[child]:
            nums[root], nums[child] = nums[child], nums[root]
            root = child
        else:
            break


if __name__ == '__main__':
    nums = [2, 3, 1, 5, 2, 4, 6]
    # bubble_sort(nums)
    # quick_sort(nums)
    # nums = print(quick_sort2(nums))
    # select_sort(nums)
    # insert_sort(nums)
    heap_sort(nums)
    print(nums)
