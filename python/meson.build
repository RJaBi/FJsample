project('FJsample', 'c',
  version : '0.2.0',
  license: 'MIT',
  meson_version: '>=0.64.0',
  default_options : ['warning_level=2'],
)

add_languages('fortran', native: false)


# Set the fortran compiler

env = environment()
FortCompiler = 'gfortran'
env.set('FC', FortCompiler)
env.set('FPM_FC', FortCompiler)

meson_path = meson.current_build_dir()

py_mod = import('python')
py = py_mod.find_installation(pure: false)
py_dep = py.dependency()


incdir_numpy = run_command(py,
  ['-c', 'import os; os.chdir(".."); import numpy; print(numpy.get_include())'],
  check : true
).stdout().strip()


incdir_f2py = run_command(py,
    ['-c', 'import os; os.chdir(".."); import numpy.f2py; print(numpy.f2py.get_include())'],
    check : true
).stdout().strip()


# fpm
fflags = '-g -fbacktrace -march=native -fPIC -funroll-loops -fstack-arrays -O3 -frepack-arrays -faggressive-function-elimination -fopenmp'
cflags = '-fPIC'
fpm_build_dir = meson_path / 'fpm_build'



#fpm_result = run_command(
run_command(
  'fpm',
  'install',
  '--profile',
  'release',
  '--compiler',
  FortCompiler,
  '--flag',
  fflags,
  '--c-flag',
  cflags,
  '--prefix',
  fpm_build_dir,
  check : true
)

# f2py
source_path = meson.project_source_root() / '..' / 'c_wrapper' / 'FJsample_c.f90'
FJsample_c_f90 = files(source_path)

FJsample_source = custom_target('FJsample_compiled.c',
  input: FJsample_c_f90,
  output: ['FJsample_compiledmodule.c', 'FJsample_compiled-f2pywrappers2.f90'],
  command: [
    py,
    '-m',
    'numpy.f2py',
    '@INPUT@',
    '-m',
    'FJsample_compiled',
    '--lower'
  ]
)

# Install Python sources
f_sources = ['FJsample/compiled/__init__.py']
py.install_sources(f_sources, subdir:'FJsample/compiled')

main_sources = ['FJsample/__init__.py', 'FJsample/main.py', 'FJsample/jack.py', 'FJsample/boot.py']
py.install_sources(main_sources, subdir:'FJsample')

# Extension fortran module
inc_np = include_directories(incdir_numpy, incdir_f2py, 'fpm_build' / 'include')

py.extension_module('FJsample_compiled',
  [FJsample_c_f90, FJsample_source],
  incdir_f2py / 'fortranobject.c',
  include_directories: [inc_np],
  dependencies : py_dep,
  link_args: ['-L' + 'fpm_build' / 'lib', '-lFJsample'],
  subdir: 'FJsample' / 'compiled',
  install : true,
)
