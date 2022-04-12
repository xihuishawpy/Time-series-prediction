# -*- coding: utf-8 -*-
# @author: Longxing Tan, tanlongxing888@163.com
# @date: 2020-03

import tensorflow as tf
from tensorflow.keras.layers import Conv1D, BatchNormalization, Activation, Dense, GlobalAveragePooling1D, Add, Multiply


class ConvbrLayer(tf.keras.layers.Layer):
    def __init__(self, units, kernel_size, strides, dilation):
        super(ConvbrLayer, self).__init__()
        self.units = units
        self.kernel_size = kernel_size
        self.strides = strides
        self.dilation = dilation

    def build(self, input_shape):
        self.conv1 = Conv1D(self.units,
                            kernel_size=self.kernel_size,
                            strides=self.strides,
                            dilation_rate=self.dilation,
                            padding="same")
        self.bn = BatchNormalization()
        self.relu = Activation('relu')
        super(ConvbrLayer, self).build(input_shape)

    def call(self, x):
        x = self.conv1(x)
        x = self.bn(x)
        x = self.relu(x)
        return x


class SeBlock(tf.keras.layers.Layer):
    '''
    Squeeze-and-Excitation Networks
    '''
    def __init__(self, units):
        super(SeBlock, self).__init__()
        self.units = units

    def build(self, input_shape):
        self.pool = GlobalAveragePooling1D()
        self.fc1 = Dense(self.units//8, activation="relu")
        self.fc2 = Dense(self.units, activation="sigmoid")
        super(SeBlock, self).build(input_shape)

    def call(self, x):
        input = x
        x = self.pool(x)
        x = self.fc1(x)
        x = self.fc2(x)
        return Multiply()([input, x])


class ReBlock(tf.keras.layers.Layer):
    def __init__(self, units, kernel_size, strides, dilation, use_se):
        super(ReBlock, self).__init__()
        self.units = units
        self.kernel_size = kernel_size
        self.strides = strides
        self.dilation = dilation
        self.conv_br1 = ConvbrLayer(units, kernel_size, strides, dilation)
        self.conv_br2 = ConvbrLayer(units, kernel_size, strides, dilation)
        if use_se:
            self.se_block = SeBlock(units=units)
        self.use_se = use_se

    def build(self, input_shape):
        super(ReBlock, self).build(input_shape)

    def call(self, x):
        x_re = self.conv_br1(x)
        x_re = self.conv_br2(x_re)
        if self.use_se:
            x_re = self.se_block(x_re)
            x_re = Add()([x, x_re])
        return x_re


def conv_br(x, units, kernel_size, strides, dilation):
    # a function is easier to reuse
    convbr = ConvbrLayer(units=units,
                         kernel_size=kernel_size,
                         strides=strides,
                         dilation=dilation)
    return convbr(x)


def se_block(x, units):
    seblock = SeBlock(units)
    return seblock(x)


def re_block(x, units, kernel_size, strides, dilation, use_se=True):
    reblock = ReBlock(units, kernel_size, strides, dilation, use_se=use_se)
    return reblock(x)
