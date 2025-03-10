import sys

import FJsample.jack as FJ
import numpy as np
import gvar as gv
from scipy import linalg
import opt_einsum  # type: ignore
import matplotlib.pyplot as plt  # type: ignore
import matplotlib as mpl  # type: ignore

# For generating the correlator data
from singleCorrelator import expFunc, nconExpFunc


def effE_forward(massdt: np.float64, GJ2: np.ndarray) -> np.ndarray:
    """
    The standard forward finite difference effective mass
    """
    try:
        eff = (1.0 / massdt) * np.log(GJ2 / np.roll(GJ2, -int(massdt), axis=len(GJ2.shape) - 1))
        return eff
    except ZeroDivisionError:
        # List to accomodate gvar's easily
        z = []
        if len(GJ2.shape) == 1:
            for nt, v in enumerate(GJ2):
                try:
                    vf = GJ2[nt + int(massdt)]
                except IndexError:
                    if nt == (len(GJ2) + 1 - int(massdt)):
                        vf = GJ2[0 + int(massdt) - 1]
                try:
                    z.append((1.0 / massdt) * np.log(v / vf))
                except ZeroDivisionError:
                    # arccosh(1) = 0
                    z.append(gv.gvar(0, 0))
        else:
            # Here this should work for jackknife subensembles
            for nt in range(0, np.shape(GJ2)[-1]):
                v = GJ2[..., nt]
                try:
                    vf = GJ2[..., nt + int(massdt)]
                except IndexError:
                    if nt == (len(GJ2) + 1 - int(massdt)):
                        vf = GJ2[..., 0 + int(massdt) - 1]
                try:
                    z.append((1.0 / massdt) * np.log(v / vf))
                except ZeroDivisionError:
                    z.append(np.zeros(np.shape(v)))
        return np.asarray(z)


