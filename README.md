# FJsample

Jackknife & Bootstrap resampling in Fortran with python bindings.

Current functionality includes 1st, 2nd, 3rd order jackknife sub ensemble generation, jackknife error estimation (not covariance!), a calculation of the mean, bootstrap resampling and a standard deviation calculation. For details see the example program(s) in `app`.
      

### Compiler support
`do concurrent` locality specifier is required by default. This is in the bootstrap code in `src/boot.f90`. gfortran15.1+, intel IFX 2024+, NVidia NVHPC all have this support.

### Build with [fortran-lang/fpm](https://github.com/fortran-lang/fpm)
Fortran Package Manager (fpm) is a great package manager and build system for Fortran.
You can build using provided `fpm.toml`:
```bash
fpm build
```
To use `FJsample` within your fpm project, add the following to your `fpm.toml` file:
```toml
[dependencies]
FJsample = { git="https://github.com/RJabi/FJsample.git" }
```

### Python
Build this library for python via
```
cd python
pip install -r build-requirements.txt
pip install -e . --no-build-isolation
```

This will give the python module `FJsample`

Alternatively it may be used by including it as a submodule in your repository and then using a conda environment file which looks something like
```
name: G2L_CSRun
channels:
  - conda-forge
dependencies:
  - conda-forge::fpm            # Fortran package manager
  - conda-forge::meson-python   # For building fortran for use in python
  - conda-forge::ninja
  - conda-forge::pip
  - conda-forge::numpy
  - pip:
       - ../../libs/FJsample/python
```

If you have difficulty due to the do-concurrent locality specifier, check the `python/meson.build` to specify a different compiler. Note that you should also export that compiler to your (shell) environment using i.e.

```
export FC=gfortran15.1
export FPM_FC=gfortran15.1
```
as it is difficult to set the compiler manually in the meson build system. Currently the `meson.build` file is hardcoded to use a compiler called `gfortran15.1`.

---

Generated with cookiecutter template:

[https://github.com/SalvadorBrandolin/fortran_meson_py](https://github.com/SalvadorBrandolin/fortran_meson_py)
