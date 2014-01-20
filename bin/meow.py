import sys
import os

sys.path.append(os.path.dirname(sys.path[0]))

from rita import rita

if __name__ == '__main__':
	r = rita.Rita()
	print r 