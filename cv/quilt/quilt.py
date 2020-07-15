import cv2
import numpy as np
import time


def get_random_block(patch, block_size):
    hs, ws = patch.shape[:2]
    b = block_size
    u, v = np.random.randint((0, 0), (ws - b, hs - b))
    block = patch[v: v + b, u: u + b]               
    return block


def compute_ssd(target_image, block, block_size, overlap_size, row, col):
    I, J = row, col    
    img = target_image
    b, s = block_size, overlap_size
    pI, pJ = I * (b - s), J * (b - s)

    # For block (0, 0), nothing to compute, return random block
    if I == J == 0:  
        return 0.

    # For top row, consider only left overlap        
    if I == 0:  
        d_left = block[0: b, 0: s] - img[0: b, pJ: pJ + s] 
        ssd = np.sum(d_left * d_left)
    # For left column, consider only top overlap        
    elif J == 0:  
        d_top = block[0: s, 0: b] - img[pI: pI + s, 0: b] 
        ssd = np.sum(d_top * d_top)
    # For interior blocks consider left, rop and corner overlaps        
    else:  
        d_top = block[0: s, s: b] - img[pI: pI + s, pJ + s: pJ + b]
        d_left = block[s: b, 0: s] - img[pI + s: pI + b, pJ: pJ + s]        
        d_corner = block[0: s, 0: s] - img[pI: pI + s, pJ: pJ + s] 
        ssd = np.sum(d_top * d_top) + np.sum(d_left * d_left) + np.sum(d_corner * d_corner)

    return ssd

def carve(slice_img, slice_block):
    assert slice_img.shape == slice_block.shape    
    b, s = slice_img.shape[:2]
    diff = (slice_img - slice_block)
    error = np.mean(diff * diff, axis=2)
    cost = np.zeros(error.shape)

    # Compute cost matrix
    cost[0, :] = error[0, :]
    for i in range(1, b):
        for j in range(0, s):
            if j == 0:
                cost[i, j] = error[i, j] + min(cost[i - 1, j], cost[i - 1, j + 1])
            elif j == s - 1:
                cost[i, j] = error[i, j] + min(cost[i - 1, j - 1], cost[i - 1, j])
            else:
                cost[i, j] = error[i, j] + min(cost[i - 1, j - 1], cost[i - 1, j], cost[i - 1, j + 1])

    # Backtrack and calculate seam
    seam = np.zeros((b, ), dtype=np.int)
    seam[b - 1] = cost[b - 1, :].argmin()
    for i in range(b - 2, -1, -1):
        j_prev = seam[i + 1]

        if j_prev == 0:
            j_list = [0, 1]                    
        elif j_prev == s - 1:
            j_list = [s - 2, s - 1]            
        else:        
            j_list = [j_prev - 1, j_prev, j_prev + 1]            

        idx = np.argmin([cost[i, j_] for j_ in j_list])        
        seam[i] = j_list[idx]
    
    # Construct carved overlap region    
    new_slice = slice_img.copy()
    for i in range(b):
        j = seam[i]        
        new_slice[i, j:, :] = slice_block[i, j:, :]

    return new_slice, seam, cost

def carve_left(target_image, block, block_size, overlap_size, block_row, block_col):
    I, J = block_row, block_col    
    img = target_image
    b, s = block_size, overlap_size        
    pI, pJ = I * (b - s), J * (b - s)
    slice_img = img[pI: pI + b, pJ: pJ + s]
    slice_block = block[0: b, 0: s]
    new_slice, seam, cost = carve(slice_img, slice_block)
    return new_slice, seam, cost


def carve_top(target_image, block, block_size, overlap_size, block_row, block_col):
    I, J = block_row, block_col    
    img = target_image
    b, s = block_size, overlap_size        
    pI, pJ = I * (b - s), J * (b - s)
    slice_img = img[pI: pI + s, pJ: pJ + b]
    slice_block = block[0: s, 0: b]

    slice_img = np.rot90(slice_img)
    slice_block = np.rot90(slice_block)
    new_slice, seam, cost = carve(slice_img, slice_block)
    new_slice = np.rot90(new_slice, -1)
    cost = np.rot90(cost, -1)
    return new_slice, seam, cost


