import unittest
class Teste(unittest.TestCase):
    def test_basico(self):
        self.assertEqual(1+1,2)
if __name__=='__main__':
    unittest.main()