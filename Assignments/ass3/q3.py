"""
requirements:

```
$ pip install git+https://github.com/Nanguage/suffix-trees
```

"""

import os
from suffix_trees import STree, visualize
from Bio.Seq import reverse_complement


if __name__ == "__main__":
    s1 = "AAAACGTCGGGATCG"
    s2 = "GGGCGTAAAGCTCT"
    T = STree.STree([s1, s2])
    Tv = visualize.VisualizeTree(T)
    dot = Tv.to_graphviz()
    dot.save("img/q3.dot")
    os.system("dot -Tpdf img/q3.dot > img/q3.pdf")

    s1_rc = reverse_complement(s1)
    s2_rc = reverse_complement(s2)
    T = STree.STree([s1_rc, s2_rc])
    Tv = visualize.VisualizeTree(T)
    dot = Tv.to_graphviz()
    dot.save("img/q3-rc.dot")
    os.system("dot -Tpdf img/q3-rc.dot > img/q3-rc.pdf")