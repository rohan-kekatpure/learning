import numpy as np
from functools import partial
import sys

sys.path.append('../build')
# Is the script is invoked from pytest
frompytest = 'pytest' in sys.modules 

import pytest
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
    if not frompytest:
        print(f'niter->{sol.niter}, neff->{sol.effectiveIndex}, tol->{sol.tol}', end=',')
        print(f'err -> {sol.effectiveIndex-neff}\n')
        if (len(sys.argv) > 1) and (sys.argv[1] in ('e', 'embed')):
            embed()
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
        MAXTOL, MAXITER, 3.4347458991523547
    )

# def test_dielectric_strong_TE1():
#     default(
#         1550 * NM, 3.5**2, 1.0, 1.45**2, 1000 * NM,
#         emm.Polarization.TE, emm.Parity.ODD,
#         emm.ModeType.DIELECTRIC_STRONG, 1, 1.5,
#         MAXTOL, MAXITER, 3.2327892969869200
#     )

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
        MAXTOL, MAXITER, 3.4165068626393458
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
        MAXTOL, MAXITER, 2.668932488161408
    )

def test_dielectric_strong_TM3():
    default(
        1550 * NM, 3.5**2, 1.0, 1.45**2, 1000 * NM,
        emm.Polarization.TM, emm.Parity.ODD,
        emm.ModeType.DIELECTRIC_STRONG, 2, 1.5,
        MAXTOL, MAXITER, 1.8652436341780112
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

def test_MDM_gap_plasmon_even():
    neff = 2.0171223996367655-0.023755375876767085j
    default(
        1550 * NM, 2.1025, -143.497 - 9.517j, -95.92 - 10.97j, 50 * NM,
        emm.Polarization.TM, emm.Parity.EVEN,
        emm.ModeType.MDM, 0, 1.0,
        MAXTOL, MAXITER, neff
    )

def test_MDM_3um_gap_plasmon_even():
    neff = 1.4679150331295268-0.0015140072312537019j
    default(
        1550 * NM, 2.1025, -143.497 - 9.517j, -95.92 - 10.97j, 3000 * NM,
        emm.Polarization.TM, emm.Parity.EVEN,
        emm.ModeType.MDM, 0, 1. - 1j,
        MAXTOL, MAXITER, neff
    )

def test_MDM_3um_gap_plasmon_odd():
    neff = 1.4550362750343577-0.0014400935244848836j
    default(
        1550 * NM, 2.1025, -143.497 - 9.517j, -95.92 - 10.97j, 3000 * NM,
        emm.Polarization.TM, emm.Parity.ODD,
        emm.ModeType.MDM, 0, 1.0 - 1j,
        MAXTOL, MAXITER, neff
    )

def test_MDM_300nm_TM1():
    # For this mode, M = 0. But it is still
    # called TM1 to be consistent with naming
    # in table 4 of the paper
    neff = 0.007407516660126918-1.981855964604849j    
    default(
        1550 * NM, 2.1025, -143.497 - 9.517j, -95.92 - 10.97j, 300 * NM,
        emm.Polarization.TM, emm.Parity.ODD,
        emm.ModeType.DIELECTRIC_STRONG, 0, 0 - 1j,
        MAXTOL, MAXITER, neff
    )

def test_MDM_300nm_TM2():
    # For this mode, M = 1. But it is still
    # called TM2 to be consistent with naming
    # in table 4 of the paper
    neff = 0.0019247843717472594 - 4.9010958288401785j
    default(
        1550 * NM, 2.1025, -143.497 - 9.517j, -95.92 - 10.97j, 300 * NM,
        emm.Polarization.TM, emm.Parity.EVEN,
        emm.ModeType.DIELECTRIC_STRONG, 1, 1.0,
        MAXTOL, 2000, neff
    )

def test_MDM_300nm_TM3():
    # For this mode, M = 1. But it is still
    # called TM3 to be consistent with naming
    # in table 4 of the paper
    neff = 0.00021421644551343586 + 7.5834875225319935j
    default(
        1550 * NM, 2.1025, -143.497 - 9.517j, -95.92 - 10.97j, 300 * NM,
        emm.Polarization.TM, emm.Parity.ODD,
        emm.ModeType.DIELECTRIC_STRONG, 1, 1.0,
        MAXTOL, 2000, neff
    )

def test_MDM_300nm_TM4():
    # For this mode, M = 2. But it is still
    # called TM4 to be consistent with naming
    # in table 4 of the paper
    neff = 0.005927495292030504 + 10.220103712927525j
    default(
        1550 * NM, 2.1025, -143.497 - 9.517j, -95.92 - 10.97j, 300 * NM,
        emm.Polarization.TM, emm.Parity.EVEN,
        emm.ModeType.DIELECTRIC_STRONG, 2, 1.0,
        MAXTOL, 2000, neff
    )

def test_MDM_300nm_TM5():
    # For this mode, M = 2. But it is still
    # called TM5 to be consistent with naming
    # in table 4 of the paper
    neff = 0.01577537648440215 + 12.831497704034192j
    default(
        1550 * NM, 2.1025, -143.497 - 9.517j, -95.92 - 10.97j, 300 * NM,
        emm.Polarization.TM, emm.Parity.ODD,
        emm.ModeType.DIELECTRIC_STRONG, 2, 1.0,
        MAXTOL, 2000, neff
    )

if __name__ == '__main__':
    # test_dielectric_strong_TE0()
    # test_dielectric_strong_TE1()
    # test_dielectric_strong_TE2()
    # test_dielectric_strong_TE3()
    # test_dielectric_strong_TM0()
    # test_dielectric_strong_TM1()
    # test_dielectric_strong_TM2()
    # test_dielectric_strong_TM3()
    # test_dielectric_weak_TE0()
    # test_dielectric_weak_TM0()
    # test_MDM_gap_plasmon_even()
    # test_MDM_gap_plasmon_even_3um()
    # test_MDM_gap_plasmon_odd_3um()    
    test_MDM_3um_gap_TM1()
