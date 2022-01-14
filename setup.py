import os
import sys
import setuptools
import versioneer


with open("README.md", "r") as fh:
    long_description = fh.read()

def check_cython():
    """
    Check to see if Cython is installed and able to compile extensions (which
    requires a C compiler and the Python headers to be installed).
    Return True on success, False on failure.
    """
    argv_org = list(sys.argv)
    try:
        from Cython.Build import cythonize
        sys.argv = argv_org[:1] + ["build_ext"]
        setuptools.setup(name="foo", version="1.0.0",
                         ext_modules=cythonize(["ndindex/__init__.py"]))
    except:
        return False
    finally:
        sys.argv = argv_org
    return True


if os.getenv("CYTHONIZE_NDINDEX") is None:
    CYTHONIZE_NDINDEX = check_cython()
else:
    try:
        CYTHONIZE_NDINDEX = bool(int(os.getenv("CYTHONIZE_NDINDEX")))
    except ValueError:
        sys.exit("Acceptable values for CYTHONIZE_NDINDEX are '0' and '1', "
                 "got: %r" % os.getenv("CYTHONIZE_NDINDEX"))

if CYTHONIZE_NDINDEX:
    from Cython.Build import cythonize
    ext_modules = cythonize(["ndindex/*.py"])
else:
    ext_modules = []

setuptools.setup(
    name="ndindex",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author="Quansight Labs",
    description="A Python library for manipulating indices of ndarrays.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://quansight-labs.github.io/ndindex/",
    packages=['ndindex', 'ndindex.tests'],
    ext_modules=ext_modules,
    license="MIT",
    install_requires=[
        "numpy",
        "sympy",
    ],
    tests_require=[
        'pytest',
        'hypothesis',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)

print("CYTHONIZE_NDINDEX: %r" % CYTHONIZE_NDINDEX)
