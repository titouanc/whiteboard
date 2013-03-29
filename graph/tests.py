"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from graph.models import Node, Taggable

class SimpleTest(TestCase):
    """
    All tests are made in this graph:
    A -> B -> C -> D;
    A -> D;
    """
    def setUp(self):
        self.a, self.b, self.c, self.d = (Node() for i in range(4))
        a.attach(b)
        b.attach(c)
        c.attach(d)
        a.attach(d)
    
    
    def testNoCycle(self):
        self.assertFalse(self.d.attach(a), 'Direct cycle')
        self.assertFalse(self.c.attach(a), 'Indirect cycle')
