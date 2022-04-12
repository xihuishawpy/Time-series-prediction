#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @author: Longxing Tan, tanlongxing888@163.com
# @date: 2020-01
# paper:
# other implementations: https://github.com/philipperemy/keras-tcn
#                        https://github.com/locuslab/TCN
#                        https://github.com/emreaksan/stcn


import tensorflow as tf
from tensorflow.keras.layers import Dense, Conv1D, Dropout, Flatten
from ..layers.wavenet_layer import Dense3D, ConvTime


params = {
    'dilation_rates': [2 ** i for i in range(4)],
    'kernel_sizes': [2 for i in range(4)],
    'filters': 128,
    'dense_hidden_size': 64
}


class TCN(object):
    """ Temporal convolutional network
    """
    def __init__(self, custom_model_params={}):
        self.params = params
        self.conv_times = [
            ConvTime(
                filters=2 * self.params['filters'],
                kernel_size=kernel_size,
                causal=True,
                dilation_rate=dilation,
                activation='relu',
            )
            for dilation, kernel_size in zip(
                self.params['dilation_rates'], self.params['kernel_sizes']
            )
        ]

        self.dense_time1 = Dense3D(units=self.params['filters'], name='encoder_dense_time_1')
        self.dense_time2 = Dense3D(units=self.params['filters'] + self.params['filters'], name='encoder_dense_time_2')
        self.dense_time3 = Dense3D(units=1, name='encoder_dense_time_3')

    def __call__(self, inputs):
        x = self.dense_time1(inputs)
        for conv_time in self.conv_times:
            x = conv_time[x]

        x = self.dense_time2(x)
        x = self.dense_time3(x)
        return x
