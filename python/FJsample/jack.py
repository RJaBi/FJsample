from FJsample.compiled import FJsample_c

from numpy import issubdtype, float64, complex128, asarray


def complement(*args):
    """
    Wraps the jackknifing functions
    Does not do mean (complement0)
    """
    if len(args) == 1:
        data = args[0]
        data = asarray(data)
        if issubdtype(data.dtype, float64):
            return complement1(data)
        elif issubdtype(data.dtype, complex128):
            return complement1_wc(data)
        else:
            raise TypeError(f'Unsupported data type {data.dtype}')
    elif len(args) == 2:
        data, icon = args
        data = asarray(data)
        if issubdtype(data.dtype, float64):
            return complement2(data, icon)
        elif issubdtype(data.dtype, complex128):
            return complement2_wc(data, icon)
        else:
            raise TypeError(f'Unsupported data type {data.dtype}')
    elif len(args) == 3:
        data, icon, jcon = args
        data = asarray(data)
        if issubdtype(data.dtype, float64):
            return complement2(data, icon, jcon)
        elif issubdtype(data.dtype, complex128):
            return complement2_wc(data, icon, jcon)
        else:
            raise TypeError(f'Unsupported data type {data.dtype}')
    else:
        raise TypeError(f'Unsupported number of arguments {len(args)}')


def mean(data):
    data = asarray(data)
    if issubdtype(data.dtype, float64):
        return complement0(data)
    elif issubdtype(data.dtype, complex128):
        return complement0_wc(data)
    else:
        raise TypeError(f'Unsupported data type {data.dtype}')


def jackErr(data):
    data = asarray(data)
    if issubdtype(data.dtype, float64):
        return jackError_wp(data)
    elif issubdtype(data.dtype, complex128):
        return jackError_wc(data)
    else:
        raise TypeError(f'Unsupported data type {data.dtype}')


# C_DOUBLE
def complement0(data):
    return FJsample_c.complement0_c(data)


def complement1(data):
    return FJsample_c.complement1_c(data)


def complement2(data, icon):
    return FJsample_c.complement2_c(data, icon)


def complement3(data):
    return FJsample_c.complement3_c(data, icon, jcon)


def jackError_wp(c):
    return FJsample_c.jackerror_wp_c(c)


# C_DOUBLE_complex
def complement0_wc(data):
    return FJsample_c.complement0_wc_c(data)


def complement1_wc(data):
    return FJsample_c.complement1_wc_c(data)


def complement2_wc(data, icon):
    return FJsample_c.complement2_wc_c(data, icon)


def complement3_wc(data):
    return FJsample_c.complement3_wc_c(data, icon, jcon)


def jackError_wc(c):
    return FJsample_c.jackerror_wc_c(c)
