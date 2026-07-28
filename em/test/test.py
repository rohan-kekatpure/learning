import sys

from pathlib import Path

from IPython import embed

sys.path.append('../build')
import emm

NM = 1e-9
ef = 3.500
es = 1.45
ec = 1.000
wg = emm.Waveguide(1000 * NM, ef**2, ec**2, es**2)

# modeopts = emm.ModeOptions(
#     1550*NM, emm.Polarization.TE, emm.Parity.EVEN,
#     emm.ModeType.DIELECTRIC_STRONG, 1, 1.5
# )

modeopts = emm.ModeOptions(
    1550*NM, emm.Polarization.TE, emm.Parity.EVEN,
    emm.ModeType.DIELECTRIC_WEAK, 1, 1.5
)

solveropts = emm.SolverOptions(1e-16, 1000)

solver = emm.Solver(wg, solveropts, modeopts)

sol = solver.solve()
print(f'converged->{sol.converged}, neff->{sol.effectiveIndex}')
