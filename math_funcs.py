import numpy as np


def coeff_fn(x1, y1, x2, y2):
    """
    Takes two points (__x1,y1) and (x2,y2) in 2D and returns the slope and intercept
    :return: (slope, intercept)
    """
    _m = (y2-y1)/(x2-x1)
    _q = y1 - _m*x1
    return _m, _q


def fill_nan(df_in, col):
    """
    Fills NaN values in 'col' using linear extrapolation
    :param df_in: Pandas DataFrame for HTSD data
    :param col: column for which to fill NaN values
    :return: None -> Performs 'imputation' inplace
    """
    for i in range(df_in.shape[0]):
        # CHECK IF NaN VALUE
        if np.isnan(df_in.loc[i, col]):
            # COMPUTE SLOPE _m AND INTERCEPT _q USING THE LAST 2 VALID VALUES
            x1, y1 = df_in.loc[i-2, 'mass [%]'], df_in.loc[i-2, col]
            x2, y2 = df_in.loc[i-1, 'mass [%]'], df_in.loc[i-1, col]
            _m, _q = coeff_fn(x1, y1, x2, y2)

            # REPLACE NaN WITH EXTRAPOLATED VALUES
            df_in.loc[i, col] = _m * df_in.loc[i, 'mass [%]'] + _q


def lin_interpolation(xx, yy, valx):
    """
    Takes the discrete sampled values of a function as (xx, yy)
    and performa a linear interpolation/extrapolation at valx
    :param xx: numpy.array -> Sampled values of the independent variable
    :param yy: numpy.array -> Sampled values of the target variable
    :param valx: float -> value of the independent variable at which to perform interpolation
    :return: float -> Result of the interpolation/extrapolation at valx
    """

    # If valx already in xx => return the corresponding yy
    if valx in xx:
        result = yy[xx == valx]

    else:
        __x1 = __x2 = __y1 = __y2 = 0
        # If valT is below the minimum or above the maximum values of 'T_recent [C]' => Extrapolate
        if valx < xx[0]:
            __x1, __y1 = xx[0], yy[0]
            __x2, __y2 = xx[1], yy[1]
        elif valx > xx[-1]:
            __x1, __y1 = xx[-2], yy[-2]
            __x2, __y2 = xx[-1], yy[-1]
        # Otherwise interpolate
        else:
            for __i in range(len(xx) - 1):
                if (valx > xx[__i]) and (valx < xx[__i + 1]):
                    __x1, __y1 = xx[__i], yy[__i]
                    __x2, __y2 = xx[__i + 1], yy[__i + 1]
                    break
        __m, __q = coeff_fn(__x1, __y1, __x2, __y2)
        result = __m * valx + __q
    return result
