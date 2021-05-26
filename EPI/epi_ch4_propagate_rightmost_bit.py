def propagateRightmostBit(x):
    """
    Should turn 01010000 to 01010000
    """
    y = (x & ~(x - 1)) - 1
    return x + y


def computeModuloPowerOfTwo(x, pow2):
    """
    e.g

    computeModuloPowerOfTwo(77, 64) = 13. 
    """
    return x & (pow2 - 1)

def isPowerOfTwo(x):    
    return x and x & (x - 1) == 0