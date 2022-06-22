#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from geektrust import Process

class test_Process(unittest.TestCase):
  
    
        
    def test_start_subs(self):
        o=Process()
        r=o.start_subs('START_SUBSCRIPTION 20-02-2022'.split())        
        self.assertEqual(r,1)
        
        
    def test_add_subscription(self):
        o=Process()
        r=o.add_subscription('ADD_SUBSCRIPTION MUSIC PESONAL'.split()) 
        self.assertEqual(r,0)
        r=o.add_subscription('ADD_SUBSCRIPTION MUSIC PERSONAL'.split()) 
        self.assertEqual(r,0)
        r=o.add_subscription('ADD_SUBSCRIPTION MUSIC PERSONAL'.split())
        self.assertEqual(r,0)
        r=o.start_subs('START_SUBSCRIPTION 20-02-2022'.split())
        self.assertEqual(r,1)
        r=o.add_subscription('ADD_SUBSCRIPTION MUSIC PERSONAL'.split()) 
        self.assertEqual(r,1)
        r=o.add_subscription('ADD_SUBSCRIPTION MUSIC PERSONAL'.split())
        self.assertEqual(r,'ADD_SUBSCRIPTION_FAILED DUPLICATE_CATEGORY')
    
    def test_add_topup(self):
        o=Process()
        r=o.add_topup('ADD_TOPUP  FOUR_DEVICE 3'.split()) 
        self.assertEqual(r,'ADD_TOPUP_FAILED SUBSCRIPTIONS_NOT_FOUND')
        
        r=o.start_subs('START_SUBSCRIPTION 20-02-2022'.split())
        self.assertEqual(r,1)
        r=o.add_subscription('ADD_SUBSCRIPTION MUSIC PERSONAL'.split()) 
        self.assertEqual(r,1)
        r=o.add_subscription('ADD_SUBSCRIPTION MUSIC PERSONAL'.split())
        self.assertEqual(r,'ADD_SUBSCRIPTION_FAILED DUPLICATE_CATEGORY')
        r=o.add_topup('ADD_TOPUP  FOUR_DEVICE 3'.split()) 
        self.assertEqual(r,1)
        
        
    def test_calculate(self):
        o=Process()        
        self.assertEqual(o.calculate(),'SUBSCRIPTIONS_NOT_FOUND')
        o.start_subs('START_SUBSCRIPTION 20-02-2022'.split()) 
        o.add_subscription('ADD_SUBSCRIPTION MUSIC PERSONAL'.split())  
        o.add_subscription('ADD_SUBSCRIPTION VIDEO PERSONAL'.split())  
        
        self.assertNotEqual(o.calculate(),'SUBSCRIPTIONS_NOT_FOUND')

if __name__=='__main__':
    unittest.main()
