from FJsample.compiled import FJsample_c

from numpy import issubdtype, float64, complex128, asarray


def bootcomplement(*args):
    """
    Wraps the bootstrapping functions
    Does not do mean (complement0)
    """

    if len(args) != 2:
        raise TypeError(f'Unsupported number of arguments {len(args)}')
    data = args[0]
    data = asarray(data)
    nboot = args[1]
    if issubdtype(data.dtype, float64):
        return complement1(data, nboot)
    elif issubdtype(data.dtype, complex128):
        return complement1_wc(data, nboot)
    else:
        raise TypeError(f'Unsupported data type {data.dtype}')
    

def stddev(data):
    data = asarray(data)
    # the function returns the error and the bias
    # the [0] selects only the error
    if issubdtype(data.dtype, float64):
        return stddev_wp(data)
    elif issubdtype(data.dtype, complex128):
        return stddev_wc(data)
    else:
        raise TypeError(f'Unsupported data type {data.dtype}')


# C_DOUBLE
def complement1(data, nboot):
    return FJsample_c.bootcomplement1_ncon_c(ncon=data.shape[0], nboot=nboot, data=data)

def stddev_wp(c):
    return FJsample_c.stddev_wp_c(c)


# C_DOUBLE_complex

def complement1_wc(data, nboot):
    return FJsample_c.bootcomplement1_wc_ncon_c(ncon=data.shape[0], nboot=nboot, data=data)   
def stddev_wc(c):
    return FJsample_c.stddev_wp_c(c)
