import numpy as np

um = 1e-6
nm = 1e-9
lambda0 = 1550 * nm
k0 = 2 * np.pi / lambda0
from IPython import embed

def dielectric_strong(core_thickness, eps_core, eps_cover, eps_substr,
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

def DMD():
    h = 100 * nm
    ef = -143.497 - 9.517j
    es = 1.45 ** 2
    ec = 1.45 ** 2
    Qc = k0 * np.emath.sqrt(ec - ef)
    Qs = k0 * np.emath.sqrt(es - ef)
    p = ef / ec
    q = ef / es

    tol = np.inf
    niter = 0
    maxtol = 1e-16
    maxiter = 1200

    nguess = 1.46 - 0.0007j
    neff = nguess
    kappa = k0 * np.emath.sqrt(ef + nguess * nguess)
    A, B = k0, 0

    while ((tol > maxtol) and (niter < maxiter)):        
        # core loop for kappa
        u = kappa
        t1 = kappa / np.tanh(kappa * h)
        t2 = kappa / np.sinh(kappa * h)

        a = -t1 - np.sqrt(B ** 2 + t2 ** 2)
        b = np.emath.sqrt(a ** 2 + kappa ** 2 + 2 * a * t1)
        v = np.emath.sqrt((a + b) ** 2 / (p ** 2) + Qc ** 2)
        kappa = 0.5 * (u + v)

        xi_c = np.emath.sqrt(kappa ** 2 - Qc ** 2)
        xi_s = np.emath.sqrt(kappa ** 2 - Qs ** 2)
        A = (p * xi_c + q * xi_s) / 2.0 
        B = (p * xi_c - q * xi_s) / 2.0        

        # convergence testing
        nprev = neff
        neff = np.emath.sqrt(ef + (kappa ** 2)/(k0 ** 2))
        tol = np.abs(nprev - neff)
        print(f'niter->{niter}, neff->{neff}, tol->{tol}')
        
        niter += 1    

def DMD_symmetric():
    h = 100 * nm
    ef = -143.49 - 9.517j
    ec = 1.45 ** 2
    Qc = k0 * np.emath.sqrt(ec - ef)
    p = ef / ec

    tol = np.inf
    niter = 0
    maxtol = 1e-16
    maxiter = 1200

    nguess = 1.0 - 0.1j
    neff = nguess
    kappa = k0 * np.emath.sqrt(ef + nguess * nguess)
    mode = 'ODD'

    while ((tol > maxtol) and (niter < maxiter)):        
        # core loop for kappa
        u = kappa
        if mode == 'EVEN':
            t1 = np.tanh(kappa * h / 2.) / p
        else:
            t1 = 1.0 / (p * np.tanh(kappa * h / 2.))

        v = Qc / np.emath.sqrt(1.0 - t1 ** 2)
        kappa = 0.5 * (u + v)

        # convergence testing
        nprev = neff
        neff = np.emath.sqrt(ef + (kappa ** 2)/(k0 ** 2))
        tol = np.abs(nprev - neff)
        print(f'niter->{niter}, neff->{neff}, tol->{tol}')
        
        niter += 1

def DMD2():
    h = 100 * nm
    ef = -143.497 - 9.517j
    ec = 1.45 ** 2
    es = 1.45 ** 2
    tol = np.inf
    niter = 0
    maxtol = 1e-16
    maxiter = 1000

    Kc = k0 * np.emath.sqrt(ef - ec)
    Ks = k0 * np.emath.sqrt(ef - es)
    p = ef / ec
    q = ef / es

    nguess = 1.
    neff = nguess
    kappa = k0 * np.emath.sqrt(ef + nguess * nguess)
    while ((tol > maxtol) and (niter < maxiter)):        
        # core loop for kappa
        u = kappa 
        x = p * np.emath.sqrt(Kc * Kc + kappa * kappa)
        y = q * np.emath.sqrt(Ks * Ks + kappa * kappa)
        t = (x + y) / (kappa * kappa + x * y)
        v = (1 / h) * np.arctanh(t)
        kappa = 0.5 * (u + v)

        # convergence testing
        nprev = neff
        neff = np.emath.sqrt(ef + (kappa / k0) ** 2)
        tol = np.abs(nprev - neff)
        print(f'niter->{niter}, neff->{neff}, tol->{tol}')
        
        niter += 1    


if __name__ == '__main__':
    # dielectric_strong()
    # MDM()
    # DMD()
    # DMD_symmetric()
    DMD2()

