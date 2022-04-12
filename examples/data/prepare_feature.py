# -*- coding: utf-8 -*-
# @author: Longxing Tan, tanlongxing888@163.com
# @date: 2020-01

import pandas as pd
import numpy as np


def transform2_lagged_feature(x, window_sizes):
    '''
    create historical lagged value as features
    :return:
    '''
    if isinstance(x, pd.Series):
        x = pd.DataFrame(x.values, index=range(len(x)), columns=["Feature"])
    inputs_lagged = pd.DataFrame()
    init_value = x.iloc[0]
    for window_size in range(1, window_sizes + 1):
        inputs_roll = np.roll(x, window_size, axis=0)
        inputs_roll[:window_size] = init_value
        inputs_roll = pd.DataFrame(
            inputs_roll,
            index=x.index,
            columns=[i + f'_lag{window_size}' for i in x.columns],
        )

        inputs_lagged = pd.concat([inputs_roll, inputs_lagged], axis=1)
    return inputs_lagged


def multi_step_y(y, predict_window, predict_gap=1):
    if isinstance(y, pd.DataFrame):
        y = y.values
    outputs = np.full((y.shape[0], predict_window), np.nan)
    y = y[:, 0]
    for i in range(predict_window):
        outputs_column = np.roll(y, -(i+predict_gap-1)).astype(np.float)
        if i + predict_gap != 1:
            outputs_column[-(i+predict_gap-1):] = np.nan
        outputs[:, i] = outputs_column
    return outputs


def simple_moving_average(x):
    pass
