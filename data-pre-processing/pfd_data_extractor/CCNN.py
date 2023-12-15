import os
import glob
import random
import numpy as np
np.random.seed(666)
import pandas as pd
from scipy.interpolate import RectBivariateSpline as interp2d
from scipy import ndimage, array, ogrid, mgrid
import sys
sys.path.append('/data1/mpsurnis/soft/presto/python/presto')
import psr_utils
import sys
sys.path.append('/data1/mpsurnis/soft/presto/python/presto')
from prepfold import pfd


def downsample(a, n, align=0):
    '''
    Reference: https://github.com/zhuww/ubc_AI/blob/master/samples.py

    a: input array of 1-3 dimentions
    n: downsample to n bins
    optional:
    align : if non-zero, downsample grid (coords) 
        will have a bin at same location as 'align'
        ( typically max(sum profile) )
        useful for plots vs. phase
         
    '''
    if type(a) in [list]:
        result = []
        for b in a:
            result.append(downsample(b))
        return result
    else:
        shape = a.shape
        D = len(shape)
        if D == 1:
            coords = mgrid[0:1-1./n:1j*n]
        elif D == 2:
            d1,d2 = shape
            n1, n2 = n
            if align: 
                #original phase bins
                x2 = mgrid[0:1.-1./d2:1j*d2]
                #downsampled phase bins
                crd = mgrid[0:1-1./n2:1j*n2]
                crd += x2[align]
                crd = (crd % 1)
                crd.sort()
                offset = crd[0]*d2
                coords = mgrid[0:d1-1:1j*n1, offset:d2-float(d2)/n2+offset:1j*n2]
            else:
                coords = mgrid[0:d1-1:1j*n1, 0:d2-1:1j*n2]
        elif D == 3:
            d1,d2,d3 = shape
            coords = mgrid[0:d1-1:1j*n, 0:d2-1:1j*n, 0:d3-1:1j*n]
        else:
            raise "too many dimentions %s " % D
        def map_to_index(x,bounds,N):
            xmin, xmax= bounds
            return (x - xmin)/(xmax-xmin)*N
        if D == 1:
            m = len(a)
            x = mgrid[0:1-1./m:1j*m]
            if align:
                #ensure new grid lands on max(a)
                coords += x[align]
                coords = coords % 1
                coords.sort()
            #newf = interp(x, a, bounds_error=True)
            #return newf(coords)
            return np.interp(coords, x, a)
        elif D == 2:

            newf = ndimage.map_coordinates(a, coords, cval=np.median(a))
            return newf
        else:
            newf = ndimage.map_coordinates(coeffs, coords, prefilter=False)
            return newf



def resize(a, M, align=0):
    '''
    The function to resize the data. 
    1. If the size of the data is larger than the standard size, we do not downsample the data 
    directly, but insert the zero elements to the data in order to make the size of the data 
    can be divisible by the standard size, and then scrunch it.

    2. If the size of the data is less than the standard size, use the downsample(interpolate)

    a: input array of 1-3 dimentions
    M: resize to n bins
    optional:
    align : if non-zero, downsample grid (coords) 
        will have a bin at same location as 'align'
        ( typically max(sum profile) )
        useful for plots vs. phase
         
    '''

    m, n = a.shape
    if n < M:
        a = downsample(a, [m, M], align)
    elif n % M != 0:
        add_num_per = int(n / M)
        full_num = (add_num_per+1) * M
        rest_num = full_num - n
        add_index = int(rest_num / add_num_per)
        count_mat = np.ones(a.shape)

        if rest_num % add_num_per != 0:
            a = np.insert(a, add_index, np.zeros((rest_num % add_num_per, m)), axis=1)
            count_mat = np.insert(count_mat, add_index, np.zeros((rest_num % add_num_per, m)), axis=1)

        for i in range(add_index-1,-1,-1):
            a = np.insert(a, i, np.zeros((add_num_per, m)), axis=1)
            count_mat = np.insert(count_mat, i, np.zeros((add_num_per, m)), axis=1)

        a = a.T.reshape(M, add_num_per+1, m).sum(axis=1).T
        count_mat = count_mat.T.reshape(M, add_num_per+1, m).sum(axis=1).T
        a = a / count_mat
    elif M < n:
        add_num_per = int(n / M) 
        a = a.T.reshape(M, add_num_per, m).mean(axis=1).T
    else:
        pass



    if m < M:
        a = downsample(a, [M, M], align)


    elif m % M != 0:
        add_num_per = int(m / M)
        full_num = (add_num_per+1) * M
        rest_num = full_num - m
        add_index = int(rest_num / add_num_per)
        count_mat = np.ones(a.shape)

        if rest_num % add_num_per != 0:
            a = np.insert(a, add_index, np.zeros((rest_num % add_num_per, M)), axis=0)
            count_mat = np.insert(count_mat, add_index, np.zeros((rest_num % add_num_per, M)), axis=0)

        for i in range(add_index-1,-1,-1):
            a = np.insert(a, i, np.zeros((add_num_per, M)), axis=0)
            count_mat = np.insert(count_mat, i, np.zeros((add_num_per, M)), axis=0)

        a = a.reshape(M, add_num_per+1, M).sum(axis=1)
        count_mat = count_mat.reshape(M, add_num_per+1, M).sum(axis=1)
        a = a / count_mat
    elif M < m:
        add_num_per = int(m / M)
        a = a.reshape(M, add_num_per, M).mean(axis=1)
    else:
        pass
    
        
    return a




