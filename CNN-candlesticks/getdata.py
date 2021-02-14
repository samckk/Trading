import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import os
import sys
from mpl_finance import candlestick2_ochl, volume_overlay
import pandas as pd
from PIL import Image
import numpy as np
from os import listdir
from keras.utils import np_utils
import cv2


def getfilenames(directory, Training, symbol = False):
    list = []
    if symbol is not False:
        return individual_stock

    else:
        if Training is True:
            for i in listdir(directory):
                if '.TW_training' in i or '.tw_training' in i:
                    list.append(i)

        else:
            for i in listdir(directory):
                if '.TW_testing' in i or '.tw_testing' in i:
                    list.append(i)
        return sorted(list)


def getalllabels(list, seq_len):
    # Clean data
    labels = []
    for i in list:
        temp = pd.read_csv('stockdatas/' + i)
        temp.drop(['Adj Close'], axis=1, inplace=True)
        temp.drop(temp[temp['Volume'] == 0].index, inplace=True)
        temp.reset_index(drop=True, inplace=True)

        # Label data
        for i in range(int(seq_len), len(temp)-1):
            # Rise = 1, Drop = 0
            if temp.loc[i, 'Close'] < temp.loc[i+1, 'Close']:
                labels.append(1)
            else:
                labels.append(0)
    labels = np_utils.to_categorical(labels, 2)
    return labels

def minmaxlabels(list, seq_len):
    labels = []
    for i in list:
        temp = pd.read_csv('stockdatas/' + i)
        temp.drop(['Adj Close'], axis=1, inplace=True)
        temp.drop(temp[temp['Volume'] == 0].index, inplace=True)
        temp.reset_index(drop=True, inplace=True)

        # Label data
        for i in range(int(seq_len), len(temp)-21):
            df = temp[i:i+21]
            df.reset_index(inplace=True)
            labels.append(0)
            for data in range(20):
              # Rise = 1, Drop = 2, Not significant = 0
              if ((df.loc[0, 'Close'] - df.loc[data+1, 'Close'])/df.loc[0, 'Close']) < -0.1:
                  labels[-1] = 1
                  break
              elif ((df.loc[0, 'Close'] - df.loc[data+1, 'Close'])/df.loc[0, 'Close']) > 0.1:
                  labels[-1] = 2
                  break
    labels = np_utils.to_categorical(labels, 3)
    return labels


def getallcandlesticks(list, dimension, seq_len, use_volume, Training):
    plt.style.use('dark_background')
    path = "{}".format(os.getcwd())
        # print(path)

    if Training is True:
        if not os.path.exists(f'{path}/candlesticks'):
            os.makedirs(f'{path}/candlesticks')
    else:
        if not os.path.exists(f'{path}/candlesticks_testing'):
            os.makedirs(f'{path}/candlesticks_testing')

    counter = 0
    for file in list:
        df = pd.read_csv('stockdatas/' + file)
        df.drop(df[df['Volume'] == 0].index, inplace=True)
        df.reset_index(drop=True, inplace=True)


        for i in range(len(df)-int(seq_len)-21):
            # ohlc+volume
            c = df.iloc[i:i + int(seq_len), :]
            if True:
                my_dpi = 96
                fig = plt.figure(figsize=(dimension / my_dpi,
                                            dimension / my_dpi), dpi=my_dpi)
                ax1 = fig.add_subplot(1, 1, 1)
                candlestick2_ochl(ax1, c['Open'], c['Close'], c['High'],
                                    c['Low'], width=1,
                                    colorup='#77d879', colordown='#db3f3f')
                ax1.grid(False)
                ax1.set_xticklabels([])
                ax1.set_yticklabels([])
                ax1.xaxis.set_visible(False)
                ax1.yaxis.set_visible(False)
                ax1.axis('off')
                
                # create the second axis for the volume bar-plot
                # Add a seconds axis for the volume overlay
                if use_volume:
                    ax2 = ax1.twinx()
                    # Plot the volume overlay
                    bc = volume_overlay(ax2, c['Open'], c['Close'], c['Volume'],
                                        colorup='#77d879', colordown='#db3f3f', alpha=0.5, width=1)
                    ax2.add_collection(bc)
                    ax2.grid(False)
                    ax2.set_xticklabels([])
                    ax2.set_yticklabels([])
                    ax2.xaxis.set_visible(False)
                    ax2.yaxis.set_visible(False)
                    ax2.axis('off')

                if Training is True:    
                    pngfile = f'candlesticks/{counter}.png'
                else:
                    pngfile = f'candlesticks_testing/{counter}.png'
                fig.savefig(pngfile, pad_inches=0, transparent=False)
                plt.close(fig)
                plt.ioff()
                counter += 1
                print(counter)


def get_vectorized(Training):
    if Training is True:
        directory = 'candlesticks'
    else:
        directory = 'candlesticks_testing'
    path = "{}".format(os.getcwd())
    X = np.zeros(shape=(len(listdir(directory)),50,50,3), dtype = np.int8)
    for i in range(len(listdir(directory))):
        X[i] = cv2.imread(f'{path}/{directory}/{i}.png')
    return X
