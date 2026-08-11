import numpy as np
from functools import partial
import sys

sys.path.append('../build')
# Is the script is invoked from pytest
frompytest = 'pytest' in sys.modules 

from typing import Callable
import pytest
from pathlib import Path
from IPython import embed

import emm

NM = 1e-9
MAXTOL = 1e-16
MAXITER = 1000
eps_vac = 1.00 ** 2
eps_Au = -95.92 - 10.97j
eps_Ag = -143.497 - 9.517j
eps_SiO2 = 1.45 ** 2
eps_Si = 3.5 ** 2
eps_GaAs = 3.3 ** 2
eps_AlGaAs = 3.256 ** 2
approx_equal = partial(np.isclose, rtol=0, atol=MAXTOL)

def default(
    *, 
    solver: Callable = None, 
    neff_true: complex = None, 
    **kwargs
) -> None:
    sol = solver(**kwargs)
    if not frompytest:
        print(f'solver->{solver.__name__}', end=',')
        print(f'niter->{sol.niter}, neff->{sol.effective_index}, tol->{sol.tol}', end=',')
        print(f'err -> {sol.effective_index - neff_true}', end=',')
        if (len(sys.argv) > 1) and (sys.argv[1] in ('e', 'embed')):
            embed()
    try:
        assert sol.converged
        assert not sol.max_iter_reached
        assert sol.tol <= kwargs['max_tol']
        assert sol.niter <= kwargs['max_iter']
        assert approx_equal(sol.effective_index, neff_true)
        print('result->ok')
    except AssertionError as e:
        print('result->exception')

def test_dielectric_strong_TE0():
    default(
        solver=emm.slab.solve_d_strong, neff_true=3.4347458991523547,
        lambda0=1550*NM, h=1000*NM, eps_core=eps_Si, eps_cover=eps_vac, eps_substr=eps_SiO2,
        pol=emm.slab.Polarization.TE, mode_index=0, parity=emm.slab.Parity.EVEN,
        neff_guess=1.0, max_tol=1e-16, max_iter=100
    )

def test_dielectric_strong_TE1():
    default(
        solver=emm.slab.solve_d_strong, neff_true=3.2327892969869200,
        lambda0=1550*NM, h=1000*NM, eps_core=eps_Si, eps_cover=eps_vac, eps_substr=eps_SiO2,
        pol=emm.slab.Polarization.TE, mode_index=1, parity=emm.slab.Parity.ODD,
        neff_guess=1.0, max_tol=1e-16, max_iter=100
    )

def test_dielectric_strong_TE2():
    default(
        solver=emm.slab.solve_d_strong, neff_true=2.872310278807718,
        lambda0=1550*NM, h=1000*NM, eps_core=eps_Si, eps_cover=eps_vac, eps_substr=eps_SiO2,
        pol=emm.slab.Polarization.TE, mode_index=1, parity=emm.slab.Parity.EVEN,
        neff_guess=1.0, max_tol=1e-16, max_iter=100
    )


def test_dielectric_strong_TE3():
    default(
        solver=emm.slab.solve_d_strong, neff_true=2.3020246174805488,
        lambda0=1550*NM, h=1000*NM, eps_core=eps_Si, eps_cover=eps_vac, eps_substr=eps_SiO2,
        pol=emm.slab.Polarization.TE, mode_index=2, parity=emm.slab.Parity.ODD,
        neff_guess=1.0, max_tol=1e-16, max_iter=100
    )


def test_dielectric_strong_TM0():
    default(
        solver=emm.slab.solve_d_strong, neff_true=3.4165068626393458,
        lambda0=1550*NM, h=1000*NM, eps_core=eps_Si, eps_cover=eps_vac, eps_substr=eps_SiO2,
        pol=emm.slab.Polarization.TM, mode_index=0, parity=emm.slab.Parity.EVEN,
        neff_guess=1.0, max_tol=1e-16, max_iter=100
    )

def test_dielectric_strong_TM1():
    default(
        solver=emm.slab.solve_d_strong, neff_true=3.1541909024008027,
        lambda0=1550*NM, h=1000*NM, eps_core=eps_Si, eps_cover=eps_vac, eps_substr=eps_SiO2,
        pol=emm.slab.Polarization.TM, mode_index=1, parity=emm.slab.Parity.ODD,
        neff_guess=1.0, max_tol=1e-16, max_iter=100
    )