def main():
    """
    Do a GEVP
    """

    # Generate x values
    xVals = np.asarray(range(1, 32))
    # NSamples
    nSample = 400

    # 4 operators
    A = np.asarray([[1.0, 0.4, 0.2, 0.5], [0.4, 1.0, 0.45, 0.7], [0.2, 0.45, 1.0, 0.6],
                    [0.5, 0.7, 0.6, 1.0]])
    # Make Covariances
    # We will make it symmetric
    ACov = [[0.02, 0.0002, 0.00035, 0.0004], [1, 0.02, 0.0003, 0.00045],
            [None, None, 0.02, 0.00054], [None, None, None, 0.02]]
    # Extract the upper triangular part
    upper_tri = np.triu(ACov)
    # Copy the upper triangular part to the lower triangular part
    ACov = upper_tri + upper_tri.T - np.diag(np.diag(ACov))
    ACov = ACov**5.0  # Just making the uncertanties much smaller
    EMean = np.asarray([0.6, 0.9, 1.2, 1.5])
    # Different states have different uncertainties on mean
    # In a way this reflects Parisi-Lepage scaling
    E = gv.gvar(EMean, 0.05 * EMean * np.asarray([0.5, 0.7, 1.0, 1.2]))
    # Make the data
    GEVPData = {}
    pData = {}
    GEVPArray = np.empty([len(xVals), 4, 4], dtype=object)
    for ii in range(0, len(A)):
        for jj in range(0, len(A)):
            lab = f'A{ii}_A{jj}'
            AErr = A * A * np.outer(ACov[ii, :], ACov[jj, :])
            # Make symmetric
            upper_tri = np.triu(AErr)
            # Copy the upper triangular part to the lower triangular part
            AErr = upper_tri + upper_tri.T - np.diag(np.diag(AErr))
            thisA = gv.gvar(A[ii] * A[jj], AErr)
            pData.update({lab: {'A': thisA, 'E': E}})
            thisY = expFunc(xVals, pData[lab])
            GEVPData.update({lab: thisY})
            GEVPArray[:, ii, jj] = thisY

    # Let's solve the GEVP
    t0 = 2
    dt = 3
    left = np.empty([4, 4], dtype=object)
    right = np.empty([4, 4], dtype=object)
    for ii in range(0, len(A)):
        for jj in range(0, len(A)):
            lab = f'A{ii}_A{jj}'
            left[ii, jj] = GEVPData[lab][t0 + dt]
            right[ii, jj] = GEVPData[lab][t0]
    #print('left', left)
    #print('right', right)

    # Can't use GV in linalg.eig!!
    left = gv.mean(left)
    right = gv.mean(right)
    w, vl, vr = linalg.eig(left, right, left=True, right=True)
    w = np.real(w)  # It's guaranteed real but for machine precision...
    print('w', w)
    print('vl', vl)
    print('vr', vr)

    # Do the projection correlated to plot to show the data isn't crazy
    GProj = np.empty([len(xVals), 4], dtype=object)
    # Use einsum to do multiplication
    conString = 'ia,tij,ja->ta'
    # opt_einsum required as it is 'objects' (gvars)
    contracted = opt_einsum.contract(conString, vl, GEVPArray, vr, backend='object')
    fig, ax = plt.subplots(figsize=(16.6, 11.6))
    legendLabels = []
    for ii in range(0, 4):
        GProj[:, ii] = contracted[..., ii]
        # Calculate effective mass for projected correlator
        effE = effE_forward(1.0, GProj[:, ii])
        ax.errorbar(xVals,
                    y=gv.mean(effE),
                    yerr=gv.sdev(effE),
                    label=f'GEVP {ii}',
                    marker='d',
                    linestyle='')
        # calculate effective mass for diagonal correlators
        effEiiii = effE_forward(1.0, GEVPArray[:, ii, ii])
        ax.errorbar(xVals,
                    y=gv.mean(effEiiii),
                    yerr=gv.sdev(effEiiii),
                    label=f'A{ii}_A{ii}',
                    marker='d',
                    linestyle='')
        # Plot Truths
        ax.axhline(gv.mean(E[ii]), linestyle='--', color='gray')
        ax.axhspan(gv.mean(E[ii]) - gv.sdev(E[ii]),
                   gv.mean(E[ii]) + gv.sdev(E[ii]),
                   alpha=0.25,
                   color='gray',
                   linewidth=0)
        legendLabels.append(f'GEVP {ii}')
        legendLabels.append(f'A{ii}_A{ii}')
    # plot limits
    ax.set_ylim([0, 2])
    # Cut off just before end
    ax.set_xlim([0, xVals[-1] - 1])
    # labels
    ax.set_ylabel('$a_\\tau\\,E$')
    ax.set_xlabel('$\\tau/ a_\\tau$')
    # add a label to the truth lines
    truth_line = mpl.lines.Line2D([], [], color='gray', label='$\\text{Truth}$', ls='--')
    # Get the current legend
    legend = ax.legend()
    # Add the new line to the legend
    legend.legend_handles.append(truth_line)
    legendLabels.append('$\\text{Truth}$')
    # Update the legend
    ax.legend(handles=legend.legend_handles, labels=legendLabels, loc='best', ncol=2)
    # show
    plt.savefig('GEVP_GVMean.pdf')
    plt.close()

    # Now generate some samples for each of the correlators as we did in the singleCorrelator.py example
    # GEVPArraySamples = np.empty([nSample, len(xVals), 4, 4], dtype=object)
    # First exand the cov matrix
    yGV = gv.gvar(gv.mean(GEVPData), (nSample - 1) * gv.evalcov(GEVPData))

    GEVPDataSamples = gv.sample(yGV, nbatch=nSample, mode='lbatch')
    dSGV = gv.dataset.avg_data(GEVPDataSamples)
    print('check GEVPData, dSGV', GEVPData['A1_A1'][0], dSGV['A1_A1'][0])
    # Take jackknifes!
    yJ1 = np.empty([nSample, len(xVals), 4, 4])
    yJErr = np.empty([len(xVals), 4, 4])
    # Mean
    yM = np.empty([len(xVals), 4, 4])
    # Values
    for ii in range(0, len(xVals)):
        for aa in range(0, 4):
            for bb in range(0, 4):
                lab = f'A{aa}_A{bb}'
                yJ1[:, ii, aa, bb] = FJ.complement(GEVPDataSamples[lab][:, ii])
                yM[ii, aa, bb] = FJ.mean(GEVPDataSamples[lab][:, ii])
                yJErr[ii, aa, bb] = FJ.jackErr(yJ1[:, ii, aa, bb])
    # Let's solve the GEVP on jackknifes
    left = np.empty([nSample, 4, 4])
    right = np.empty([nSample, 4, 4])
    left[:, :, :] = yJ1[:, t0 + dt, :, :]
    right[:, :, :] = yJ1[:, t0, :, :]
    wS = np.empty([nSample, 4])
    vrS = np.empty([nSample, 4, 4])
    vlS = np.empty([nSample, 4, 4])
    GProjSamples = np.empty([nSample, len(xVals), 4])
    for icon in range(0, nSample):
        wS[icon, :], vlS[icon, :, :], vrS[icon, :, :] = linalg.eig(left[icon, :, :],
                                                                   right[icon, :, :],
                                                                   left=True,
                                                                   right=True)
    # Solve it on the mean of the jackknifes
    wJM, vlJM, vrJM = linalg.eig(np.mean(left, axis=0),
                                 np.mean(right, axis=0),
                                 left=True,
                                 right=True)
    # Solve it on actual mean
    wM, vlM, vrM = linalg.eig(yM[t0 + dt, :, :], yM[t0, :, :], left=True, right=True)

    # project all at once
    conString = 'nia,ntij,nja->nta'
    contracted = np.einsum(conString, vlS, yJ1, vrS)
    #contracted = np.einsum('ia,ntij,ja->nta', vlM, yJ1, vrM)
    #contracted = np.einsum('ia,ntij,ja->nta', vl, yJ1, vr)
    # Now i will make it into a GV (to make plotting easier)
    yJGV = gv.dataset.avg_data(contracted, spread=True, median=False)
    yJGV_Covariance = gv.evalcov(yJGV)  # First get covariance matrix
    yJGV_Corrected = gv.gvar(gv.mean(yJGV), (nSample - 1) * yJGV_Covariance)
    fig, ax = plt.subplots(figsize=(16.6, 11.6))
    legendLabels = []
    for ii in range(0, 4):
        # Calculate effective mass for projected correlator
        effE = effE_forward(1.0, yJGV_Corrected[:, ii])
        ax.errorbar(xVals,
                    y=gv.mean(effE),
                    yerr=gv.sdev(effE),
                    label=f'GEVP {ii}',
                    marker='d',
                    linestyle='')
        # calculate effective mass for diagonal correlators
        effEiiii = effE_forward(1.0, dSGV[f'A{ii}_A{ii}'])
        ax.errorbar(xVals,
                    y=gv.mean(effEiiii),
                    yerr=gv.sdev(effEiiii),
                    label=f'A{ii}_A{ii}',
                    marker='d',
                    linestyle='')
        # Plot Truths
        ax.axhline(gv.mean(E[ii]), linestyle='--', color='gray')
        ax.axhspan(gv.mean(E[ii]) - gv.sdev(E[ii]),
                   gv.mean(E[ii]) + gv.sdev(E[ii]),
                   alpha=0.25,
                   color='gray',
                   linewidth=0)
        legendLabels.append(f'GEVP {ii}')
        legendLabels.append(f'A{ii}_A{ii}')
    # plot limits
    ax.set_ylim([0, 2])
    # Cut off just before end
    ax.set_xlim([0, xVals[-1] - 1])
    # labels
    ax.set_ylabel('$a_\\tau\\,E$')
    ax.set_xlabel('$\\tau/ a_\\tau$')
    # add a label to the truth lines
    truth_line = mpl.lines.Line2D([], [], color='gray', label='$\\text{Truth}$', ls='--')
    # Get the current legend
    legend = ax.legend()
    # Add the new line to the legend
    legend.legend_handles.append(truth_line)
    legendLabels.append('$\\text{Truth}$')
    # Update the legend
    ax.legend(handles=legend.legend_handles, labels=legendLabels, loc='best', ncol=2)
    # show
    plt.savefig('GEVP_Jack.pdf')
    plt.close()

    #############################################################################
    # Let's solve the GEVP on sampled GV
    t0 = 2
    dt = 3
    left = np.empty([4, 4], dtype=object)
    right = np.empty([4, 4], dtype=object)
    dSGVArray = np.empty([len(xVals), 4, 4], dtype=object)
    for ii in range(0, len(A)):
        for jj in range(0, len(A)):
            lab = f'A{ii}_A{jj}'
            left[ii, jj] = dSGV[lab][t0 + dt]
            right[ii, jj] = dSGV[lab][t0]
            dSGVArray[:, ii, jj] = dSGV[lab]
    # Can't use GV in linalg.eig!!
    left = gv.mean(left)
    right = gv.mean(right)
    w, vl, vr = linalg.eig(left, right, left=True, right=True)
    w = np.real(w)  # It's guaranteed real but for machine precision...
    print('w', w)
    print('vl', vl)
    print('vr', vr)

    # Do the projection correlated to plot to show the data isn't crazy
    GProj = np.empty([len(xVals), 4], dtype=object)
    # Use einsum to do multiplication
    conString = 'ia,tij,ja->ta'
    # opt_einsum required as it is 'objects' (gvars)
    contracted = opt_einsum.contract(conString, vl, dSGVArray, vr, backend='object')
    fig, ax = plt.subplots(figsize=(16.6, 11.6))
    legendLabels = []
    for ii in range(0, 4):
        GProj[:, ii] = contracted[..., ii]
        # Calculate effective mass for projected correlator
        effE = effE_forward(1.0, GProj[:, ii])
        ax.errorbar(xVals,
                    y=gv.mean(effE),
                    yerr=gv.sdev(effE),
                    label=f'GEVP {ii}',
                    marker='d',
                    linestyle='')
        # calculate effective mass for diagonal correlators
        effEiiii = effE_forward(1.0, dSGV[f'A{ii}_A{ii}'])
        ax.errorbar(xVals,
                    y=gv.mean(effEiiii),
                    yerr=gv.sdev(effEiiii),
                    label=f'A{ii}_A{ii}',
                    marker='d',
                    linestyle='')
        # Plot Truths
        ax.axhline(gv.mean(E[ii]), linestyle='--', color='gray')
        ax.axhspan(gv.mean(E[ii]) - gv.sdev(E[ii]),
                   gv.mean(E[ii]) + gv.sdev(E[ii]),
                   alpha=0.25,
                   color='gray',
                   linewidth=0)
        legendLabels.append(f'GEVP {ii}')
        legendLabels.append(f'A{ii}_A{ii}')
    # plot limits
    ax.set_ylim([0, 2])
    # Cut off just before end
    ax.set_xlim([0, xVals[-1] - 1])
    # labels
    ax.set_ylabel('$a_\\tau\\,E$')
    ax.set_xlabel('$\\tau/ a_\\tau$')
    # add a label to the truth lines
    truth_line = mpl.lines.Line2D([], [], color='gray', label='$\\text{Truth}$', ls='--')
    # Get the current legend
    legend = ax.legend()
    # Add the new line to the legend
    legend.legend_handles.append(truth_line)
    legendLabels.append('$\\text{Truth}$')
    # Update the legend
    ax.legend(handles=legend.legend_handles, labels=legendLabels, loc='best', ncol=2)
    # show
    plt.savefig('GEVP_JGVMean.pdf')
    plt.close()

    sys.exit()


if __name__ == '__main__':
    main()
