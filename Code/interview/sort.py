# coding=utf-8


def bubble_sort(nums):
    for i in range(len(nums)):
        for j in range(len(nums) - i - 1):
            if nums[i] > nums[j]:
                nums[i], nums[j] = nums[j], nums[i]


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