def test_dielectric_strong_TM2():
    default(
        solver=emm.slab.solve_d_strong, neff_true=2.668932488161408,
        lambda0=1550*NM, h=1000*NM, eps_core=eps_Si, eps_cover=eps_vac, eps_substr=eps_SiO2,
        pol=emm.slab.Polarization.TM, mode_index=1, parity=emm.slab.Parity.EVEN,
        neff_guess=1.0, max_tol=1e-16, max_iter=100
    )

def test_dielectric_strong_TM3():
    default(
        solver=emm.slab.solve_d_strong, neff_true=1.8652436341780112,
        lambda0=1550*NM, h=1000*NM, eps_core=eps_Si, eps_cover=eps_vac, eps_substr=eps_SiO2,
        pol=emm.slab.Polarization.TM, mode_index=2, parity=emm.slab.Parity.ODD,
        neff_guess=1.0, max_tol=1e-16, max_iter=100
    )

def test_dielectric_weak_TE0():
    default(
        solver=emm.slab.solve_d_weak, neff_true=3.2659964664547623,
        lambda0=1550*NM, h=1000*NM, eps_core=eps_GaAs, eps_cover=eps_vac, eps_substr=eps_AlGaAs,
        pol=emm.slab.Polarization.TE, parity=emm.slab.Parity.EVEN,
        neff_guess=1.0, max_tol=1e-16, max_iter=100
    )

def test_dielectric_weak_TM0():
    default(
        solver=emm.slab.solve_d_weak, neff_true=3.26338400537407312,
        lambda0=1550*NM, h=1000*NM, eps_core=eps_GaAs, eps_cover=eps_vac, eps_substr=eps_AlGaAs,
        pol=emm.slab.Polarization.TM, parity=emm.slab.Parity.EVEN,
        neff_guess=1.0, max_tol=1e-16, max_iter=100
    )
    
def test_MDM_gap_plasmon_even():
    default(
        solver=emm.slab.solve_mdm, 
        neff_true=2.0171223996367655-0.023755375876767085j,
        lambda0=1550*NM, h=50*NM, eps_core=eps_SiO2,
        eps_cover=eps_Ag, eps_substr=eps_Au,
        parity=emm.slab.Parity.EVEN, neff_guess=1.0, 
        max_tol=1e-16, max_iter=100
    )

def test_MDM_3um_gap_plasmon_even():
    default(
        solver=emm.slab.solve_mdm, 
        neff_true=1.4679150331295268-0.0015140072312537019j,
        lambda0=1550*NM, h=3000*NM, eps_core=eps_SiO2,
        eps_cover=eps_Ag, eps_substr=eps_Au,
        parity=emm.slab.Parity.EVEN, neff_guess=1.0, 
        max_tol=1e-16, max_iter=100
    )

def test_MDM_3um_gap_plasmon_odd():
    # TODO: This seems slightly more sensitive to initial guess than
    # other mode types.
    default(
        solver=emm.slab.solve_mdm, 
        neff_true=1.4550362750343577-0.0014400935244848836j,
        lambda0=1550*NM, h=3000*NM, eps_core=eps_SiO2,
        eps_cover=eps_Ag, eps_substr=eps_Au,
        parity=emm.slab.Parity.ODD, neff_guess=1.45 - 1j, 
        max_tol=1e-16, max_iter=1000
    )

def test_MDM_300nm_TM1():
    # For this mode, M = 0. But it is still
    # called TM1 to be consistent with naming
    # in table 4 of the paper
    default(
        solver=emm.slab.solve_d_strong, 
        neff_true=0.007407516660126918-1.981855964604849j,
        lambda0=1550*NM, h=300*NM, eps_core=eps_SiO2, eps_cover=eps_Ag, 
        eps_substr=eps_Au, pol=emm.slab.Polarization.TM, mode_index=0, 
        parity=emm.slab.Parity.ODD, neff_guess=1.0, max_tol=1e-16, max_iter=100
    )

def test_MDM_300nm_TM2():
    # For this mode, M = 1. But it is still
    # called TM2 to be consistent with naming
    # in table 4 of the paper
    default(
        solver=emm.slab.solve_d_strong, 
        neff_true=0.0019247843717472594 - 4.9010958288401785j,
        lambda0=1550*NM, h=300*NM, eps_core=eps_SiO2, eps_cover=eps_Ag, 
        eps_substr=eps_Au, pol=emm.slab.Polarization.TM, mode_index=1, 
        parity=emm.slab.Parity.EVEN, neff_guess=1.0, max_tol=1e-16, max_iter=100
    )

