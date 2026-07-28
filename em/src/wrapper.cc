#include <pybind11/pybind11.h>
#include <pybind11/complex.h>
#include "slab.h"

namespace py = pybind11;

PYBIND11_MODULE(emm, m) {
    m.doc() = "Three-layer dielectric slab waveguide solver";

    py::enum_<Polarization>(m, "Polarization")
        .value("TE", Polarization::TE)
        .value("TM", Polarization::TM)
        .export_values();
    
    py::enum_<Parity>(m, "Parity")
        .value("ODD", Parity::ODD)
        .value("EVEN", Parity::EVEN);

    py::enum_<ModeType>(m, "ModeType")
        .value("DIELECTRIC_STRONG", ModeType::DIELECTRIC_STRONG)
        .value("DIELECTRIC_WEAK", ModeType::DIELECTRIC_WEAK)        
        .value("DMD", ModeType::DMD)
        .value("MDM", ModeType::MDM);

    py::class_<Waveguide>(m, "Waveguide")
        .def(py::init<double, Scalar, Scalar, Scalar>(),
            py::arg("core_thickness") = 1 * UM,
            py::arg("core_eps") = Scalar(3.5 * 3.5),
            py::arg("cover_eps") = Scalar(1.0),
            py::arg("substr_eps") = Scalar(1.5 * 1.5)
        )
        // Read-write attributes
        .def_readwrite("core_thickness", &Waveguide::coreThickness)
        .def_readwrite("core_eps", &Waveguide::coreEps)
        .def_readwrite("cover_eps", &Waveguide::coverEps)
        .def_readwrite("substr_eps", &Waveguide::substrEps)
        .def("__repr__", [](const Waveguide& w) {
            return "<Waveguide core_thickness=" + std::to_string(w.coreThickness) + ">";
        });

    py::class_<ModeOptions>(m, "ModeOptions")
        .def(py::init<>())
        
        .def(py::init<double, Polarization, Parity, ModeType, unsigned int, Scalar>(),
            py::arg("lambda0") = 1550 * NM,
            py::arg("polarization") = Polarization::TE,
            py::arg("parity") = Parity::EVEN,
            py::arg("type") = ModeType::DIELECTRIC_STRONG,
            py::arg("index") = 0,
            py::arg("effective_index_guess") = Scalar(1.1)
        )

        .def_readwrite("lambda0", &ModeOptions::lambda0)
        .def_readwrite("polarization", &ModeOptions::polarization)
        .def_readwrite("parity", &ModeOptions::parity)
        .def_readwrite("type", &ModeOptions::type)
        .def_readwrite("index", &ModeOptions::index)
        .def_readwrite("effective_index_guess", &ModeOptions::effectiveIndexGuess)

        .def("__repr__", [](const ModeOptions& opts) {
            return "<ModeOptions lambda0=" + std::to_string(opts.lambda0) + 
                   " index=" + std::to_string(opts.index) + ">";
        });        

    py::class_<SolverOptions>(m, "SolverOptions")
        .def(py::init<>())

        .def(py::init<double, double>(),
            py::arg("max_tol") = 1e-6,
            py::arg("max_iter") = 1000.0
        )

        .def_readwrite("max_tol", &SolverOptions::maxTol)
        .def_readwrite("max_iter", &SolverOptions::maxIter)

        .def("__repr__", [](const SolverOptions& opt) {
            return "<SolverOptions max_tol=" + std::to_string(opt.maxTol) +
                   " max_iter=" + std::to_string(opt.maxIter) + ">";
        });        

    py::class_<Solution>(m, "Solution")
        .def(py::init<>())

        .def(py::init<double, unsigned int, bool, bool, Scalar>(),
            py::arg("tol") = std::numeric_limits<double>::infinity(),
            py::arg("niter") = 0,
            py::arg("converged") = false,
            py::arg("max_iter_reached") = false,
            py::arg("effectiveIndex") = Scalar(1.0)
        )
        .def_readonly("effectiveIndex", &Solution::effectiveIndex)
        .def_readonly("tol", &Solution::tol)
        .def_readonly("niter", &Solution::niter)
        .def_readonly("converged", &Solution::converged)
        .def_readonly("max_iter_reached", &Solution::maxIterReached)
        .def("__repr__", [](const Solution& sol) {
            std::string status = sol.converged ? "Converged" : "Failed";
            return "<Solution status=" + status + 
                   " niter=" + std::to_string(sol.niter) + 
                   " tol=" + std::to_string(sol.tol) + ">";
        });    

    py::class_<Solver>(m, "Solver")
        .def(py::init<Waveguide, SolverOptions, ModeOptions>(),
            py::arg("waveguide"),
            py::arg("solver_options"),
            py::arg("mode_options")
        )

        .def("solve", &Solver::solve, 
             "Executes the solver pipeline and returns a Solution struct.")

        // Read-only access to the public 'solution' member reference
        // py::return_value_policy::reference_internal ties the lifetime of 
        // the returned solution to the Solver instance to avoid dangling pointers.
        .def_property_readonly("solution", 
            [](const Solver& self) -> const Solution& {
                return self.solution;
            },
            py::return_value_policy::reference_internal,
            "Read-only access to the current Solution state."
        );        
}