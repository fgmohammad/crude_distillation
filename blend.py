import pandas as pd
from math_funcs import *
from scipy.interpolate import InterpolatedUnivariateSpline


class Blend:
    def __init__(self, name_a, name_b, frac_a, fname):
        """
        Crude blend object from blending crude_a with volume fraction of frac_a
        and crude_b with volume fraction of (1-frac_a)
        :param name_a: str -> Name of crude_a
        :param name_b: str -> Name of crude_b
        :param frac_a: float -> fraction of crude_a
        :param fname: str -> path to th file with crude names and abbreviations
        """
        self.name_a = name_a
        self.name_b = name_b
        self.frac_a = frac_a
        self.fname = fname

        # Get distillation profile for the blend
        self.htsd_blend = self.get_dist_profile()

    def get_htsd_data(self, name):
        """
        Takes the name of a crude and returns HTSD data in a Pandas DataFrame
        :param name: str -> Name of the crude
        :return: Pandas DataFrame containing HTSD data
        """
        __abbr = self.get_abbr(name=name)
        __fname_csv = f'data/htsd_{name.replace(" ", "_")}_{__abbr}.csv'
        return pd.read_csv(__fname_csv).drop('Unnamed: 0', axis=1)

    def get_abbr(self, name):
        """
        Takes the name of the crude and reads its abbreviation from self.fname
        :param name: str -> crude name
        :return: str -> crude abbr
        """
        crudes = pd.read_csv(self.fname).drop('Unnamed: 0', axis=1)
        return crudes[crudes['name'].str.startswith(name)].abbr.values[0]

    def get_dist_profile(self):
        # Get the HTSD for the two crudes
        __htsd_a = self.get_htsd_data(self.name_a)
        __htsd_b = self.get_htsd_data(self.name_b)

        # Fill missing values in col='T_recent [C]'
        __col = 'T_recent [C]'
        fill_nan(df_in=__htsd_a, col=__col)
        fill_nan(df_in=__htsd_b, col=__col)

        # Set the Temperature values
        __Tmin = min(__htsd_a['T_recent [C]'].min(), __htsd_b['T_recent [C]'].min())
        __Tmax = max(__htsd_a['T_recent [C]'].max(), __htsd_b['T_recent [C]'].max())
        __vT = np.linspace(__Tmin, __Tmax, 1000)

        # Define interpolation functions
        s_a = InterpolatedUnivariateSpline(__htsd_a['T_recent [C]'].values, __htsd_a['mass [%]'].values, k=1)
        s_b = InterpolatedUnivariateSpline(__htsd_b['T_recent [C]'].values, __htsd_b['mass [%]'].values, k=1)

        # Fraction of crude_a evaporated at temperature __T
        __evap_a = s_a(__vT)
        # Constraints on the evaporated fraction
        __evap_a[__evap_a < 0.] = 0.
        __evap_a[__evap_a > 100.] = 100.

        # Fraction of crude_a evaporated at temperature __T
        __evap_b = s_b(__vT)
        # Constraints on the evaporated fraction
        __evap_b[__evap_b < 0.] = 0.
        __evap_b[__evap_b > 100.] = 100.

        # Fraction of the blend evaporated at temperature __T
        __evap = __evap_a * self.frac_a + __evap_b * (1. - self.frac_a)

        __list_dict = [{'T_recent [C]': __x, 'mass [%]': __y} for __x, __y in zip(__vT, __evap)]

        # Store __vt and the corresponding blend evaporated fractions in a Pandas DataFrame
        __df = pd.DataFrame(__list_dict)

        # 'Invert' the function to get the temperatures at which tabulated fractions of the blend have evaporated
        __xx = np.array([5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 99])

        s_blend = InterpolatedUnivariateSpline(__df['mass [%]'].values, __df['T_recent [C]'].values, k=2)
        __yy = s_blend(__xx)
        __list_dict = [{'mass [%]': __x, 'T_recent [C]': __y} for __x, __y in zip(__xx, __yy)]

        return pd.DataFrame(__list_dict)
