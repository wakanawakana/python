BBS for Python 
==================

This is the release of:
 - the CVPR 2015 Best-Buddies Similarity for Robust Template Matching
 - https://people.csail.mit.edu/talidekel/papers/BBS_CVPR15.pdf

License and Citation
====================

All code is provided for research purposes only and without any warranty. 

How to use:
==================
Same opencv template matching  
 ex:  
 
    template = cv2.imread('template.png')  
    search = cv2.imread('search.png')  
    bbs = BestBuddiesSimilarity()  
    pz = 3  
    gamma = 2.0  
    max_pt, max_value, res = bbs.BBS(template, search, pz, gamma)  

 
