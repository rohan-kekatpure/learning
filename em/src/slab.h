# ifndef __SLAB3
# define  __SLAB3

#include <complex>
#include <limits.h>
#include <numbers>

using Real = double;
using Scalar = std::complex<Real>;


constexpr auto UM = static_cast<Real>(1e-6);
constexpr auto NM = static_cast<Real>(1e-9);
constexpr auto PI = static_cast<Real>(std::numbers::pi);
constexpr auto INFTY = std::numeric_limits<Real>::infinity();

enum class Polarization {TE, TM};
enum class Parity {ODD, EVEN};
enum class ModeType {DIELECTRIC_STRONG, DIELECTRIC_WEAK, DMD, MDM};

struct Waveguide {    
    Real coreThickness{1 * UM};
    Scalar coreEps{3.5 * 3.5};
    Scalar coverEps{1.0};
    Scalar substrEps{1.5 * 1.5};

    //ctor
    Waveguide(
        Real coreThickness, 
        Scalar coreEps, 
        Scalar coverEps, 
        Scalar substrEps
    ): coreThickness{coreThickness}, coreEps{coreEps}, 
       coverEps{coverEps}, substrEps{substrEps} {} 
};

struct ModeOptions {
    Real lambda0 = 1550 * NM; // vacuum wavelength    
    Polarization polarization = Polarization::TE;
    Parity parity = Parity::EVEN;
    ModeType type = ModeType::DIELECTRIC_STRONG;
    unsigned int index = 0;
    Scalar effectiveIndexGuess = 1.1;

    //ctors
    ModeOptions() {}

    ModeOptions(
        Real lambda0, Polarization pol, Parity par, 
        ModeType mt, unsigned int i, Scalar neff0
    ) 
    : polarization{pol}, parity{par}, type{mt}, 
    index{i}, effectiveIndexGuess{neff0} {}
};

struct SolverOptions {
    Real maxTol{1e-6};
    Real maxIter{1000};

    //ctors
    SolverOptions() {}
    
    SolverOptions(Real maxTol, Real maxIter)
    :maxTol{maxTol}, maxIter{maxIter} {}
};

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

class Solver {
    private: 
    // set and passed by caller
    Waveguide waveguide;
    SolverOptions solverOptions;
    ModeOptions modeOptions;    
    
    // struct to store intermediate results
    Solution sol; // private result; mutable

    // indicator for whether the solver is setup
    bool isSetup = false;

    public:
    // public readony version of solverContext
    const Solution& solution; // public result; readonly

    Solver(Waveguide wg, SolverOptions sopt, ModeOptions mopt)
    : waveguide{wg}, solverOptions{sopt}, modeOptions{mopt}, solution(sol) {}

    Solution solve();
    
};

#endif