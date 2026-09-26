"""Log a human intervention. usage: python tools/human.py p2 c1 "what you did and why" """
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import log

if len(sys.argv) < 4:
    sys.exit(__doc__)
print(log(sys.argv[1], sys.argv[2], "human", note=" ".join(sys.argv[3:]), who=os.environ.get("USER", "?")))
