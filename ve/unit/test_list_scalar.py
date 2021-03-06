'''
Created on Jun 21, 2020

@author: ballance
'''
import vsc
from vsc_test_case import VscTestCase
from vsc.visitors.model_pretty_printer import ModelPrettyPrinter

class TestListScalar(VscTestCase):
    
    @vsc.randobj
    class my_item_c(object):
        
        def __init__(self):
            self.fixed = vsc.rand_list_t(vsc.bit_t(8), sz=4)
            self.dynamic = vsc.randsz_list_t(vsc.bit_t(8))
            self.queue = vsc.randsz_list_t(vsc.bit_t(8))
   
    
    def test_randsz_smoke(self):
        
        @vsc.randobj
        class my_item_c(object):
            
            def __init__(self):
                self.l = vsc.randsz_list_t(vsc.uint8_t())
                
                
            @vsc.constraint
            def l_c(self):
                self.l.size in vsc.rangelist(vsc.rng(2,10))
                self.l[1] == (self.l[0]+1)
                
        it = my_item_c()
        
        it.randomize()
        
        print("it.l.size=" + str(it.l.size))
        
        for i,v in enumerate(it.l):
            print("v[" + str(i) + "] = " + str(v))

        self.assertEqual(it.l[1], it.l[0]+1)

    def test_randsz_len(self):
        
        @vsc.randobj
        class my_item_c(object):
            
            def __init__(self):
                self.l = vsc.randsz_list_t(vsc.uint8_t())
                
                
            @vsc.constraint
            def l_c(self):
                self.l.size in vsc.rangelist(vsc.rng(2,10))
                self.l[1] == (self.l[0]+1)
                
        it = my_item_c()
        
        it.randomize()
        
        self.assertGreaterEqual(len(it.l), 2)
        self.assertLessEqual(len(it.l), 10)
        
        print("it.l.size=" + str(it.l.size))
        
        for i,v in enumerate(it.l):
            print("v[" + str(i) + "] = " + str(v))

        self.assertEqual(it.l[1], it.l[0]+1)

    def test_randsz_foreach_idx(self):
        
        @vsc.randobj
        class my_item_c(object):
            
            def __init__(self):
                self.l = vsc.randsz_list_t(vsc.uint8_t())
                self.a = vsc.rand_uint8_t()
                
                
            @vsc.constraint
            def l_c(self):
                self.l.size in vsc.rangelist(vsc.rng(2,10))
                
                with vsc.foreach(self.l, it=False, idx=True) as idx:
                    with vsc.if_then(idx > 0):
                        self.l[idx] == self.l[idx-1]+1
                
        it = my_item_c()
        
        it.randomize()
        
        for i in range(len(it.l)):
            if i > 0:
                self.assertEqual(it.l[i], it.l[i-1]+1)

    def disabled_test_sum_simple(self):
        
        @vsc.randobj
        class my_item_c(object):
            
            def __init__(self):
                self.l = vsc.rand_list_t(vsc.uint8_t(), sz=5)
                self.a = vsc.rand_uint8_t()
                
            @vsc.constraint
            def sum_c(self):
                self.l.sum == 5
                
                with vsc.foreach(self.l) as it:
                    it != 0
                
        it = my_item_c()
        it.randomize()
        print("Model: " + ModelPrettyPrinter.print(it.get_model()))
        
        self.assertEqual(it.l.sum, 5)
        