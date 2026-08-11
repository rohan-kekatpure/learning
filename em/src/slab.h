# ifndef __SLAB
# define  __SLAB

#include <complex>
#include <limits.h>
#include <numbers>

namespace slab {
using Real = double;
using Scalar = std::complex<Real>;

constexpr Real PI = std::numbers::pi_v<Real>;
constexpr Real ONE = 1., TWO = 2., HALF = 0.5;
constexpr auto INFTY = std::numeric_limits<Real>::infinity();

enum class Polarization {TE, TM};
enum class Parity {ODD, EVEN};
enum class ModeType {DIELECTRIC_STRONG, DIELECTRIC_WEAK, DMD, MDM};

struct Solution {
    // converged values
    Scalar effectiveIndex = 1.0;

    // convergence info
    Real tol = INFTY;
    unsigned int niter = 0;
    bool converged = false;
    bool maxIterReached = false;

    //ctor
    Solution() {}

    Solution(
        Real tol, unsigned int niter, bool converged, 
        bool maxIterReached, Scalar effectiveIndex
    ): tol{tol}, niter{niter}, converged{converged}, 
    maxIterReached{maxIterReached}, effectiveIndex{effectiveIndex} {}

};

Solution solveDStrong(
    const Real lambda0, 
    const Real h, 
    const Scalar epsCore, 
    const Scalar epsCover, 
    const Scalar epsSubstr, 
    const Polarization pol,
    const unsigned int modeIndex, 
    const Parity parity, 
    const Scalar neffGuess, 
    const Real maxTol, 
    const unsigned int maxIter
);

Solution solveDStrongSym(
    const Real lambda0, 
    const Real h, 
    const Scalar epsCore, 
    const Scalar epsClad,
    const Polarization pol, 
    const unsigned int modeIndex, 
    const Parity parity, 
    const Scalar neffGuess, 
    const Real maxTol, 
    const unsigned int maxIter
); 

Solution solveDWeak(
    const Real lambda0, 
    const Real h, 
    const Scalar epsCore, 
    const Scalar epsCover, 
    const Scalar epsSubstr, 
    const Polarization pol,
    const Parity parity, 
    const Scalar neffGuess, 
    const Real maxTol, 
    const unsigned int maxIter
);

Solution solveDWeakSym(
    const Real lambda0, 
    const Real h, 
    const Scalar epsCore, 
    const Scalar epsClad,
    const Polarization pol, 
    const Parity parity, 
    const Scalar neffGuess, 
    const Real maxTol, 
    const unsigned int maxIter
);

Solution solveMDM(
    const Real lambda0, 
    const Real h, 
    const Scalar epsCore, 
    const Scalar epsCover, 
    const Scalar epsSubstr, 
    const Parity parity, 
    const Scalar neffGuess, 
    const Real maxTol, 
    const unsigned int maxIter
);

Solution solveMDMSym(
    const Real lambda0, 
    const Real h, 
    const Scalar epsCore, 
    const Scalar epsClad,
    const Parity parity, 
    const Scalar neffGuess, 
    const Real maxTol, 
    const unsigned int maxIter
);

Solution solveDMD(
    const Real lambda0, 
    const Real h, 
    const Scalar epsCore, 
    const Scalar epsCover, 
    const Scalar epsSubstr, 
    const Parity parity, 
    const Scalar neffGuess, 
    const Real maxTol, 
    const unsigned int maxIter
);

Solution solveDMDSym(
    const Real lambda0, 
    const Real h, 
    const Scalar epsCore, 
    const Scalar epsClad,
    const Parity parity, 
    const Scalar neffGuess, 
    const Real maxTol, 
    const unsigned int maxIter
);

} // namespace slab
#endif