import sys

from main import main

# arg1 = chip , arg2 = net
print("Not found: ", main(sys.argv[1], sys.argv[2], 2, 0, 1, True))