def test_MDM_300nm_TM3():
    # For this mode, M = 1. But it is still
    # called TM3 to be consistent with naming
    # in table 4 of the paper
    default(
        solver=emm.slab.solve_d_strong, 
        neff_true=0.00021421644551343586 + 7.5834875225319935j,
        lambda0=1550*NM, h=300*NM, eps_core=eps_SiO2, eps_cover=eps_Ag, 
        eps_substr=eps_Au, pol=emm.slab.Polarization.TM, mode_index=1, 
        parity=emm.slab.Parity.ODD, neff_guess=1.0, max_tol=1e-16, max_iter=100
    )

def test_MDM_300nm_TM4():
    # For this mode, M = 2. But it is still
    # called TM4 to be consistent with naming
    # in table 4 of the paper
    default(
        solver=emm.slab.solve_d_strong, 
        neff_true=0.005927495292030504 + 10.220103712927525j,
        lambda0=1550*NM, h=300*NM, eps_core=eps_SiO2, eps_cover=eps_Ag, 
        eps_substr=eps_Au, pol=emm.slab.Polarization.TM, mode_index=2, 
        parity=emm.slab.Parity.EVEN, neff_guess=1.0, max_tol=1e-16, max_iter=100
    )

def test_MDM_300nm_TM5():
    # For this mode, M = 2. But it is still
    # called TM5 to be consistent with naming
    # in table 4 of the paper
    default(
        solver=emm.slab.solve_d_strong, 
        neff_true=0.01577537648440215+12.831497704034192j,
        lambda0=1550*NM, h=300*NM, eps_core=eps_SiO2, eps_cover=eps_Ag, 
        eps_substr=eps_Au, pol=emm.slab.Polarization.TM, mode_index=2, 
        parity=emm.slab.Parity.ODD, neff_guess=1.0, max_tol=1e-16, max_iter=100
    )

def test_DMD_50nm_plasmon():
    default(
        solver=emm.slab.solve_dmd, 
        neff_true=1.461063388390511-0.0008056177063505853j,
        lambda0=1550*NM, h=50*NM, eps_core=eps_Ag, 
        eps_cover=eps_SiO2, eps_substr=eps_vac, parity=emm.slab.Parity.ODD,
        neff_guess=1.0 - 1j, max_tol=1e-16, max_iter=100
    )

@pytest.mark.skip('not working yet')
def test_DMD_100nm_low_energy_plasmon():
    default(
        solver=emm.slab.solve_dmd, 
        neff_true=1.4603853489134264-0.0006469974919998885j,
        lambda0=1550*NM, h=100*NM, eps_core=eps_Ag, 
        eps_cover=eps_SiO2, eps_substr=eps_SiO2, parity=emm.slab.Parity.EVEN,
        neff_guess=1.46 - 0.0001j, max_tol=1e-16, max_iter=1000
    )

@pytest.mark.skip('not working yet')
def test_DMD_100nm_high_energy_plasmon():
    default(
        solver=emm.slab.solve_dmd, 
        neff_true=1.4603853489134264-0.0006469974919998885j,
        lambda0=1550*NM, h=100*NM, eps_core=eps_Ag, 
        eps_cover=eps_SiO2, eps_substr=eps_SiO2, parity=emm.slab.Parity.ODD,
        neff_guess=1.46 - 0.0001j, max_tol=1e-16, max_iter=1000
    )

def test_dielectric_strong_sym_TE0():
    default(
        solver=emm.slab.solve_d_strong_sym, neff_true=3.21500035466944,
        lambda0=1550*NM, h=400*NM, eps_core=eps_Si, eps_clad=eps_SiO2,
        pol=emm.slab.Polarization.TE, mode_index=0, parity=emm.slab.Parity.EVEN,
        neff_guess=1.0, max_tol=1e-16, max_iter=100
    )

def test_dielectric_strong_sym_TE1():
    default(
        solver=emm.slab.solve_d_strong_sym, neff_true=2.277392558413031,
        lambda0=1550*NM, h=400*NM, eps_core=eps_Si, eps_clad=eps_SiO2,
        pol=emm.slab.Polarization.TE, mode_index=1, parity=emm.slab.Parity.ODD,
        neff_guess=1.0, max_tol=1e-16, max_iter=100
    )

def test_dielectric_strong_sym_TM0():
    default(
        solver=emm.slab.solve_d_strong_sym, neff_true=3.0053242806289244,
        lambda0=1550*NM, h=400*NM, eps_core=eps_Si, eps_clad=eps_SiO2,
        pol=emm.slab.Polarization.TM, mode_index=0, parity=emm.slab.Parity.EVEN,
        neff_guess=1.0, max_tol=1e-16, max_iter=100
    )

