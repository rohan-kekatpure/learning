import numpy as np

um = 1e-6
nm = 1e-9
lambda0 = 1550 * nm
k0 = 2 * np.pi / lambda0
from IPython import embed

def dielectric_strong(core_thickness, eps_core, eps_cover, eps_substr
                      mode_index, mode_parity, max_tol, max_iter, nguess):
    h = core_thickness
    ef = eps_core
    ec = eps_cover
    es = eps_substr
    Kc = k0 * np.sqrt(ef - ec)
    Ks = k0 * np.sqrt(ef - es)
    M = mode_index

    tol = np.inf
    niter = 0
    maxtol = max_tol
    maxiter = max_iter
    p = 1.
    q = 1.

    nguess = 1.5
    neff = nguess
    k = k0 * np.emath.sqrt(ef - nguess * nguess)
    omega = 0.1
    while ((tol > maxtol) and (niter < maxiter)):
        # core loop
        u = k
        gc = np.emath.sqrt(Kc * Kc - k * k)
        gs = np.emath.sqrt(Ks * Ks - k * k)
        Gc = np.emath.sqrt(k * k + gc * gc * p * p)
        Gs = np.emath.sqrt(k * k + gs * gs * q * q)
        num = p * q * gc * gs - k * k + Gc * Gs
        denom = k * (p * gc + q * gs)
        v = (2 / h) * (M * np.pi + np.arctan(num / denom))    
        k = omega * u + (1 - omega) * v

        # Convergence
        nprev = neff
        neff = np.emath.sqrt(ef - k * k/(k0 * k0))
        tol = np.abs(nprev - neff)
        print(f'niter->{niter}, neff->{neff}, tol->{tol}')
        niter += 1
    
def MDM():
    h = 3000 * nm
    ef = 1.45 * 1.45
    ec = -143.497 - 9.517j
    es = -95.92 - 10.97j
    Kc = k0 * np.emath.sqrt(ef - ec)
    Ks = k0 * np.emath.sqrt(ef - es)
    p = ef / ec
    q = ef / es

    tol = np.inf
    niter = 0
    maxtol = 1e-16
    maxiter = 1200

    nguess = 1.0
    neff = nguess
    kappa = k0 * np.emath.sqrt(ef + nguess * nguess)
    while ((tol > maxtol) and (niter < maxiter)):        
        # core loop for kappa
        u = kappa
        alphac = np.emath.sqrt(Kc ** 2 + kappa ** 2)
        alphas = np.emath.sqrt(Ks ** 2 + kappa ** 2)
        S = 0.5 * (p * alphac + q * alphas)
        t1 = S / np.tanh(kappa * h)
        t2 = np.emath.sqrt(p * q * alphac * alphas)
        v = -t1 - np.emath.sqrt((t1 + t2) * (t1 - t2))        
        kappa = (u + v) / 2.0

        # convergence testing
        nprev = neff
        neff = np.emath.sqrt(ef + (kappa ** 2)/(k0 ** 2))
        tol = np.abs(nprev - neff)
        print(f'niter->{niter}, neff->{neff}, tol->{tol}')
        
        niter += 1    

if __name__ == '__main__':
    # dielectric_strong()
    # MDM()

