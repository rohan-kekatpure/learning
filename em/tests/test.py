
import numpy as np
from functools import partial
import sys; sys.path.append('../build')

from pathlib import Path
from IPython import embed

import emm

NM = 1e-9
MAXTOL = 1e-16
MAXITER = 1000

approx_equal = partial(np.isclose, rtol=0, atol=MAXTOL)

def default(
    lambda0 :float,
    ecore: complex,
    ecover: complex,
    esub: complex,
    hcore: float,
    polarization: emm.Polarization,
    mode_parity: emm.Parity, 
    mode_type: emm.ModeType,    
    mode_index: int, 
    nguess: float,
    max_tol: float,
    max_iter: int,
    neff: complex
):
    waveguide = emm.Waveguide(hcore, ecore, ecover, esub)
    
    modeopts = emm.ModeOptions(
        lambda0, 
        polarization, 
        mode_parity,
        mode_type, 
        mode_index, 
        nguess
    )

    solveropts = emm.SolverOptions(max_tol, max_iter)
    solver = emm.Solver(waveguide, solveropts, modeopts)
    sol = solver.solve()

    assert sol.converged
    assert not sol.max_iter_reached
    assert sol.tol <= solveropts.max_tol
    assert sol.niter <= solveropts.max_iter
    assert approx_equal(sol.effectiveIndex, neff)

def test_dielectric_strong_TE0():
    default(
        1550 * NM, 3.5**2, 1.0, 1.45**2, 1000 * NM,
        emm.Polarization.TE, emm.Parity.EVEN,
        emm.ModeType.DIELECTRIC_STRONG, 0, 1.5,
        MAXTOL, MAXITER, 3.4347458991523551
    )

def test_dielectric_strong_TE1():
    default(
        1550 * NM, 3.5**2, 1.0, 1.45**2, 1000 * NM,
        emm.Polarization.TE, emm.Parity.ODD,
        emm.ModeType.DIELECTRIC_STRONG, 1, 1.5,
        MAXTOL, MAXITER, 3.2327892969869200
    )

def test_dielectric_strong_TE2():
    default(
        1550 * NM, 3.5**2, 1.0, 1.45**2, 1000 * NM,
        emm.Polarization.TE, emm.Parity.EVEN,
        emm.ModeType.DIELECTRIC_STRONG, 1, 1.5,
        MAXTOL, MAXITER, 2.872310278807718 
    )

def test_dielectric_strong_TE3():
    default(
        1550 * NM, 3.5**2, 1.0, 1.45**2, 1000 * NM,
        emm.Polarization.TE, emm.Parity.ODD,
        emm.ModeType.DIELECTRIC_STRONG, 2, 1.5,
        MAXTOL, MAXITER, 2.3020246174805488
    )

def test_dielectric_strong_TM0():
    default(
        1550 * NM, 3.5**2, 1.0, 1.45**2, 1000 * NM,
        emm.Polarization.TM, emm.Parity.EVEN,
        emm.ModeType.DIELECTRIC_STRONG, 0, 1.5,
        MAXTOL, MAXITER, 3.4165068626393461
    )

def test_dielectric_strong_TM1():
    default(
        1550 * NM, 3.5**2, 1.0, 1.45**2, 1000 * NM,
        emm.Polarization.TM, emm.Parity.ODD,
        emm.ModeType.DIELECTRIC_STRONG, 1, 1.5,
        MAXTOL, MAXITER, 3.1541909024008027
    )

def test_dielectric_strong_TM2():
    default(
        1550 * NM, 3.5**2, 1.0, 1.45**2, 1000 * NM,
        emm.Polarization.TM, emm.Parity.EVEN,
        emm.ModeType.DIELECTRIC_STRONG, 1, 1.5,
        MAXTOL, MAXITER, 2.6689324881614085
    )

def test_dielectric_strong_TM3():
    default(
        1550 * NM, 3.5**2, 1.0, 1.45**2, 1000 * NM,
        emm.Polarization.TM, emm.Parity.ODD,
        emm.ModeType.DIELECTRIC_STRONG, 2, 1.5,
        MAXTOL, MAXITER, 1.8652436341780116
    )

def test_dielectric_weak_TE0():
    default(
        1550 * NM, 3.3**2, 1.0, 3.256**2, 1000 * NM,
        emm.Polarization.TE, emm.Parity.EVEN,
        emm.ModeType.DIELECTRIC_WEAK, 0, 1.0,
        MAXTOL, MAXITER, 3.2659964664547623
    )

def test_dielectric_weak_TM0():
    default(
        1550 * NM, 3.3**2, 1.0, 3.256**2, 1000 * NM,
        emm.Polarization.TM, emm.Parity.EVEN,
        emm.ModeType.DIELECTRIC_WEAK, 0, 1.0,
        MAXTOL, MAXITER, 3.26338400537407312
    )