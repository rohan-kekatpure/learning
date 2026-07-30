import numpy as np

um = 1e-6
nm = 1e-9
lambda0 = 1550 * nm
k0 = 2 * np.pi / lambda0

def dielectric_strong():
    h = 1000 * nm
    ef = 3.5 * 3.5
    ec = 1.0
    es = 1.45 * 1.45
    Kc = k0 * np.sqrt(ef - ec)
    Ks = k0 * np.sqrt(ef - es)
    M = 0

    tol = np.inf
    niter = 0
    maxtol = 1e-16
    maxiter = 100
    p = 1.
    q = 1.

    nguess = 1.5
    neff = nguess
    k = k0 * np.emath.sqrt(ef - nguess * nguess)
    while ((tol > maxtol) and (niter < maxiter)):
        nprev = neff
        gc = np.emath.sqrt(Kc * Kc - k * k)
        gs = np.emath.sqrt(Ks * Ks - k * k)
        Gc = np.emath.sqrt(k * k + gc * gc * p * p)
        Gs = np.emath.sqrt(k * k + gs * gs * q * q)
        num = p * q * gc * gs - k * k + Gc * Gs
        denom = k * (p * gc + q * gs)
        k = (2 / h) * (M * np.pi + np.arctan(num / denom))    
        neff = np.emath.sqrt(ef - k * k/(k0 * k0))
        tol = np.abs(nprev - neff)
        print(f'niter->{niter}, neff->{neff}, tol->{tol}')
        niter += 1

def MDM():
    h = 50 * nm
    ef = 1.45 * 1.45
    ec = -143.49 - 9.52j
    es = -95.92 - 10.97j
    Kc = k0 * np.sqrt(ef - ec)
    Ks = k0 * np.sqrt(ef - es)
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
        alphac = np.emath.sqrt(Kc ** 2 + kappa ** 2)
        alphas = np.emath.sqrt(Ks ** 2 + kappa ** 2)
        S = (p * alphac + q * alphas) / 2.0
        t1 = S / np.tanh(kappa * h)
        t2 = t1 * t1 - p * q * alphac * alphas
        kappa = -t1 + np.sqrt(t2) 

        # convergence testing
        nprev = neff
        neff = np.emath.sqrt(ef + (kappa ** 2)/(k0 ** 2))
        tol = np.abs(nprev - neff)
        print(f'niter->{niter}, neff->{neff}, tol->{tol}')
        niter += 1    

if __name__ == '__main__':
    MDM()

