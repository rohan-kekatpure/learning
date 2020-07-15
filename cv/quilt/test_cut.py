import numpy as np
import matplotlib.pyplot as pl

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
    seam = np.zeros((b,), dtype=np.int)
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

def main():
    shape = r, c = (60, 10)
    dark = np.full(shape, 64, dtype=np.int)
    light = np.full(shape, 192, dtype=np.int)

    # Create blocks
    block1 = np.zeros((r, c, 3), dtype=np.int)
    block2 = np.zeros((r, c, 3), dtype=np.int)
    block1[:, :, 0] = dark
    block1[:, :, 1] = dark
    block1[:, :, 2] = dark
    block2[:, :, 0] = light
    block2[:, :, 1] = light
    block2[:, :, 2] = light

    # Create seam
    idx = np.arange(0, r).reshape(-1, 1)
    cols = np.full((r, 1), fill_value=c//2)
    seam = np.column_stack((idx, cols))
    random_walk = np.random.randint(-1, 2, size=(r, 1)).cumsum()
    seam[:, 1] += random_walk
    seam[:, 1] = seam[:, 1].clip(0, 9)

    # Make vales at the seam equal in both blocks
    block2[seam[:, 0], seam[:, 1], :] = 128

    new_slice, new_seam, cost = carve(block1, block2)

    fig, ax = pl.subplots(1, 3)
    ax[0].imshow(block1, cmap='gray')
    ax[1].imshow(block2, cmap='gray')
    ax[2].imshow(new_slice, cmap='gray')
    pl.show(block=True)
    from IPython import embed; embed(); exit(0)


if __name__ == '__main__':
    main()
