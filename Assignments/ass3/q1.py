"""
requirements:

```
$ pip install git+https://github.com/Nanguage/suffix-trees
```

"""

import os
from suffix_trees import STree, visualize


if __name__ == "__main__":
    s1 = "ACGT"
    s2 = "TGCA"
    T = STree.STree([s1, s2])
    Tv = visualize.VisualizeTree(T)
    dot = Tv.to_graphviz()
    dot.save("img/q1.dot")
    os.system("dot -Tpdf img/q1.dot > img/q1.pdf")
