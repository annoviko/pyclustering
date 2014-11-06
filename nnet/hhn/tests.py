import unittest;

from nnet.hhn import hhn_network;

class Test(unittest.TestCase):
    def testName(self):
        net = hhn_network(10);

if __name__ == "__main__":
    unittest.main();