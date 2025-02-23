# FJsample

Jackknife resampling in Fortran with python bindings

### Python
Build this library for python via
```
cd python
pip install -r build-requirements.txt
pip install -e . --no-build-isolation
```

This will give the python module `FJsample`

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

---

Generated with cookiecutter template:

[https://github.com/SalvadorBrandolin/fortran_meson_py](https://github.com/SalvadorBrandolin/fortran_meson_py)
