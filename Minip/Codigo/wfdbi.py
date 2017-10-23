import wfdb
import numpy as np
import matplotlib.pyplot as plt
from wfdb.readwrite import records
from wfdb.readwrite import _headers
from wfdb.readwrite import _signals
from wfdb.readwrite import annotations
import savefig as sf




def plotrec(record=None, title = None, annotation = None, timeunits='samples',
    sigstyle='', annstyle='r*', figsize=None, returnfig = False, ecggrids=[]):


    # Check the validity of items used to make the plot
    # Return the x axis time values to plot for the record (and annotation if any)
    t, tann, annplot = checkplotitems(record, title, annotation, timeunits, sigstyle, annstyle)

    siglen, nsig = record.p_signals.shape

    # Expand list styles
    if isinstance(sigstyle, str):
        sigstyle = [sigstyle]*record.nsig
    else:
        if len(sigstyle) < record.nsig:
            sigstyle = sigstyle+['']*(record.nsig-len(sigstyle))
    if isinstance(annstyle, str):
        annstyle = [annstyle]*record.nsig
    else:
        if len(annstyle) < record.nsig:
            annstyle = annstyle+['r*']*(record.nsig-len(annstyle))

    # Expand ecg grid channels
    if ecggrids == 'all':
        ecggrids = range(0, record.nsig)

    # Create the plot
    fig=plt.figure(figsize=figsize)

    for ch in range(nsig):
        # Plot signal channel
        ax = fig.add_subplot(nsig, 1, ch+1)
        ax.plot(t, record.p_signals[:,ch], sigstyle[ch], zorder=3, color="black")

        if (title is not None) and (ch==0):
            plt.title(title)

        # Plot annotation if specified
        if annplot[ch] is not None:
            ax.plot(tann[ch], record.p_signals[annplot[ch], ch], annstyle[ch])

        # Axis Labels
        if timeunits == 'samples':
            plt.xlabel('index/sample')
        else:
            plt.xlabel('time/'+timeunits[:-1])


        if record.signame[ch] is not None:
            chanlabel=record.signame[ch]
        else:
            chanlabel='channel'
        if record.units[ch] is not None:
            unitlabel=record.units[ch]
        else:
            unitlabel='NU'
        plt.ylabel(chanlabel+"/"+unitlabel)

        # Show standard ecg grids if specified.
        if ch in ecggrids:

            auto_xlims = ax.get_xlim()
            auto_ylims= ax.get_ylim()

            major_ticks_x, minor_ticks_x, major_ticks_y, minor_ticks_y = calc_ecg_grids(
                auto_ylims[0], auto_ylims[1], record.units[ch], record.fs, auto_xlims[1], timeunits)

            min_x, max_x = np.min(minor_ticks_x), np.max(minor_ticks_x)
            min_y, max_y = np.min(minor_ticks_y), np.max(minor_ticks_y)

            for tick in minor_ticks_x:
                ax.plot([tick, tick], [min_y,  max_y], c='#ff0000', marker='|', zorder=1)
            for tick in major_ticks_x:
                ax.plot([tick, tick], [min_y, max_y], c='#ff0000', marker='|', zorder=2)
            for tick in minor_ticks_y:
                ax.plot([min_x, max_x], [tick, tick], c='#ff0000', marker='_', zorder=1)
            for tick in major_ticks_y:
                ax.plot([min_x, max_x], [tick, tick], c='#ff0000', marker='_', zorder=2)

            # Plotting the lines changes the graph. Set the limits back
            ax.set_xlim(auto_xlims)
            ax.set_ylim(auto_ylims)

    #plt.show(fig)
    fig.savefig("/home/manuel/Documents/Minip/fullimgs/"+title+".png")

    # Return the figure if requested
    if returnfig:
        return fig


def calc_ecg_grids(minsig, maxsig, units, fs, maxt, timeunits):

    # 5mm 0.2s major grids, 0.04s minor grids
    # 0.5mV major grids, 0.125 minor grids
    # 10 mm is equal to 1mV in voltage.

    # Get the grid interval of the x axis
    if timeunits == 'samples':
        majorx = 0.2*fs
        minorx = 0.04*fs
    elif timeunits == 'seconds':
        majorx = 0.2
        minorx = 0.04
    elif timeunits == 'minutes':
        majorx = 0.2/60
        minorx = 0.04/60
    elif timeunits == 'hours':
        majorx = 0.2/3600
        minorx = 0.04/3600

    # Get the grid interval of the y axis
    if units.lower()=='uv':
        majory = 500
        minory = 125
    elif units.lower()=='mv':
        majory = 0.5
        minory = 0.125
    elif units.lower()=='v':
        majory = 0.0005
        minory = 0.000125
    else:
        raise ValueError('Signal units must be uV, mV, or V to plot the ECG grid.')


    major_ticks_x = np.arange(0, _signals.upround(maxt, majorx)+0.0001, majorx)
    minor_ticks_x = np.arange(0, _signals.upround(maxt, majorx)+0.0001, minorx)

    major_ticks_y = np.arange(_signals.downround(minsig, majory), _signals.upround(maxsig, majory)+0.0001, majory)
    minor_ticks_y = np.arange(_signals.downround(minsig, majory), _signals.upround(maxsig, majory)+0.0001, minory)

    return (major_ticks_x, minor_ticks_x, major_ticks_y, minor_ticks_y)



