import numpy as np

from testing import timing

@timing
def func_np(x):
    x_mean = np.mean(x, axis=0) 
    x_std = np.sqrt(np.var(x, axis=0))
    vh = x_mean + 3 * x_std
    vl = x_mean - 3 * x_std
    
    x_filter = np.logical_and((vl[None, :] < x[0:15, :, :]), (x[0:15, :, :]< vh[None, :]))
    
    p_mean = np.mean(x[0:15, :, :] * x_filter, axis=0)
    return p_mean

@timing
def func_for(x):
    f = np.zeros(x[0].shape, dtype=float)
    for r in range(f.shape[0]):
        for c in range(f.shape[1]):
            m = np.mean(x[:, r, c])
            std = np.sqrt(np.var(x[:, r, c]))
            vh = m + 3 * std
            vl = m - 3 * std
            p_list = np.array([])
            for exp in range(15):
                if vl < x[exp, r, c] < vh:
                    p_list = np.append(p_list, x[exp, r, c])

            f[r, c] = np.mean(p_list)
    return f
    
if __name__ == '__main__':
    x = np.random.rand(20, 10000, 10000)
    p_np = func_np(x)
    p_for = func_for(x)
