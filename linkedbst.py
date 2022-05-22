"""
File: linkedbst.py
Author: Ken Lambert
"""

from random import shuffle
from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from math import log
import time
from tqdm import tqdm
import sys


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            string = ""
            if node != None:
                string += recurse(node.right, level + 1)
                string += "| " * level
                string += str(node.data) + "\n"
                string += recurse(node.left, level + 1)
            return string

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        node = self._root
        while True:
            if node is None:
                return node
            elif item > node.data:
                node = node.right
            elif item < node.data:
                node = node.left
            else:
                return item

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""
        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            node = self._root
            while True:
                if item >= node.data:
                    if node.right == None:
                        node.right = BSTNode(item)
                        break
                    else:
                        node = node.right
                else:
                    if node.left == None:
                        node.left = BSTNode(item)
                        break
                    else:
                        node = node.left
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def lift_max_left(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            current_node = top.left
            while not current_node.right == None:
                parent = current_node
                current_node = current_node.right
            top.data = current_node.data
            if parent == top:
                top.left = current_node.left
            else:
                parent.right = current_node.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = 'L'
        current_node = self._root
        while not current_node == None:
            if current_node.data == item:
                item_removed = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = 'L'
                current_node = current_node.left
            else:
                direction = 'R'
                current_node = current_node.right

        # Return None if the item is absent
        if item_removed == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not current_node.left == None \
                and not current_node.right == None:
            lift_max_left(current_node)
        else:

            # Case 2: The node has no left child
            if current_node.left == None:
                new_child = current_node.right

                # Case 3: The node has no right child
            else:
                new_child = current_node.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return item_removed

    def replace(self, item, new_item):
        """
        If item is in self, replaces it with new_item and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                old_data = probe.data
                probe.data = new_item
                return old_data
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def is_leaf(self, node):
        '''Function to determine if node is a leaf'''
        if node == None:
            return True
        return node.left is None and node.right is None

    def children(self, node):
        '''Returns list of node's children'''
        if node == None:
            return []
        return [node.left, node.right]

    def _height_rec(self, top):
        '''
        Helper function
        :param top:
        :return:
        '''
        if self.is_leaf(top):
            return 0
        else:
            return 1 + max(self._height_rec(child) for child in self.children(top))

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''
        if self._root is not None:
            return self._height_rec(self._root)
        return 0

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        return self.height() < (2 * log(self._size + 1) - 1)

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        result = []
        for node in self.inorder():
            if node >= low and node <= high:
                result.append(node)
            if node > high:
                break
        return result

    def _balance_rec(self, nodes):
        if nodes == []:
            return None
        else:
            index = len(nodes) // 2
            center = nodes[index]
            self.add(center)
            del nodes[index]
            return self._balance_rec(nodes[:index]), self._balance_rec(nodes[index:])

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        nodes = [item for item in self]
        self.clear()
        nodes.sort()
        self._balance_rec(nodes)

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        for node in self.inorder():
            if node > item:
                return node
        return None

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        prev_node = None
        for node in self.inorder():
            if node >= item:
                return prev_node
            prev_node = node
        return node

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        sys.setrecursionlimit(10**8)
        print('Word list establishing...', end='\n')
        with open(path, 'r', encoding='utf-8') as file:
            words = file.readlines()
            test_words = words[:]
            shuffle(test_words)
            test_words[:10000]

        NUM_OF_ITERATIONS = 10000
        print('Started search in a list')
        start = time.time()
        for i in tqdm(range(NUM_OF_ITERATIONS)):
            words.index(test_words[i])
        print(f'List search time: {time.time()-start}', end='\n\n')
        print('Building a sorted tree...', end='\n\n')
        for word in words:
            self.add(word)
        print('Started sorted tree search')
        start = time.time()
        for i in tqdm(range(NUM_OF_ITERATIONS)):
            self.find(test_words[i])
        print(f'Sorted tree search time: {time.time()-start}', end='\n\n')
        self.clear()
        shuffle(words)
        print('Building unsorted tree...', end='\n\n')
        for word in words:
            self.add(word)
        print('Started unsorted tree find')
        start = time.time()
        for i in tqdm(range(NUM_OF_ITERATIONS)):
            self.find(test_words[i])
        print(f'Unsorted tree find time: {time.time()-start}', end='\n\n')
        print('Rebalancing...', end='\n\n')
        self.rebalance()
        print('Started balanced tree find')
        start = time.time()
        for i in tqdm(range(NUM_OF_ITERATIONS)):
            self.find(test_words[i])
        print(f'Balanced tree find time: {time.time()-start}')
