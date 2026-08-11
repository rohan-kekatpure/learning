
#include <stdexcept>
#include <complex>
#include <cmath>
#include <numbers>
#include <stdexcept>
#include "slab.h"

namespace slab {

inline auto _rsd(Scalar x, Scalar y) {
    return std::sqrt((x - y) * (x + y));
}

inline auto _rss(Scalar x, Scalar y) {
    // std::hypot cannot take complex arguments
    // so we need to implement own
    return std::sqrt(x * x + y * y);
}

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
) {        
    Scalar gc, gs, Gc, Gs, num, denom;

    // Initialize solution s with default values
    const auto k0 = TWO * PI / lambda0;
    const auto Kc = k0 * std::sqrt(epsCore - epsCover);
    const auto Ks = k0 * std::sqrt(epsCore - epsSubstr);
    auto k = k0 * std::sqrt(epsCore - neffGuess * neffGuess);
    auto M = modeIndex;
    Scalar neffPrev, u, v;
    Real sign = parity == Parity::EVEN? 1 : -1;
    Solution s{};
    Scalar p, q;

    if (pol == Polarization::TE) {
        p = ONE;
        q = ONE;
    } else if (pol == Polarization::TM) {
        p = epsCore / epsCover;
        q = epsCore / epsSubstr;
    } else {
        throw(std::invalid_argument("`pol` can be Polarization::TE or Polarization::TM\n"));
    }

    // core loop
    while ((s.tol > maxTol) && (s.niter < maxIter)) {
        // core loop
        u = k;
        gc = _rsd(Kc, k);
        gs = _rsd(Ks, k);
        Gc = _rss(k, p * gc);
        Gs = _rss(k, q * gs);
        num = (p * q * gc * gs - k * k) + sign * Gc * Gs;
        denom = k * (p * gc + q * gs);
        v = (TWO / h) * (M * PI + std::atan(num / denom));  
        k = HALF * (u + v);

        // Convergence testing 
        neffPrev = s.effectiveIndex;
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
) {        
    // Initialize solution s with default values
    const auto k0 = TWO * PI / lambda0;
    const auto Kc = k0 * std::sqrt(epsCore - epsClad);
    auto k = k0 * std::sqrt(epsCore - neffGuess * neffGuess);
    auto M = modeIndex;
    Scalar neffPrev, u, v, t;
    Scalar p = pol == Polarization::TE ? ONE : epsCore/epsClad;
    Solution s{};

    // core loop
    while ((s.tol > maxTol) && (s.niter < maxIter)) {
        // core loop
        u = k;
        t = p * std::sqrt((Kc * Kc) / (k * k) - ONE);
        if (parity == Parity::EVEN) {
            v = (TWO / h) * (M * PI + std::atan(t));
        }
        else if (parity == Parity::ODD) {
            v = (TWO / h) * (M * PI - std::atan(ONE / t));
        } else {
            throw(std::invalid_argument("parity must be Parity::EVEN or Parity::ODD\n"));
        }
        k = HALF * (u + v);

        // Convergence testing 
        neffPrev = s.effectiveIndex;
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
) {    
    // Initialize solution s with default values
    const auto k0 = TWO * PI / lambda0;
    const auto Kc = k0 * std::sqrt(epsCore - epsCover);
    const auto Ks = k0 * std::sqrt(epsCore - epsSubstr);
    auto k = k0 * std::sqrt(epsCore - neffGuess * neffGuess);
    Scalar neffPrev, p, q;

    Real sign = parity == Parity::EVEN? -1 : 1;
    if (pol == Polarization::TE) {
        p = ONE;
        q = ONE;
    } else if (pol == Polarization::TM) {
        p = epsCore / epsCover;
        q = epsCore / epsSubstr;
    } else {
        throw(std::invalid_argument("`pol` can be Polarization::TE or Polarization::TM\n"));
    }

    Scalar gc, gs, Gc, Gs, num, denom, t1, t2, t3, t4, t5, p2q2, u, v;;
    Solution s{};
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
) {        
    // Initialize solution s with default values
    const auto k0 = TWO * PI / lambda0;    
    const auto Kc = k0 * std::sqrt(epsCore - epsClad);
    auto k = k0 * std::sqrt(epsCore - neffGuess * neffGuess);
    Scalar neffPrev, u, v, t, w;
    const auto p = pol == Polarization::TE ? ONE : epsCore/epsClad;
    Solution s{};

    // core loop
    while ((s.tol > maxTol) && (s.niter < maxIter)) {
        // core loop
        u = k;
        t = std::tan(k * h / TWO);
        if (parity == Parity::EVEN) {
            w = (ONE / p) * t;
        }
        else if (parity == Parity::ODD) {
            w = (ONE / p) / t;
        } else {
            throw(std::invalid_argument("parity must be Parity::EVEN or Parity::ODD\n"));
        }
        v = Kc / std::sqrt(ONE + w * w);
        k = HALF * (u + v);

        // Convergence testing 
        neffPrev = s.effectiveIndex;
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
) {        
    Scalar ac, as, S;

    // Initialize solution s with default values
    const auto k0 = TWO * PI / lambda0;
    const auto Kc = k0 * std::sqrt(epsCore - epsCover);
    const auto Ks = k0 * std::sqrt(epsCore - epsSubstr);
    const Real sign = parity == Parity::EVEN? 1 : -1;
    const auto p = epsCore / epsCover;
    const auto q = epsCore / epsSubstr;
    auto kappa = k0 * std::sqrt(neffGuess * neffGuess - epsCore);
    Scalar neffPrev, u, v, t1, t2;
    Solution s{};

    while ((s.tol > maxTol) && (s.niter < maxIter)) {        
        // core loop
        u = kappa;
        ac = _rss(Kc, kappa);
        as = _rss(Ks, kappa);
        S = HALF * (p * ac + q * as);
        t1 = S / std::tanh(kappa * h);
        t2 = std::sqrt(p * q * ac * as);
        v = -t1 + sign * std::sqrt((t1 + t2) * (t1 - t2));
        kappa = HALF * (u + v);
        
        // convergence testing
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

Solution solveMDMSym(
    const Real lambda0, 
    const Real h, 
    const Scalar epsCore, 
    const Scalar epsClad,
    const Parity parity, 
    const Scalar neffGuess, 
    const Real maxTol, 
    const unsigned int maxIter
) {        
    // Initialize solution s with default values
    const auto k0 = TWO * PI / lambda0;
    const auto Kc = k0 * std::sqrt(epsCore - epsClad);
    const Scalar p = epsCore / epsClad;
    Scalar neffPrev, u, v, t, pk;
    Solution s{};

    auto kappa = k0 * std::sqrt(epsCore - neffGuess * neffGuess);
    while ((s.tol > maxTol) && (s.niter < maxIter)) {
        // core loop
        u = kappa;
        pk = p * std::sqrt(kappa * kappa + Kc * Kc);
        t = std::tanh(kappa * h / TWO);

        // The ODD even switch is reverse to that in the paper.
        // The paper contains an error.
        if (parity == Parity::EVEN) {
            v = -pk / t;
        }
        else if (parity == Parity::ODD) {
            v = -pk * t;
        } else {
            throw(std::invalid_argument("Parity must be Parity::EVEN or Parity::ODD\n"));
        }

        kappa = HALF * (u + v);

        // Convergence testing 
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
) {        
    Scalar ac, as, S;

    // Initialize solution s with default values
    const auto k0 = TWO * PI / lambda0;
    const auto Qc = k0 * std::sqrt(epsCover - epsCore);
    const auto Qs = k0 * std::sqrt(epsSubstr - epsCore);
    const Real sign = parity == Parity::EVEN? 1 : -1;    
    const auto p = epsCore / epsCover;
    const auto q = epsCore / epsSubstr;
    
    Solution s{};
    Scalar t1, t2, neffPrev, a, b, A = k0, B = 0, xic, xis, u, v;
    auto kappa = k0 * std::sqrt(neffGuess * neffGuess - epsCore);
    while ((s.tol > maxTol) && (s.niter < maxIter)) {        
        // core loop
        u = kappa;
        t1 = kappa / std::tanh(kappa * h);
        t2 = kappa / std::sinh(kappa * h);
        a = -t1 + sign * std::sqrt(B * B + t2 * t2);
        b = std::sqrt(a * a + kappa * kappa + TWO * a * t1);
        v = std::sqrt((a + b) * (a + b) / (p * p) + Qc * Qc);
        kappa = HALF * (u + v);
        xic = _rsd(kappa, Qc);
        xis = _rsd(kappa, Qs);
        A = HALF * (p * xic + q * xis);
        B = HALF * (p * xic - q * xis);
        
        // convergence testing
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

Solution solveDMDSym(
    const Real lambda0, 
    const Real h, 
    const Scalar epsCore, 
    const Scalar epsClad,
    const Parity parity, 
    const Scalar neffGuess, 
    const Real maxTol, 
    const unsigned int maxIter
) {        
    // Initialize solution s with default values
    const auto k0 = TWO * PI / lambda0;
    const auto Qc = k0 * std::sqrt(epsClad - epsCore);
    auto kappa = k0 * std::sqrt(epsCore - neffGuess * neffGuess);
    const Scalar p = epsCore / epsClad;
    Scalar neffPrev, u, v, r, t;
    Solution s{};

    // core loop
    while ((s.tol > maxTol) && (s.niter < maxIter)) {
        // core loop
        u = kappa;
        t = std::tanh(kappa * h / TWO);
        if (parity == Parity::EVEN) {
            r = t / p ;            
        }
        else if (parity == Parity::ODD) {
            r = ONE/(t * p);            
        } else {
            throw(std::invalid_argument("Parity must be Parity::EVEN or Parity::ODD\n"));
        }
        v = Qc / std::sqrt(ONE - r * r);
        kappa = HALF * (u + v);

        // Convergence testing 
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

} // namespace Slab