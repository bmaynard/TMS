import unittest
import sys
sys.path.append(sys.path[0] + "/../")

TEST_MODULES = [
			'db_test',
			'http_test'
]

def suite():
    return unittest.TestLoader().loadTestsFromNames(TEST_MODULES)

if __name__ == "__main__":
    unittest.main(defaultTest="suite")