def test_dielectric_weak_sym_TM_odd():
    default(
        solver=emm.slab.solve_d_weak_sym, neff_true=1.6245324208522463,
        lambda0=1550*NM, h=400*NM, eps_core=eps_Si, eps_clad=eps_SiO2,
        pol=emm.slab.Polarization.TM, parity=emm.slab.Parity.ODD,
        neff_guess=1.0, max_tol=1e-16, max_iter=100
    )

def test_dielectric_weak_sym_TM_even():
    default(
        solver=emm.slab.solve_d_weak_sym, neff_true=1.4921116935578076,
        lambda0=1550*NM, h=400*NM, eps_core=eps_Si, eps_clad=eps_SiO2,
        pol=emm.slab.Polarization.TM, parity=emm.slab.Parity.EVEN,
        neff_guess=1.0, max_tol=1e-16, max_iter=100
    )

def test_MDM_50nm_gap_plasmon():
    default(
        solver=emm.slab.solve_mdm_sym, 
        neff_true=1.9660357596156883-0.015421133552370401j,
        lambda0=1550*NM, h=50*NM, eps_core=eps_SiO2,
        eps_clad=eps_Ag, parity=emm.slab.Parity.EVEN, neff_guess=2.0, 
        max_tol=1e-16, max_iter=100
    )

def test_MDM_3um_gap_plasmon_even():
    default(
        solver=emm.slab.solve_mdm_sym, 
        neff_true=1.4697636802205067-0.001743157363667023j,
        lambda0=1550*NM, h=3000*NM, eps_core=eps_SiO2,
        eps_clad=eps_Au, parity=emm.slab.Parity.EVEN, neff_guess=2.0, 
        max_tol=1e-16, max_iter=100
    )

def test_MDM_3um_gap_plasmon_odd():
    h = 1000 * NM
    eps_gap = eps_Si
    default(
        solver=emm.slab.solve_mdm, 
        neff_true=3.666521776733708-0.01067212473304136j,
        lambda0=1550*NM, h=h, eps_core=eps_gap,
        eps_cover=eps_Ag, eps_substr=eps_Ag,
        parity=emm.slab.Parity.EVEN, neff_guess=3.5 - 0.01j, 
        max_tol=1e-16, max_iter=1000
    )

    default(
        solver=emm.slab.solve_mdm_sym, 
        neff_true=3.666521776733705-0.010672124733040961j,
        lambda0=1550*NM, h=h, eps_core=eps_gap,
        eps_clad=eps_Ag, parity=emm.slab.Parity.EVEN, neff_guess=3.5 - 0.01j, 
        max_tol=1e-16, max_iter=1000
    )

    default(
        solver=emm.slab.solve_mdm, 
        neff_true=3.649771271471782-0.012172950643379398j,
        lambda0=1550*NM, h=h, eps_core=eps_gap,
        eps_cover=eps_Ag, eps_substr=eps_Ag,
        parity=emm.slab.Parity.ODD, neff_guess=3.5 - 0.01j, 
        max_tol=1e-16, max_iter=100
    )

    default(
        solver=emm.slab.solve_mdm_sym, 
        neff_true=3.6497712714717796-0.012172950643378696j,
        lambda0=1550*NM, h=h, eps_core=eps_gap,
        eps_clad=eps_Ag, parity=emm.slab.Parity.ODD, neff_guess=3.5 - 0.01j, 
        max_tol=1e-16, max_iter=100
    )

def main():
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
    # test_MDM_3um_gap_plasmon_even()
    # test_MDM_3um_gap_plasmon_odd()
    # test_MDM_300nm_TM1()
    # test_MDM_300nm_TM2()
    # test_MDM_300nm_TM3()
    # test_MDM_300nm_TM4()    
    # test_MDM_300nm_TM5()   
    # test_DMD_50nm_plasmon()         
    # test_DMD_100nm_low_energy_plasmon()
    # test_DMD_100nm_high_energy_plasmon()
    # test_dielectric_strong_sym_TE0()
    # test_dielectric_strong_sym_TE1()
    # test_dielectric_strong_sym_TM0()
    # test_dielectric_weak_sym_TM_even()
    # test_dielectric_weak_sym_TM_odd()
    # test_MDM_50nm_gap_plasmon()
    # test_MDM_3um_gap_plasmon_even()
    test_MDM_3um_gap_plasmon_odd()    
if __name__ == '__main__':
    main()