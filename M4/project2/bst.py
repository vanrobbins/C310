"""
Binary Search Tree Implementation
Purpose: Main BST class with insert, delete, search, and traversal methods
Author: Van Robbins
"""

from tree_node import TreeNode


class BinarySearchTree:
    # BST class for inserting, deleting, searching, and traversing nodes
    
    def __init__(self):
        # make empty tree
        self.root = None
    
    def insert(self, value):
        # add element to tree
        self.root = self._insert_recursive(self.root, value)
    
    def _insert_recursive(self, node, value):
        # helper method for recursive insertion
        if node is None:
            return TreeNode(value)
        
        if value < node.value:
            node.left = self._insert_recursive(node.left, value)
        elif value > node.value:
            node.right = self._insert_recursive(node.right, value)
        # dont insert duplicates
        
        return node
    
    def delete(self, value):
        # remove a node with the value from the tree
        self.root = self._delete_recursive(self.root, value)
    
    def _delete_recursive(self, node, value):
        # helper method for recursive deletion
        if node is None:
            return None
        
        if value < node.value:
            node.left = self._delete_recursive(node.left, value)
        elif value > node.value:
            node.right = self._delete_recursive(node.right, value)
        else:
            # node to be deleted found
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            else:
                # node has two children - find inorder successor
                successor = self._find_min(node.right)
                node.value = successor.value
                node.right = self._delete_recursive(node.right, successor.value)
        
        return node
    
    def _find_min(self, node):
        # find the minimum value node in a subtree
        while node.left is not None:
            node = node.left
        return node
    
    def search(self, value):
        # find a specific element in the tree
        return self._search_recursive(self.root, value)
    
    def _search_recursive(self, node, value):
        # helper method for recursive search
        if node is None:
            return False
        
        if value == node.value:
            return True
        elif value < node.value:
            return self._search_recursive(node.left, value)
        else:
            return self._search_recursive(node.right, value)
    
    def in_order_traversal(self):
        # display all elements in the tree in in-order (sorted order)
        result = []
        self._in_order_recursive(self.root, result)
        return result
    
    def _in_order_recursive(self, node, result):
        # helper method for in-order traversal
        if node is not None:
            self._in_order_recursive(node.left, result)
            result.append(node.value)
            self._in_order_recursive(node.right, result)
    
    def pre_order_traversal(self):
        # display all elements in the tree in pre-order
        result = []
        self._pre_order_recursive(self.root, result)
        return result
    
    def _pre_order_recursive(self, node, result):
        # helper method for pre-order traversal
        if node is not None:
            result.append(node.value)
            self._pre_order_recursive(node.left, result)
            self._pre_order_recursive(node.right, result)
    
    def post_order_traversal(self):
        # display all elements in the tree in post-order
        result = []
        self._post_order_recursive(self.root, result)
        return result
    
    def _post_order_recursive(self, node, result):
        # helper method for post-order traversal
        if node is not None:
            self._post_order_recursive(node.left, result)
            self._post_order_recursive(node.right, result)
            result.append(node.value)
    
    def height(self):
        # return the height of the tree
        return self._height_recursive(self.root)
    
    def _height_recursive(self, node):
        # helper method for calculating height
        if node is None:
            return 0
        
        left_height = self._height_recursive(node.left)
        right_height = self._height_recursive(node.right)
        
        return 1 + max(left_height, right_height)
    
    def is_empty(self):
        # check if the tree is empty
        return self.root is None
