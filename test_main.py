from app import *
import unittest,requests

class TestResponse(unittest.TestCase):
    def test_request(self):
        url = input("Please write your file url:")
# c:/...
        try:
            with open(url, "r") as f:
                while True:
                    line1 = [line.rstrip("\n") for line in f]
                    line2 = [line.rstrip("\n") for line in f]
                    re=requests.get(line1)
                    print(re)
                    print(self.assertEqual(re,line2))
                    if not line2: break
            f.close()
        except IOError:
            return "Could not read file"
        return 'ALL_PASSED'

if __name__ == '__main__':
    unittest.main()