class pfddata(pfd):
    '''
    Reference: https://github.com/zhuww/ubc_AI/blob/master/samples.py
    '''
    initialized = False
    def __init__(self, filename, centre=True):
        
        if not filename == 'self':
            pfd.__init__(self, filename)
            
        self.dedisperse()
        self.adjust_period()
        self.threshold = 0.015
        self.miss_subbands_threshold = 0.8
        self.miss_time_vs_phase_threshold = 0.5
        
        if not 'input_feature' in self.__dict__:
            self.input_feature = {}
            
        self.input_feature.update({"attribute:[period]": np.array([self.topo_p1])})
        if centre:
            max_index = self.profs.sum(0).sum(0).argmax()
            nbin = self.proflen
            noff = int(nbin / 2 - max_index)
            self.profs = np.roll(self.profs, noff, axis=-1)
            

        self.align = self.profs.sum(0).sum(0).argmax()
        if self.align >= 64:
            self.align=0
        
        self.initialized = True
        
        
        
    def getdata(self, sumprof_bins=64, subbands_bins=64, time_vs_phase_bins=64, DM_bins=200, drop_zero=True):
        '''
        drop_zero: if True: 
            if the rows in subbands and time_vs_phase_bin are very close zero relative to others, 
            they will be dropped
        '''
        if not 'input_feature' in self.__dict__:
            self.input_feature = {}
            
        if not self.initialized:
            print('pfd not initialized.')
            self.__init__('self')
            
        def greyscale(array2d):
            """
            greyscale(array2d, **kwargs):
                Plot a 2D array as a greyscale image using the same scalings
                    as in prepfold.
            """
            # Use the same scaling as in prepfold_plot.c
            global_max = array2d.max()
            min_parts = np.minimum.reduce(array2d, 1)
            array2d = (array2d - min_parts[:,np.newaxis]) / (np.fabs(global_max) - np.fabs(min_parts.max()))
            return array2d
        
        def sumprof_curve(M):
            if (M is not None) and (len(self.sumprof) != M):
                sumprof = downsample(self.sumprof, M, self.align)
            else:
                sumprof = self.sumprof
                
            normprof = sumprof - min(sumprof)
            if np.max(normprof) == 0:
                sumprof = normprof
            else:
                sumprof = normprof / max(normprof)
            return sumprof
        
        def subbands_fig(M):
            profs = self.profs.sum(0)
            subbands = greyscale(profs)
            
            if drop_zero:
                norm_subbands = subbands / subbands.max()
                sed = norm_subbands.mean(axis=1)
                valid_index = np.where(sed > self.threshold)[0]
                missed_ratio_subbands = 1. - len(valid_index) * 1.0 / len(sed)
                if missed_ratio_subbands < self.miss_subbands_threshold:
                    subbands = subbands[valid_index]
                else:
                    missed_ratio_subbands = 0.
            # resize the data
            if (M is not None) and (subbands.shape[0] != M or subbands.shape[1] != M):
                subbands = resize(subbands, M, self.align)

            subbands = greyscale(subbands)
            
            return subbands

        def time_vs_phase_fig(M):
            # time vs phase
            profs = self.profs.sum(1)
            time_vs_phase = greyscale(profs)
            #if drop_zero:
             #   norm_time_vs_phase = time_vs_phase / time_vs_phase.max()
              #  reduced_chi2 = norm_time_vs_phase.mean(axis=1)
               # valid_index = np.where(reduced_chi2 > self.threshold)[0]
                #missed_ratio_time_vs_phase = 1. - len(valid_index) * 1.0 / len(reduced_chi2)
                #if missed_ratio_time_vs_phase < self.miss_time_vs_phase_threshold:
                #    time_vs_phase = time_vs_phase[valid_index]
                #else:
                 #   missed_ratio_time_vs_phase = 0.
            #if (M is not None) and (time_vs_phase.shape[0] != M or time_vs_phase.shape[1] != M):
             #   time_vs_phase = resize(time_vs_phase, M, self.align)

            time_vs_phase = greyscale(time_vs_phase)
            
            return time_vs_phase
            
        def DM_curve(M):
            ddm = (self.dms.max() - self.dms.min())/2.
            loDM, hiDM = (self.bestdm - ddm , self.bestdm + ddm)
            loDM = max((0, loDM)) #make sure cut off at 0 DM
            hiDM = max((ddm, hiDM)) #make sure cut off at 0 DM
            N = 200
            interp = False
            sumprofs = self.profs.sum(0)
            if not interp:
                profs = sumprofs
            else:
                profs = np.zeros(np.shape(sumprofs), dtype='d')
            DMs = psr_utils.span(loDM, hiDM, N)
            chis = np.zeros(N, dtype='f')
            subdelays_bins = self.subdelays_bins.copy()
            for ii, DM in enumerate(DMs):
                subdelays = psr_utils.delay_from_DM(DM, self.barysubfreqs)
                hifreqdelay = subdelays[-1]
                subdelays = subdelays - hifreqdelay
                delaybins = subdelays*self.binspersec - subdelays_bins
                if interp:
                    interp_factor = 16
                    for jj in range(p.nsub):
                        profs[jj] = psr_utils.interp_rotate(sumprofs[jj], delaybins[jj],
                                                            zoomfact=interp_factor)
                    # Note: Since the interpolation process slightly changes the values of the
                    # profs, we need to re-calculate the average profile value
                    avgprof = (profs/self.proflen).sum()
                else:
                    new_subdelays_bins = np.floor(delaybins+0.5)
                    for jj in range(self.nsub):
                        #profs[jj] = psr_utils.rotate(profs[jj], new_subdelays_bins[jj])
                        delay_bins = int(new_subdelays_bins[jj] % len(profs[jj]))
                        if not delay_bins==0:
                            profs[jj] = np.concatenate((profs[jj][delay_bins:], profs[jj][:delay_bins]))

                    subdelays_bins += new_subdelays_bins
                    avgprof = self.avgprof
                sumprof = profs.sum(0)
                chis[ii] = self.calc_redchi2(prof=sumprof, avg=avgprof)
            if len(chis) != M:
                chis = downsample(chis, M)
            
            chis = chis - np.min(chis)
            max_chis = np.max(chis) 
            if max_chis != 0:
                chis = chis / max_chis
            
            return chis
            
            
        data = {'sumprof':sumprof_curve(sumprof_bins), 
                'subbands':subbands_fig(subbands_bins), 
                'time_vs_phase':time_vs_phase_fig(time_vs_phase_bins), 
                'DM':DM_curve(DM_bins)}
        
        return data





def load_pfd(f):
    p = pfddata(f)
    return p.getdata()

load_pfd('psb_DM52.50_ACCEL_200:2_10.06ms_Cand.pfd')

