import sys
from dataclasses import dataclass

lines = [line.rstrip() for line in sys.stdin.readlines()]


class Node:
    def __init__(self, data, next, prev):
        self.data: int = data
        self.next = next
        self.prev = prev


dummy = Node(999, None, None)

nodes = [dummy]
for (idx, line) in enumerate(lines):
    num = int(line)
    node = Node(num, next=None, prev=nodes[-1])
    nodes.append(node)
    nodes[-2].next = node

nodes[-1].next = dummy
dummy.prev = nodes[-1]


def printList(strt: Node):
    global dummy
    node = strt
    if node is dummy:
        node = node.next
    while node is not None and node is not dummy:
        print(node.data, end=", ")
        node = node.next
    print()


def insertAfter(to_add: Node, offset: int):
    global dummy, added, indices
    curr = to_add
    deleteNode(curr)
    if offset == 0:
        tmp = dummy.next
        to_add.next = tmp
        dummy.next = to_add
        to_add.prev = dummy
    while offset > 0:
        curr = curr.next
        if curr is dummy:
            curr = curr.next
        offset -= 1

    while offset < 0:
        curr = curr.prev
        if curr is dummy:
            curr = curr.prev
        offset += 1

    tmp = curr.next
    curr.next = to_add
    to_add.prev = curr
    to_add.next = tmp
    tmp.prev = to_add


def deleteNode(node: Node):
    global dummy
    if node is dummy:
        print(f"cant delete dummy")
        return
    tmp = node.next
    node.prev.next = tmp
    tmp.prev = node.prev
    # del node


# print(nodes)
# printList(dummy)
for (idx, node) in enumerate(nodes[1:]):
    insertAfter(node, node.data if node.data > 0 else node.data - 1)


def findZero():
    global dummy
    curr = dummy
    while curr:
        if curr.data == 0:
            return curr
        curr = curr.next


# deleteNode(nodes[-1])
printList(dummy)
# insertAfter(nodes[2], -3)
# printList(dummy)
zero = findZero()
count = 0
breakpoints = [1000, 2000, 3000]
curr = zero
running = 0
while count < 4000:
    curr = curr.next
    if curr is dummy:
        curr = curr.next
    count += 1
    if count in breakpoints:
        running += curr.data
        # print(curr.data, end=" ")

print(running)
