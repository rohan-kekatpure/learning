'''
Python implementations of the algorithms in the paper
to check for errors and improvements. This file is not 
a part of the production release.
'''
import numpy as np

um = 1e-6
nm = 1e-9
eps_vac = 1.00 ** 2
eps_Au = -95.92 - 10.97j
eps_Ag = -143.497 - 9.517j
eps_SiO2 = 1.45 ** 2
eps_Si = 3.5 ** 2
eps_GaAs = 3.3 ** 2
eps_AlGaAs = 3.256 ** 2
lambda0 = 1550 * nm
EVEN = 1
ODD = -1
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

def dielectric_strong2(core_thickness, eps_core, eps_cover, eps_substr,
                      pol, mode_index, max_tol, max_iter, nguess):
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

    if pol == 'TM':
        p = ef / ec
        q = ef / es
    elif pol == 'TE':
        p = q = 1.
    else:
        raise ValueError('invalid polarization')

    neff = nguess
    k = k0 * np.emath.sqrt(ef - nguess * nguess)    
    while ((tol > maxtol) and (niter < maxiter)):
        # core loop
        u = k
        gc = np.emath.sqrt(Kc * Kc - k * k)
        gs = np.emath.sqrt(Ks * Ks - k * k)
        mu = 1j * k
        num = (mu - p * gc) * (mu - q * gs) 
        denom = (mu + p * gc) * (mu + q * gs) 
        Z = num / denom
        r = np.abs(Z)
        theta = np.angle(Z)
        v = (1 / h) * (M * np.pi + (1/2.) * theta + (1/2.j) * np.log(r))    
        k = 0.5 * (u + v)

        # Convergence
        nprev = neff
        neff = np.emath.sqrt(ef - k * k/(k0 * k0))
        tol = np.abs(nprev - neff)
        print(f'niter->{niter}, neff->{neff}, tol->{tol}')
        niter += 1

def dweak1(core_thickness, eps_core, eps_cover, eps_substr,
           pol, max_tol, max_iter, nguess):
    h = core_thickness
    ef = eps_core
    ec = eps_cover
    es = eps_substr
    Kc = k0 * np.sqrt(ef - ec)
    Ks = k0 * np.sqrt(ef - es)

    tol = np.inf
    niter = 0
    maxtol = max_tol
    maxiter = max_iter

    if pol == 'TM':
        p = ef / ec
        q = ef / es
    elif pol == 'TE':
        p = q = 1.
    else:
        raise ValueError('invalid polarization')

    neff = nguess
    k = k0 * np.emath.sqrt(ef - nguess * nguess)    
    while ((tol > maxtol) and (niter < maxiter)):
        # core loop
        u = k
        gc = np.emath.sqrt(Kc * Kc - k * k)
        gs = np.emath.sqrt(Ks * Ks - k * k)        
        v = (k * k - p * q * gc * gs) * np.tan(k * h) / (p * gc + q * gs)
        k = 0.5 * (u + v)

        # Convergence
        nprev = neff
        neff = np.emath.sqrt(ef - k * k/(k0 * k0))
        tol = np.abs(nprev - neff)
        print(f'niter->{niter}, neff->{neff}, tol->{tol}')
        niter += 1    


def dweak3(core_thickness, eps_core, eps_cover, eps_substr,
           pol, max_tol, max_iter, nguess):
    h = core_thickness
    ef = eps_core
    ec = eps_cover
    es = eps_substr
    Kc = k0 * np.sqrt(ef - ec)
    Ks = k0 * np.sqrt(ef - es)

    tol = np.inf
    niter = 0
    maxtol = max_tol
    maxiter = max_iter

    if pol == 'TM':
        p = ef / ec
        q = ef / es
    elif pol == 'TE':
        p = q = 1.
    else:
        raise ValueError('invalid polarization')

    neff = nguess
    k = k0 * np.emath.sqrt(ef - nguess * nguess)    
    while ((tol > maxtol) and (niter < maxiter)):
        # core loop
        u = k
        gc = np.emath.sqrt(Kc * Kc - k * k)
        gs = np.emath.sqrt(Ks * Ks - k * k)        
        Nr = (k * k - p * q * gc * gs)
        Dr = k * (p * gc + q * gs)
        v = (1./h) * (np.pi / 2. - np.arctan(Nr / Dr) - 5 * np.pi)
        k = 0.5 * (u + v)

        # Convergence
        nprev = neff
        neff = np.emath.sqrt(ef - k * k/(k0 * k0))
        tol = np.abs(nprev - neff)
        print(f'niter->{niter}, neff->{neff}, tol->{tol}')
        niter += 1

def dweak4(core_thickness, eps_core, eps_cover, eps_substr,
           pol, max_tol, max_iter, nguess):
    h = core_thickness
    ef = eps_core
    ec = eps_cover
    es = eps_substr

    # ensure es > ec
    if (ec > es):
        ec, es = es, ec
    
    Kc = k0 * np.sqrt(ef - ec)
    Ks = k0 * np.sqrt(ef - es)

    tol = np.inf
    niter = 0
    maxtol = max_tol
    maxiter = max_iter

    if pol == 'TM':
        p = ef / ec
        q = ef / es
    elif pol == 'TE':
        p = q = 1.
    else:
        raise ValueError('invalid polarization')

    neff = nguess
    k = k0 * np.emath.sqrt(ef - nguess * nguess)    

    while ((tol > maxtol) and (niter < maxiter)):
        # core loop
        u = k
        gc = np.emath.sqrt(Kc * Kc - k * k)        
        gs = np.emath.sqrt(Ks * Ks - k * k)        
        theta = np.arctan(p * gc / k)
        v = Ks /np.sqrt(1. + (np.tan(k * h - theta) / q)**2)
        k = 0.5 * (u + v)

        # Convergence
        nprev = neff
        neff = np.emath.sqrt(ef - k * k/(k0 * k0))
        tol = np.abs(nprev - neff)
        print(f'niter->{niter}, neff->{neff}, tol->{tol}')
        niter += 1

