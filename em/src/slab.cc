
#include <stdexcept>
#include <complex>
#include <cmath>
#include <numbers>
#include "slab.h"

inline auto _rsd(Scalar x, Scalar y) {
    return std::sqrt((x - y) * (x + y));
}

inline auto _rss(Scalar x, Scalar y) {
    // std::hypot cannot take complex arguments
    // so we need to implement own
    return std::sqrt(x * x + y * y);
}

Solution solveDStrong(
    const Real k0, 
    const Real h, 
    const Scalar epsCore, 
    const Scalar epsCover, 
    const Scalar epsSubstr, 
    const Scalar p, 
    const Scalar q, 
    unsigned int modeIndex, 
    const Parity parity, 
    const Scalar neffGuess, 
    const Real maxTol, 
    const unsigned int maxIter
) {        
    Scalar gc, gs, Gc, Gs, num, denom;

    // Initialize solution s with default values
    const auto Kc = k0 * std::sqrt(epsCore - epsCover);
    const auto Ks = k0 * std::sqrt(epsCore - epsSubstr);
    auto k = k0 * std::sqrt(epsCore - neffGuess * neffGuess);
    auto M = modeIndex;
    Scalar neffPrev;
    Real sign = parity == Parity::EVEN? 1 : -1;
    Solution s{};

    // core loop
    while ((s.tol > maxTol) && (s.niter < maxIter)) {
        neffPrev = s.effectiveIndex;
        gc = _rsd(Kc, k);
        gs = _rsd(Ks, k);
        Gc = _rss(k, p * gc);
        Gs = _rss(k, q * gs);
        num = (p * q * gc * gs - k * k) + sign * Gc * Gs;
        denom = k * (p * gc + q * gs);
        k = (TWO / h) * (M * PI + std::atan(num / denom));  
        s.effectiveIndex = std::sqrt(epsCore - (k * k) / (k0 * k0));
        s.tol = std::abs(s.effectiveIndex - neffPrev);
        s.niter++;
    }

    if (s.tol < maxTol) {
        s.converged = true;        
    }

    if (s.niter >= maxIter) {
        s.maxIterReached = true;
    }    

    return s;
}

Solution solveDWeak(
    const Real k0, 
    const Real h, 
    const Scalar epsCore, 
    const Scalar epsCover, 
    const Scalar epsSubstr, 
    const Scalar p, 
    const Scalar q, 
    const Parity parity, 
    const Scalar neffGuess, 
    const Real maxTol, 
    const unsigned int maxIter
) {    
    // Initialize solution s with default values
    const auto Kc = k0 * std::sqrt(epsCore - epsCover);
    const auto Ks = k0 * std::sqrt(epsCore - epsSubstr);
    auto k = k0 * std::sqrt(epsCore - neffGuess * neffGuess);
    Scalar neffPrev;
    Real sign = parity == Parity::EVEN? -1 : 1;
    Scalar gc, gs, Gc, Gs, num, denom;

    Solution s{};
    Scalar t1, t2, t3, t4, t5, p2q2, u, v;
    while ((s.tol > maxTol) && (s.niter < maxIter)) {
        // core loop
        u = k;
        gc = _rsd(Kc, k);
        gs = _rsd(Ks, k);
        Gc = _rss(k, p * gc);
        Gs = _rss(k, q * gs);
        t1 = p * q * Kc * Ks;
        t2 = Gc * Gs * std::cos(k * h);
        p2q2 = p * p * q * q;
        t3 = (p2q2 - ONE) * (k * k * k * k);
        t4 = p2q2 * (Kc * Kc + Ks * Ks);
        num = (t1 * t1) - (t2 * t2) + t3;
        denom = t4 + sign * TWO * t2;
        v = std::sqrt(num / denom);        
        k = HALF * (u + v);

        // convergence testing
        neffPrev = s.effectiveIndex;
        s.effectiveIndex = std::sqrt(epsCore - (k * k) / (k0 * k0));
        s.tol = std::abs(s.effectiveIndex - neffPrev);
        s.niter++;
        // printf("niter->%d, neff-> %0.16f +i(%0.16f)\n", 
        //     s.niter, s.effectiveIndex.real(), s.effectiveIndex.imag());
    }

    if (s.tol < maxTol) {
        s.converged = true;        
    }

    if (s.niter >= maxIter) {
        s.maxIterReached = true;
    }    

    return s;    
}

Solution solveMDM(
    const Real k0, 
    const Real h, 
    const Scalar epsCore, 
    const Scalar epsCover, 
    const Scalar epsSubstr, 
    const Scalar p, 
    const Scalar q, 
    const Parity parity, 
    const Scalar neffGuess, 
    const Real maxTol, 
    const unsigned int maxIter
) {        
    Scalar ac, as, S;

    // Initialize solution s with default values
    const auto Kc = k0 * std::sqrt(epsCore - epsCover);
    const auto Ks = k0 * std::sqrt(epsCore - epsSubstr);
    auto kappa = k0 * std::sqrt(neffGuess * neffGuess - epsCore);
    Scalar neffPrev, u, v;
    Real sign = parity == Parity::EVEN? 1 : -1;
    Solution s{};

    Scalar t1, t2;
    // core loop
    while ((s.tol > maxTol) && (s.niter < maxIter)) {        
        u = kappa;
        ac = _rss(Kc, kappa);
        as = _rss(Ks, kappa);
        S = HALF * (p * ac + q * as);
        t1 = S / std::tanh(kappa * h);
        t2 = std::sqrt(p * q * ac * as);
        v = -t1 + sign * std::sqrt((t1 + t2) * (t1 - t2));
        kappa = 0.5 * (u + v);

        neffPrev = s.effectiveIndex;
        s.effectiveIndex = std::sqrt(epsCore + (kappa * kappa) / (k0 * k0));
        s.tol = std::abs(s.effectiveIndex - neffPrev);
        s.niter++;
    }

    if (s.tol < maxTol) {
        s.converged = true;        
    }

    if (s.niter >= maxIter) {
        s.maxIterReached = true;
    }    

    return s;
}

Solution solveDMD() {
    return Solution();
}

Solution Solver::solve() {    
    const auto& pol = modeOptions.polarization;
    const auto& ef = waveguide.coreEps;
    const auto& es = waveguide.substrEps;
    const auto& ec = waveguide.coverEps;
    const auto& h = waveguide.coreThickness;
    const auto& nguess = modeOptions.effectiveIndexGuess;
    const auto& maxTol = solverOptions.maxTol;
    const auto& maxIter = solverOptions.maxIter;
    const auto& M = modeOptions.index;

    Scalar p = 1.0, q = 1.0;
    if (pol == Polarization::TM) {
        p = ef / ec;
        q = ef / es;
    }

    const auto k0 = TWO * PI / modeOptions.lambda0;    

    // Set setup status to true
    isSetup = true;    
    
    switch(modeOptions.type) {
        case ModeType::DIELECTRIC_STRONG:
            sol = solveDStrong(
                k0, h, ef, ec, es, p, q, M, modeOptions.parity, 
                nguess, maxTol, maxIter
            );
            break;
        case ModeType::DIELECTRIC_WEAK:
            sol = solveDWeak(
                k0, h, ef, ec, es, p, q, modeOptions.parity,
                nguess, maxTol, maxIter
            );
            break;
        case ModeType::MDM:
            sol = solveMDM(
                k0, h, ef, ec, es, p, q, modeOptions.parity, 
                nguess, maxTol, maxIter                
            );
            break;
        case ModeType::DMD:
            sol = solveDMD();
            break;
        default:
            break;
    }

    return sol;
}

