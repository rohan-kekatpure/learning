class Solution:
    def computeArea(self, A, B, C, D, E, F, G, H):
        a1 = (C - A) * (D - B)
        a2 = (G - E) * (H - F)
        
        # Calculate overlaps. I got these expressions by looking at various types
        # of overlaps and finding pattern. At least I didnt find coming up with these
        # straightforward, but with experimentation, it is possible. 
        ovy = min(D, H) - max(B, F)
        ovx = min(C, G) - max(A, E)
        
        # If any one of the overlaps expressions is negative, then the rectangles are
        # completely separated. Again, you can convince yourself this by looking at
        # pictures of a few overlap types.
        if (ovx < 0) or (ovy < 0):
            a3 = 0
        else:
            a3 = ovx * ovy
        
        return a1 + a2 - a3