def MDM(core_thickness, eps_core, eps_cover, eps_substr,
        parity, nguess, max_tol, max_iter):
    h = core_thickness
    ef = eps_core
    ec = eps_cover
    es = eps_substr

    Kc = k0 * np.emath.sqrt(ef - ec)
    Ks = k0 * np.emath.sqrt(ef - es)
    p = ef / ec
    q = ef / es

    tol = np.inf
    niter = 0
    neff = nguess
    kappa = k0 * np.emath.sqrt(ef + nguess * nguess)
    while ((tol > max_tol) and (niter < max_iter)):        
        # core loop for kappa
        u = kappa
        alphac = np.emath.sqrt(Kc ** 2 + kappa ** 2)
        alphas = np.emath.sqrt(Ks ** 2 + kappa ** 2)
        S = 0.5 * (p * alphac + q * alphas)
        t1 = S / np.tanh(kappa * h)
        t2 = np.emath.sqrt(p * q * alphac * alphas)
        v = -t1 + np.emath.sqrt((t1 + t2) * (t1 - t2))        
        kappa = (u + v) / 2.0

        # convergence testing
        nprev = neff
        neff = np.emath.sqrt(ef + (kappa ** 2)/(k0 ** 2))
        tol = np.abs(nprev - neff)
        print(f'niter->{niter}, neff->{neff}, tol->{tol}')
        
        niter += 1    

def DMD1(core_thickness, eps_core, eps_cover, eps_substr, parity, max_tol, max_iter):
    h = core_thickness 
    ef = eps_core
    es = eps_substr
    ec = eps_cover
    Qc = k0 * np.emath.sqrt(ec - ef)
    Qs = k0 * np.emath.sqrt(es - ef)
    p = ef / ec
    q = ef / es

    tol = np.inf
    nguess = 1.0 + 0.0001j
    niter = 0
    neff = nguess
    kappa = k0 * np.emath.sqrt(ef + nguess * nguess)
    A, B = k0, 0

    while ((tol > max_tol) and (niter < max_iter)):        
        # core loop for kappa
        u = kappa
        t1 = kappa / np.tanh(kappa * h)
        t2 = kappa / np.sinh(kappa * h)

        a = -t1 + parity * np.sqrt(B ** 2 + t2 ** 2)
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

def DMD2(core_thickness, eps_core, eps_cover, eps_substr, max_tol, max_iter):
    h = core_thickness
    ef = eps_core
    es = eps_substr
    ec = eps_cover
    Kc = k0 * np.emath.sqrt(ef - ec)
    Ks = k0 * np.emath.sqrt(ef - es)
    p = ef / ec
    q = ef / es

    tol = np.inf
    niter = 0
    maxtol = 1e-16
    maxiter = 1200

    nguess = 1.4
    neff = nguess
    kappa = k0 * np.emath.sqrt(ef + nguess * nguess)

    while ((tol > maxtol) and (niter < maxiter)):        
        # core loop for kappa
        u = kappa
        alphac = np.emath.sqrt(Kc * Kc + kappa * kappa)
        alphas = np.emath.sqrt(Ks * Ks + kappa * kappa)
        theta = np.arctanh(-p * alphac / kappa)
        v = Ks / np.emath.sqrt((np.tanh(kappa * h - theta) / q)**2 - 1)
        kappa = 0.5 * (u + v)

        # convergence testing
        nprev = neff
        neff = np.emath.sqrt(ef + (kappa ** 2)/(k0 ** 2))
        tol = np.abs(nprev - neff)
        print(f'niter->{niter}, neff->{neff}, tol->{tol}')
        
        niter += 1       

def MDMsym(core_thickness, eps_core, eps_clad, 
           parity, nguess, max_tol, max_iter):
    h = core_thickness
    ef = eps_core
    ec = eps_clad
    
    Kc = k0 * np.emath.sqrt(ef - ec)
    p = ef / ec
    
    tol = np.inf
    niter = 0
    neff = nguess
    kappa = k0 * np.emath.sqrt(nguess * nguess - ef)
    while ((tol > max_tol) and (niter < max_iter)):        
        # core loop for kappa
        u = kappa
        pk = p * np.sqrt(Kc ** 2 + kappa ** 2)
        t = np.tanh(kappa * h / 2.)
        if parity == EVEN:
            v = -pk * t
        elif parity == ODD:
            v = -pk / t
        else:
            raise ValueError('invalid parity')

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
    # DMD1(50e-9, -143.497 - 9.517j, 1.0, 1.45**2, 1, 1e-16, 1000)
    # DMD_symmetric()

    # dielectric_strong2(1000e-9, 3.5**2, 1.0, 1.45**2,
    #                   'TM', 4, 1e-16, 1000, 1.45)
    
    # dweak4(1e-6, 3.5**2, 1.0, 1.45**2,
    #       'TE', 1e-16, 1000, 1.45)

    # DMD2(50e-9, -143.497 - 9.517j, 1.0, 1.45**2, 1e-16, 1000)

    # DMD2(100e-9, -143.497 - 9.517j, 1.45**2, 1.45**2, 1e-16, 1000)

    MDM(50e-9, eps_SiO2, eps_Ag, eps_Ag, EVEN, 2.0, 1e-16, 100)
    MDMsym(50e-9, eps_SiO2, eps_Ag, EVEN, 2.0, 1e-16, 100)
    

