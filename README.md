# Project 2 - Xiaowen Li


## Instruction

This project was written in Python 3.9, compiles through Windows cmd with parameters to indicate the input and output file name.

```bash
C:\Location>python Project2.py small.txt small-soln.txt
C:\Location>python Project2.py medium.txt medium-soln.txt
C:\Location>python Project2.py large.txt large-soln.txt
```

To verify the output, use the verifyGraph.py script.
```bash
C:\Location>python Project2.py large.txt large-soln.txt
C:\Location>python verifyGraph.py large.txt large-soln.txt
Path is correct.
```
## Packages
```python
import sys
import numpy 
from collections import defaultdict
```