def carve_seam(target_image, block, block_size, overlap_size, block_row, block_col):
    I, J = block_row, block_col
    b, s = block_size, overlap_size
    args = target_image, block, block_size, overlap_size, block_row, block_col
    # No left or top carving for the first block
    if I == J == 0:
        return block

    # For blocks to the right of the first block, left carving is always performed
    if J > 0:
        ov_left, seam_left, cost_left = carve_left(*args)
        block[:b, :s] = ov_left

    # For blocks below the first block, top carving is always performed
    if I > 0:
        ov_top, seam_top, cost_top = carve_top(*args)
        block[:s, :b] = ov_top

    # Decide if top or left overlap region is better in the corner
    if (I > 0) and (J > 0):
        if cost_left[s-1, seam_left[s-1]] <= cost_top[seam_top[s-1], s-1]:
            block[:b, :s] = ov_left
        else:
            block[:s, :b] = ov_top

    return block

def find_best_block_random(target_image, patch, block_size, overlap_size, block_row, block_col):
    I, J = block_row, block_col
    b, s = block_size, overlap_size

    best_ssd = np.inf
    best_block = None
    for num_trials in range(1000):
        # Select candidate block (random block from patch)
        block = get_random_block(patch, b)
        ssd = compute_ssd(target_image, block, b, s, I, J)
        if ssd < best_ssd:
            best_ssd = ssd            
            best_block = block.copy()

    return best_block, best_ssd

def find_best_block_exhaustive(target_image, patch, block_size, overlap_size, block_row, block_col):
    I, J = block_row, block_col
    b, s = block_size, overlap_size
    patch_height, patch_width = patch.shape[:2]

    best_ssd = np.inf
    best_block = None
    for i in range(patch_height - block_size):
        for j in range(patch_width - block_size):
            block = patch[i : i + b, j: j + b]
            ssd = compute_ssd(target_image, block, block_size, overlap_size, I, J)
            if ssd < best_ssd:
                best_ssd = ssd            
                best_block = block.copy()

    return best_block, best_ssd

def main():
    t1 = time.time()
    patch = cv2.imread('sample2.png')
    hs, ws, c = patch.shape
    # init_block_size = min(hs, ws) // 2
    init_block_size = 60
    block_size = b = 6 * (init_block_size // 6)
    overlap_size = s = block_size // 6
    init_target_size = 512
    num_blocks = 1 + np.ceil((init_target_size - b) // (b - s))
    num_blocks = int(num_blocks)
    target_size = b + (num_blocks - 1) * (b - s)
    print('target_size: ', target_size)
    print('block_size: ', block_size)
    print('overlap_size: ', overlap_size)
    print('num_blocks: ', num_blocks)

    target_img_random = np.zeros((target_size, target_size, c), dtype=np.int)
    target_img_ssd = np.zeros((target_size, target_size, c), dtype=np.int)
    target_img_carved = np.zeros((target_size, target_size, c), dtype=np.int)

    # Form target image using random blocks    
    for row in range(num_blocks):
        pI = row * (b - s)
        for col in range(num_blocks):            
            pJ = col * (b - s)
            print('row: {row}/{num}, col: {col}/{num}'.format(row=row, col=col, num=num_blocks))
            # Add block to random image (which is just being generated for comparison)
            target_img_random[pI: pI + b, pJ: pJ + b, :] = get_random_block(patch, b)

            # Synthesize next block of SSD image
            block_ssd, _ = find_best_block_exhaustive(target_img_ssd, patch, b, s, row, col)
            target_img_ssd[pI: pI + b, pJ: pJ + b, :] = block_ssd

            # Seam carving
            block_carved = carve_seam(target_img_carved, block_ssd, b, s, row, col)
            target_img_carved[pI: pI + b, pJ: pJ + b, :] = block_carved

    cv2.imwrite('random.jpg', target_img_random)
    cv2.imwrite('ssd.jpg', target_img_ssd)
    cv2.imwrite('carved.jpg', target_img_carved)
    print('Conversion took {} seconds'.format(time.time() - t1))

if __name__ == '__main__':
    main()




