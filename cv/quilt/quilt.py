from collections import namedtuple
from pathlib import Path
import random
import cv2
import numpy as np
import time
from tqdm import trange

BlockData = namedtuple('BlockData', field_names=['row', 'col', 'ssd'])
Block = namedtuple('Block', field_names=['pixels', 'ssd'])

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

def _carve(slice_img, slice_block):
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
    min_cost = cost[b - 1, :].min()
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

    return new_slice, seam, min_cost

def carve_left(target_image, block_pixels, block_size, overlap_size, block_row, block_col):
    I, J = block_row, block_col
    img = target_image
    b, s = block_size, overlap_size
    pI, pJ = I * (b - s), J * (b - s)
    slice_img = img[pI: pI + b, pJ: pJ + s]
    slice_block = block_pixels[0: b, 0: s]
    new_slice, seam, min_cost = _carve(slice_img, slice_block)
    return new_slice, seam, min_cost


def carve_top(target_image, block_pixels, block_size, overlap_size, block_row, block_col):
    I, J = block_row, block_col
    img = target_image
    b, s = block_size, overlap_size
    pI, pJ = I * (b - s), J * (b - s)
    slice_img = img[pI: pI + s, pJ: pJ + b]
    slice_block = block_pixels[0: s, 0: b]

    slice_img = np.rot90(slice_img)
    slice_block = np.rot90(slice_block)
    new_slice, seam, min_cost = _carve(slice_img, slice_block)
    new_slice = np.rot90(new_slice, -1)
    return new_slice, seam, min_cost


def carve_seam(target_image, block, block_size, overlap_size, block_row, block_col):
    I, J = block_row, block_col
    b, s = block_size, overlap_size
    args = target_image, block.pixels, block_size, overlap_size, block_row, block_col

    # No left or top carving for the first block
    if I == J == 0:
        return block

    new_pixels = block.pixels.copy()
    tot_cost = 0
    # For blocks below the first block, top carving is always performed
    if I > 0:
        ov_top, seam_top, min_cost_top = carve_top(*args)
        new_pixels[:s, :b] = ov_top
        tot_cost += min_cost_top

    # For blocks to the right of the first block, left carving is always performed
    if J > 0:
        ov_left, seam_left, min_cost_left = carve_left(*args)
        new_pixels[:b, :s] = ov_left
        tot_cost += min_cost_left

    new_block = Block(new_pixels, tot_cost)
    return new_block

def _search(target_texture, patch, block_size, overlap_size, block_row, block_col):
    I, J = block_row, block_col
    b, s = block_size, overlap_size
    patch_height, patch_width = patch.shape[:2]

    best_block = Block([], np.inf)
    block_data = []
    for i in range(patch_height - block_size):
        for j in range(patch_width - block_size):
            block_pixels = patch[i: i + b, j: j + b, :].copy()
            ssd = compute_ssd(target_texture, block_pixels, block_size, overlap_size, I, J)
            block_data.append(BlockData(i, j, ssd))
            if ssd < best_block.ssd:
                best_block = Block(block_pixels, ssd)

    return best_block, block_data

def search(target_texture, patch, block_size, overlap_size, block_row, block_col, method, threshold):
    I, J = block_row, block_col
    b, s = block_size, overlap_size

    if I == J == 0:
        return Block(patch[:b, :b, :], 0)

    best_block, block_data = _search(target_texture, patch, b, s, I, J)
    if method == 'best':
        return best_block

    max_ssd = int((1. + threshold) * best_block.ssd)
    good_blocks = [b for b in block_data if b.ssd <= max_ssd]
    pick_i, pick_j, pick_ssd = random.choice(good_blocks)
    fuzzy_block_pixels = patch[pick_i: pick_i + b, pick_j: pick_j + b, :].copy()
    fuzzy_block = Block(fuzzy_block_pixels, pick_ssd)
    return fuzzy_block

def quilt(input_patch, block_size=54, output_texture_size_init=1000,
          method='best', carve=True, fuzzy_search_threshold=0.03):
    assert method in ['best', 'fuzzy'], \
        'Invalid method {}, must be one of ["best", "fuzzy"]'.format(method)

    _, _, num_channels = input_patch.shape
    block_size = b = 6 * (block_size // 6)
    overlap_size = s = block_size // 6
    num_blocks = 1 + np.ceil((output_texture_size_init - b) // (b - s))
    num_blocks = int(num_blocks)
    TSIZE = b + (num_blocks - 1) * (b - s)  # Computed output texture size

    tex_random = np.zeros((TSIZE, TSIZE, num_channels), dtype=np.int)
    tex_output = np.zeros((TSIZE, TSIZE, num_channels), dtype=np.int)

    # Form target image using random blocks
    for block_row in trange(num_blocks, ncols=50):
        pI = block_row * (b - s)
        for block_col in trange(num_blocks, leave=False, ncols=50, unit_scale=True):
            pJ = block_col * (b - s)

            # Synthesize next block of SSD image
            next_block = search(
                tex_output,
                input_patch,
                block_size,
                overlap_size,
                block_row,
                block_col,
                method='best',
                threshold=fuzzy_search_threshold
            )

            if carve:
                next_block = carve_seam(tex_output, next_block, b, s, block_row, block_col)

            tex_output[pI: pI + b, pJ: pJ + b, :] = next_block.pixels

    return tex_output


def main():

    root = Path('samples')
    for patch_path in root.glob('*'):
        t1 = time.time()
        patch = cv2.imread(patch_path.as_posix())
        init_block_size = 54
        block_size = b = 6 * (init_block_size // 6)
        overlap_size = s = block_size // 6
        init_target_size = 500
        num_blocks = 1 + np.ceil((init_target_size - b) // (b - s))
        num_blocks = int(num_blocks)
        target_size = b + (num_blocks - 1) * (b - s)
        print('patch: ', patch_path)
        print('target_size: ', target_size)
        print('block_size: ', block_size)
        print('overlap_size: ', overlap_size)
        print('num_blocks: ', num_blocks)

        tex_proc = quilt(
            patch, block_size, target_size, method='fuzzy',
            carve=True, fuzzy_search_threshold=0.3
        )

        output_root = Path('outputs')
        basename = patch_path.stem
        proc_output_pth = output_root / (basename + '_processed.jpg')
        cv2.imwrite(proc_output_pth.as_posix(), tex_proc)
        print('Conversion took {} seconds'.format(time.time() - t1))

if __name__ == '__main__':
    main()




