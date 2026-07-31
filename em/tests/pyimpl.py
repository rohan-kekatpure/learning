import numpy as np

um = 1e-6
nm = 1e-9
lambda0 = 1550 * nm
k0 = 2 * np.pi / lambda0
from IPython import embed

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

    nguess = 2 - 1j
    neff = nguess
    kappa = k0 * np.emath.sqrt(ef + nguess * nguess)
    while ((tol > maxtol) and (niter < maxiter)):        
        # core loop for kappa
        kprev = kappa
        alphac = np.emath.sqrt(Kc ** 2 + kappa ** 2)
        alphas = np.emath.sqrt(Ks ** 2 + kappa ** 2)
        S = 0.5 * (p * alphac + q * alphas)
        t1 = S / np.tanh(kappa * h)
        t2 = np.emath.sqrt(p * q * alphac * alphas)
        v = -t1 + np.emath.sqrt((t1 + t2) * (t1 - t2))        
        kappa = (kprev + v)/2.0

        # convergence testing
        nprev = neff
        neff = np.emath.sqrt(ef + (kappa ** 2)/(k0 ** 2))
        tol = np.abs(nprev - neff)
        print(f'kr->{kappa.real:.16f}, ki->{kappa.imag:.16f}')                
        print(f'acr->{alphac.real:.16f}, aci->{alphac.imag:.16f}')        
        print(f'asr->{alphas.real:.16f}, asi->{alphas.imag:.16f}')        
        print(f'niter->{niter}, neff->{neff}, tol->{tol}\n')
        
        niter += 1    

if __name__ == '__main__':
    MDM()

