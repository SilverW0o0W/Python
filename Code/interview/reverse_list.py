#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@author: Silver (silver.codingcat@gmail.com)
@create: 2022/11/21
@brief: 翻转链表
"""

# Definition for singly-linked list.
from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def __init__(self):
        self.successor = None

    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head and not head.next:
            return head

        cur = self.reverseList(head.next)
        head.next.next = head
        head.next = None
        return cur
