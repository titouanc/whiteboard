"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from graph.models import Node, Leaf, Taggable, CannotHaveChildren

class SimpleTest(TestCase):
    def mkNode(self, name, klass=Node):
        """Helper function to easily create nodes or inherited"""
        return klass.objects.create(name=name)
    
    
    def testAttach(self):
        """
        A -> B -> C -> D
        A -> D
        A -> E -> B
        """
        a, b, c, d, e = (self.mkNode(chr(ord('A')+i)) for i in range(5))
        ### AdventureTime !
        self.assertTrue(a.attach(b) and b.attach(c) and c.attach(d), 'Construct basic graph')
        self.assertTrue(a.attach(d), 'Another path')
        self.assertTrue(a.attach(e), 'Attach single new node')
        self.assertTrue(e.attach(b), 'Insert reference from new node')
        self.assertFalse(d.attach(a), 'Direct loop')
        self.assertFalse(c.attach(e), 'Indirect loop')
        self.assertTrue(c.attach(e, False), 'Force attach with loop')
    
    
    def testLeaves(self):
        leaf = self.mkNode("Leaf", Leaf)
        node = self.mkNode("Node")
        self.assertRaises(CannotHaveChildren, leaf.attach, node, msg='Leaf cannot have child')
    
    def testReachablility(self):
        """
        Test some reachability methods on a simple graph
        A -> B -> E
        A -> C -> D
        C -> E
        """
        a, b, c, d, e = (self.mkNode(chr(ord('A')+i)) for i in range(5))
        a.attach(b) and b.attach(e)
        a.attach(c) and c.attach(d)
        c.attach(e)
        ### AdventureTime !
        self.assertTrue(e.has_ancestor(c), 'Direct parent->child relation')
        self.assertTrue(e.has_ancestor(b), 'Direct parent->child relation (alt)')
        self.assertTrue(e.has_ancestor(a), 'Grandfather->grandchild relation')
        self.assertFalse(d.has_ancestor(b), 'No relation')
    
    
    def testRelated(self):
        avl = self.mkNode('AVL', Taggable)
        avl.add_keywords('bst', 'tree', 'balanced')
        splice = self.mkNode('Splice game', Taggable)
        splice.add_keywords('tree', 'game')
        poney = self.mkNode('My Little Poney', Taggable)
        poney.add_keywords('poney', 'Bram', 'bot', 'irc')
        ### AdventureTime !
        self.assertIn(splice, avl.related(), 'Basic tag-based relation')
        self.assertNotIn(poney, avl.related(), 'Basic tag-based no-relation')
    