def checkplotitems(record, title, annotation, timeunits, sigstyle, annstyle):

    # signals
    if not isinstance(record, records.Record):
        raise TypeError("The 'record' argument must be a valid wfdb.Record object")
    if not isinstance(record.p_signals, np.ndarray) or record.p_signals.ndim != 2:
        raise TypeError("The plotted signal 'record.p_signals' must be a 2d numpy array")

    siglen, nsig = record.p_signals.shape

    # fs and timeunits
    allowedtimes = ['samples', 'seconds', 'minutes', 'hours']
    if timeunits not in allowedtimes:
        raise ValueError("The 'timeunits' field must be one of the following: ", allowedtimes)
    # Get x axis values. fs must be valid when plotting time
    if timeunits == 'samples':
        t = np.linspace(0, siglen-1, siglen)
    else:
        if not isinstance(record.fs, _headers.floattypes):
            raise TypeError("The 'fs' field must be a number")

        if timeunits == 'seconds':
            t = np.linspace(0, siglen-1, siglen)/record.fs
        elif timeunits == 'minutes':
            t = np.linspace(0, siglen-1, siglen)/record.fs/60
        else:
            t = np.linspace(0, siglen-1, siglen)/record.fs/3600

    # units
    if record.units is None:
        record.units = ['NU']*nsig
    else:
        if not isinstance(record.units, list) or len(record.units)!= nsig:
            raise ValueError("The 'units' parameter must be a list of strings with length equal to the number of signal channels")
        for ch in range(nsig):
            if record.units[ch] is None:
                record.units[ch] = 'NU'

    # signame
    if record.signame is None:
        record.signame = ['ch'+str(ch) for ch in range(1, nsig+1)]
    else:
        if not isinstance(record.signame, list) or len(record.signame)!= nsig:
            raise ValueError("The 'signame' parameter must be a list of strings, with length equal to the number of signal channels")

    # title
    if title is not None and not isinstance(title, str):
        raise TypeError("The 'title' field must be a string")

    # signal line style
    if isinstance(sigstyle, str):
        pass
    elif isinstance(sigstyle, list):
        if len(sigstyle) > record.nsig:
            raise ValueError("The 'sigstyle' list cannot have more elements than the number of record channels")
    else:
        raise TypeError("The 'sigstyle' field must be a string or a list of strings")

    # annotation plot style
    if isinstance(annstyle, str):
        pass
    elif isinstance(annstyle, list):
        if len(annstyle) > record.nsig:
            raise ValueError("The 'annstyle' list cannot have more elements than the number of record channels")
    else:
        raise TypeError("The 'annstyle' field must be a string or a list of strings")


    # Annotations if any
    if annotation is not None:

        # The output list of numpy arrays (or Nones) to plot
        annplot = [None]*record.nsig

        # Move single channel annotations to channel 0
        if isinstance(annotation, annotations.Annotation):
            annplot[0] = annotation.sample
        elif isinstance(annotation, np.ndarray):
            annplot[0] = annotation
        # Ready list.
        elif isinstance(annotation, list):
            if len(annotation) > record.nsig:
                raise ValueError("The number of annotation series to plot cannot be more than the number of channels")
            if len(annotation) < record.nsig:
                annotation = annotation+[None]*(record.nsig-len(annotation))
            # Check elements. Copy over to new list.
            for ch in range(record.nsig):
                if isinstance(annotation[ch], annotations.Annotation):
                    annplot[ch] = annotation[ch].sample
                elif isinstance(annotation[ch], np.ndarray):
                    annplot[ch] = annotation[ch]
                elif annotation[ch] is None:
                    pass
                else:
                    raise TypeError("The 'annotation' argument must be a wfdb.Annotation object, a numpy array, None, or a list of these data types")
        else:
            raise TypeError("The 'annotation' argument must be a wfdb.Annotation object, a numpy array, None, or a list of these data types")

        # The annotation locations to plot
        tann = [None]*record.nsig

        for ch in range(record.nsig):
            if annplot[ch] is None:
                continue
            if timeunits == 'samples':
                tann[ch] = annplot[ch]
            elif timeunits == 'seconds':
                tann[ch] = annplot[ch]/record.fs
            elif timeunits == 'minutes':
                tann[ch] = annplot[ch]/record.fs/60
            else:
                tann[ch] = annplot[ch]/record.fs/3600
    else:
        tann = None
        annplot = [None]*record.nsig

    # tann is the sample values to plot for each annotation series
    return (t, tann, annplot)
