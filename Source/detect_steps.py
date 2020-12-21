# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 15:41:03 2020

@author: arsii
"""


def detect_steps(timeseries,
                 title,
                 xlabel,
                 savepath = False,
                 savename = False,
                 ):
    
    """
    Detect steps from the time series and plot the figure.
    Optionally saves the figure.

    Parameters
    ----------
    timeseries : Pandas series
            time series for step detection
    title : str
            Figure title.
    xlabel : str
            Figure xlabel.
    savename : str, optional
            Figure savename. The default is False.
    savepath : Path object, optional
            Figure save folder. The default is False.

    Returns
    -------
    None.

    """
    # signal
    sig = timeseries.values.reshape(-1,1)
    
    # window / kernel
    '''
    win = signal.gaussian(51,std=5).reshape(-1,1)
    win = np.gradient(win,axis=0)
    win = win - win.mean()
    win = win / win.max()
    '''
    # stepfunction
    win = -(np.array([0]*24+[1]*24).reshape(-1,1))
    
    
    # convolution
    filtered = signal.convolve(sig, win, mode='same') / sum(win)
    
    # find peaks / low points 
    peaks, properties = find_peaks(filtered.reshape(-1), height=0)
    bottoms, properties_b = find_peaks(-filtered.reshape(-1),height=0)
    heights = properties['peak_heights']
    lows = properties_b['peak_heights']
    
    # find top / low indices and values
    top_indices = heights.argsort()[-5:][::-1]
    top_peaks = peaks[top_indices]
    neg_indices = (lows).argsort()[-5:][::-1]
    neg_peaks = bottoms[neg_indices]

    # plot
    fig, (ax_orig, ax_win, ax_filt) = plt.subplots(3, 1, sharex=True,figsize=(20,10))
    plt.suptitle(title, y=1.05,fontsize=20)
    ax_orig.plot(sig)    
    ax_orig.set_ylabel('Original value')
    ax_orig.set_title('Original timeseries')
    ax_orig.margins(0, 0.1)
    ax_win.plot(win)
    ax_win.set_title('Kernel / filter')    
    ax_win.set_ylabel('Filter level')
    ax_win.margins(0, 0.1)
    ax_filt.plot(filtered)
    ax_filt.set_ylim(30,90)
    ax_filt.plot(neg_peaks, filtered[neg_peaks], "x", markersize=15, color="blue")    
    ax_filt.plot(top_peaks, filtered[top_peaks], "x", markersize=15, color="red")    
    ax_filt.set_title('Filtered timeseries')    
    ax_filt.set_ylabel('Filtered level')
    ax_filt.set_xlabel(xlabel)    
    ax_filt.margins(0, 0.1)
    fig.tight_layout()
    
    if not all((savename,savepath)):
        plt.show()
      
    elif all((savename,savepath)):
       
        assert isinstance(savename,str), "Invalid savename type."
        
        if savepath.exists():
            with open(savepath / (savename + "_filtered_peaks" + ".png"), mode="wb") as outfile:
                plt.savefig(outfile, format="png")
        else:
            raise Exception("Requested folder: " + str(savepath) + " does not exist.")
    else:
        raise Exception("Arguments were not given correctly.")
    
    return peaks, bottoms, top_indices, neg_indices

def plot_histogram(Result,
                   title,
                   savepath = False,
                   savename = False,
                   ylabel = "Battery Level (%)",
                   xlabel  = "Date",
                   dates = False,
                   ):
    """
    

    Parameters
    ----------
    Result : TYPE
        DESCRIPTION.
    title : TYPE
        DESCRIPTION.
    savepath : TYPE, optional
        DESCRIPTION. The default is False.
    savename : TYPE, optional
        DESCRIPTION. The default is False.
    ylabel : TYPE, optional
        DESCRIPTION. The default is "Battery Level (%)".
    xlabel : TYPE, optional
        DESCRIPTION. The default is "Date".
    dates : TYPE, optional
        DESCRIPTION. The default is False.
     : TYPE
        DESCRIPTION.

    Raises
    ------
    Exception
        DESCRIPTION.

    Returns
    -------
    None.

    """
        
    fig2 = plt.figure(figsize=(20,15))
    
    plt.suptitle(title +" / histograms",fontsize=20)
    
    plt.subplot(2,2,1)
    plt.hist(Result.observed)
    plt.title('Observations',fontsize=16)
    plt.xlabel("Battery Level (%)")
    plt.ylabel("Count")
                
    plt.subplot(2,2,2)
    plt.hist(Result.trend)
    plt.title('Trend',fontsize=16)
    plt.xlabel("Battery Level (%)")
    plt.ylabel("Count")
    
    plt.subplot(2,2,3)
    plt.hist(Result.seasonal)
    plt.title('Seasonal',fontsize=16)
    plt.xlabel("Battery Level (%)")
    plt.ylabel("Count")
     
    plt.subplot(2,2,4)
    plt.hist(Result.resid)
    plt.title('Residuals',fontsize=16)
    plt.xlabel("Battery Level (%)")
    plt.ylabel("Count")
     
    fig2.tight_layout(pad=4.0)
    
    if not all((savename,savepath)):
        plt.show()
      
    elif all((savename,savepath)):
        
        assert isinstance(savename,str), "Invalid savename type."
        
        if savepath.exists():
            with open(savepath / (savename + "_hist" + ".png"), mode="wb") as outfile:
                plt.savefig(outfile, format="png")
        else:
            raise Exception("Requested folder: " + str(savepath) + " does not exist.")
    else:
        raise Exception("Arguments were not given correctly.")