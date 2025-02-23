import FJsample.jack as FJ
import numpy as np
import gvar as gv

# import matplotlib.pyplot as plt  # type: ignore


################################################################
## SETUP DATA
def expFunc(x, p):
    """
        A sum of forward exponentials
        in form suitable for lsqfit
        p[A], p[E] are amplitudes and energies
        """
    try:
        ans = np.zeros(len(x))
        for A, E in zip(p['A'], p['E']):
            term = A * np.exp(-E * x[:])
            ans[:] = ans[:] + term[:]
        return ans
    except TypeError:
        # This just handles gvar as input
        ans = np.zeros(len(x), dtype=object)
        if np.shape(p['A']) == () and np.shape(p['E']) == ():
            pA = [p['A']]
            pE = [p['E']]
        else:
            pA = p['A']
            pE = p['E']
        for A, E in zip(pA, pE):
            term = A * np.exp(-E * x[:])
            ans[:] = ans[:] + term[:]
        return ans


def nconExpFunc(x, p):
    """
    Here we have A, E as 2dim arrays
    The first index is the icon or sample
    The 2nd is the state
    """
    if len(np.shape(p['E'])) == 1 or len(np.shape(p['E'])) == 1:
        # only a single state
        # so broadcast it two 2dim
        Ap = np.empty([len(p['A']), 1])
        Ep = np.empty([len(p['A']), 1])
        Ap[:, 0] = p['A']
        Ep[:, 0] = p['E']
    else:
        Ap = p['A']
        Ep = p['E']
    out = np.empty([np.shape(Ap)[0], len(x)])
    for ii in range(0, np.shape(Ap)[0]):
        out[ii, :] = expFunc(x, {'A': Ap[ii, :], 'E': Ep[ii, :]})
    return out


###########################################################


def main():
    """
    Let's do some simple examples
    Uncorrelated, only 2 uncorrelated parameters
    """

    # Generate x values
    xVals = np.asarray(range(1, 32))
    A = 1.0
    E = 0.6
    # Generate the plot for truth
    p = {'A': [A], 'E': [E]}
    yTrue = expFunc(xVals, p)

    print('Truth', yTrue[0])

    rng = np.random.default_rng(seed=100)
    nSample = 100
    pVecs = {
        'A': rng.normal(loc=A, scale=A * 0.02, size=nSample),
        'E': rng.normal(loc=E, scale=E * 0.05, size=nSample)
    }
    ySamples = nconExpFunc(xVals, pVecs)
    # ySamples is [nSample, len(x)]

    # Take 1st order jackknifes
    yJ1 = np.empty([nSample, len(xVals)])
    yJErr = np.empty(len(xVals))
    # Mean
    yM = np.empty(len(xVals))
    for ii in range(0, len(xVals)):
        yJ1[:, ii] = FJ.complement(ySamples[:, ii])
        yM[ii] = FJ.mean(ySamples[:, ii])
        yJErr[ii] = FJ.jackErr(yJ1[:, ii])

    print('FJ', yM[0], yJErr[0])
    # Take gvar
    yGV = gv.dataset.avg_data(ySamples)
    print('GV from samples', gv.mean(yGV[0]), gv.sdev(yGV[0]))

    yJGV = gv.dataset.avg_data(yJ1, spread=True, median=False)
    print('GV from jack', gv.mean(yJGV[0]), gv.sdev(yJGV[0]))
    print('The above is too small by factor of (nSample - 1)**2.0')
    print('GV from Jack (sdev * (nSample - 1)**0.5)', gv.sdev(yJGV[0]) * np.sqrt(nSample - 1))
    # An alternative way to do this would be
    yJGV_Covariance = gv.evalcov(yJGV)  # First get covariance matrix
    yJGV_Corrected = gv.gvar(gv.mean(yJGV), (nSample - 1) * yJGV_Covariance)
    print('GV from jack Corrected', gv.mean(yJGV_Corrected[0]), gv.sdev(yJGV_Corrected[0]))

    # Let's go the other way now
    # Let's generate a whole bunch of samples from some gvar data
    # Have to expand the cov matrix by (nSample -1) to make this work with gv.dataset.avg_data
    yGVE = gv.gvar(gv.mean(yGV), (nSample - 1) * gv.evalcov(yGV))
    yGVSamples = gv.sample(yGVE, nbatch=nSample, mode='lbatch')
    yGVSD = gv.dataset.avg_data(yGVSamples)
    print('GV Samples from samples', gv.mean(yGVSD[0]), gv.sdev(yGVSD[0]))
    # and a jackknfie test
    # Take 1st order jackknifes
    yGVSJ1 = np.empty([nSample, len(xVals)])
    yGVSJErr = np.empty(len(xVals))
    # Mean
    yGVSM = np.empty(len(xVals))
    for ii in range(0, len(xVals)):
        yGVSJ1[:, ii] = FJ.complement(yGVSamples[:, ii])
        yGVSM[ii] = FJ.mean(yGVSamples[:, ii])
        yGVSJErr[ii] = FJ.jackErr(yGVSJ1[:, ii])

    print('FJ GV Samples', yGVSM[0], yGVSJErr[0])

    # Use A, and E as gvar
    GVP = gv.dataset.avg_data(pVecs)
    print('GVP', GVP)
    yGVP = expFunc(xVals, GVP)
    print('A E GV', gv.mean(yGVP[0]), gv.sdev(yGVP[0]))


if __name__ == '__main__':
    main()
