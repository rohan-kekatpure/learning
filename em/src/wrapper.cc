#include <pybind11/pybind11.h>
#include <pybind11/complex.h>
#include <pybind11/stl.h>
#include "slab.h"

namespace py = pybind11;

PYBIND11_MODULE(emm, m) {
    m.doc() = "Electromagnetics module";
    //submodule slab
    py::module_ slab_m = m.def_submodule("slab", "Solver functions for 1D Slab waveguides");

    // polarization states
    py::enum_<slab::Polarization>(slab_m, "Polarization", "Light polarization state")
        .value("TE", slab::Polarization::TE)
        .value("TM", slab::Polarization::TM)
        .export_values();

    // Mode parity
    py::enum_<slab::Parity>(slab_m, "Parity", "Mode field parity profile")
        .value("ODD", slab::Parity::ODD)
        .value("EVEN", slab::Parity::EVEN)
        .export_values();

    // Solution type
    py::enum_<slab::ModeType>(slab_m, "ModeType", "Waveguide physical regime")
        .value("DIELECTRIC_STRONG", slab::ModeType::DIELECTRIC_STRONG)
        .value("DIELECTRIC_WEAK", slab::ModeType::DIELECTRIC_WEAK)
        .value("DMD", slab::ModeType::DMD)
        .value("MDM", slab::ModeType::MDM)
        .export_values();

    py::class_<slab::Solution>(slab_m, "Solution", "Convergence data and solved effective index")
        .def(py::init<>(), "Default constructor")
        .def(py::init<slab::Real, unsigned int, bool, bool, slab::Scalar>(),
             py::arg("tol"), py::arg("niter"), py::arg("converged"),
             py::arg("max_iter_reached"), py::arg("effective_index"),
             "Explicit parameter constructor")
        .def_readwrite("effective_index", &slab::Solution::effectiveIndex)
        .def_readwrite("tol", &slab::Solution::tol)
        .def_readwrite("niter", &slab::Solution::niter)
        .def_readwrite("converged", &slab::Solution::converged)
        .def_readwrite("max_iter_reached", &slab::Solution::maxIterReached)
        .def("__repr__", [](const slab::Solution& s) {
            return "<slab.Solution neff=(" + 
                   std::to_string(s.effectiveIndex.real()) + 
                   (s.effectiveIndex.imag() >= 0 ? "+" : "") + 
                   std::to_string(s.effectiveIndex.imag()) + "j)" +
                   ", converged=" + (s.converged ? "True" : "False") +
                   ", niter=" + std::to_string(s.niter) +
                   ", tol=" + std::to_string(s.tol) + ">";
        });


    // 1. Dielectric Strong
    slab_m.def("solve_d_strong", &slab::solveDStrong,
        py::kw_only(),
        py::arg("lambda0"),
        py::arg("h"),
        py::arg("eps_core"),
        py::arg("eps_cover"),
        py::arg("eps_substr"),
        py::arg("pol"),
        py::arg("mode_index"),
        py::arg("parity"),
        py::arg("neff_guess"),
        py::arg("max_tol") = 1e-16,
        py::arg("max_iter") = 100,
        "Solve asymmetric strongly guided dielectric waveguide mode"
    );

    slab_m.def("solve_d_strong_sym", &slab::solveDStrongSym,
        py::kw_only(),
        py::arg("lambda0"),
        py::arg("h"),
        py::arg("eps_core"),
        py::arg("eps_clad"),
        py::arg("pol"),
        py::arg("mode_index"),
        py::arg("parity"),
        py::arg("neff_guess"),
        py::arg("max_tol") = 1e-16,
        py::arg("max_iter") = 100,
        "Solve symmetric strongly guided dielectric waveguide mode"
    );

    // 2. Dielectric Weak
    slab_m.def("solve_d_weak", &slab::solveDWeak,
        py::kw_only(),
        py::arg("lambda0"),
        py::arg("h"),
        py::arg("eps_core"),
        py::arg("eps_cover"),
        py::arg("eps_substr"),
        py::arg("pol"),
        py::arg("parity"),
        py::arg("neff_guess"),
        py::arg("max_tol") = 1e-16,
        py::arg("max_iter") = 100,
        "Solve asymmetric weakly guided dielectric waveguide mode"
    );

    slab_m.def("solve_d_weak_sym", &slab::solveDWeakSym,
        py::kw_only(),
        py::arg("lambda0"),
        py::arg("h"),
        py::arg("eps_core"),
        py::arg("eps_clad"),
        py::arg("pol"),
        py::arg("parity"),
        py::arg("neff_guess"),
        py::arg("max_tol") = 1e-16,
        py::arg("max_iter") = 100,
        "Solve symmetric weakly guided dielectric waveguide mode"
    );

    slab_m.def("solve_mdm", &slab::solveMDM,
        py::kw_only(),
        py::arg("lambda0"),
        py::arg("h"),
        py::arg("eps_core"),
        py::arg("eps_cover"),
        py::arg("eps_substr"),
        py::arg("parity"),
        py::arg("neff_guess"),
        py::arg("max_tol") = 1e-16,
        py::arg("max_iter") = 100,
        "Solve asymmetric Metal-Dielectric-Metal plasmonic waveguide mode"
    );

    slab_m.def("solve_mdm_sym", &slab::solveMDMSym,
        py::kw_only(),
        py::arg("lambda0"),
        py::arg("h"),
        py::arg("eps_core"),
        py::arg("eps_clad"),
        py::arg("parity"),
        py::arg("neff_guess"),
        py::arg("max_tol") = 1e-16,
        py::arg("max_iter") = 100,
        "Solve symmetric Metal-Dielectric-Metal plasmonic waveguide mode"
    );

    // 4. Plasmonic DMD
    slab_m.def("solve_dmd", &slab::solveDMD,
        py::kw_only(),
        py::arg("lambda0"),
        py::arg("h"),
        py::arg("eps_core"),
        py::arg("eps_cover"),
        py::arg("eps_substr"),
        py::arg("parity"),
        py::arg("neff_guess"),
        py::arg("max_tol") = 1e-16,
        py::arg("max_iter") = 100,
        "Solve asymmetric Dielectric-Metal-Dielectric plasmonic waveguide mode"
    );

    slab_m.def("solve_dmd_sym", &slab::solveDMDSym,
        py::kw_only(),
        py::arg("lambda0"),
        py::arg("h"),
        py::arg("eps_core"),
        py::arg("eps_clad"),
        py::arg("parity"),
        py::arg("neff_guess"),
        py::arg("max_tol") = 1e-16,
        py::arg("max_iter") = 100,
        "Solve symmetric Dielectric-Metal-Dielectric plasmonic waveguide mode"
    );
}