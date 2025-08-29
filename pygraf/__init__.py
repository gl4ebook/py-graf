import warnings  # noqa

warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")

try:
    import numpy  # noqa

except ModuleNotFoundError:
    print(
        "Using Py-graf requires the python packages Numpy. "
        "Please see the docs for installation instructions."
    )
    raise

from pygraf.version import VERSION as __version__  # noqa