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
