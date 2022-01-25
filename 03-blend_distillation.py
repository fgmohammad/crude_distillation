# Compute the blend distillation profile given two crude oils and their fractions
from blend import *
import argparse






parser = argparse.ArgumentParser()
parser.add_argument('--name_a', type=str, help='Name of crude_a')
parser.add_argument('--name_b', type=str, help='Name of crude_b')
parser.add_argument('--frac_a', type=float, help='Fraction of crude_a in the blend [0,1]')
parser.add_argument('--fname', type=str, help='filepath for crudes_list.csv')
args = parser.parse_args()


assert (args.frac_a>=0.)&(args.frac_a<=1.)

# Create the blend of the two crudes
my_blend = Blend(name_a=args.name_a, name_b=args.name_b, frac_a=args.frac_a, fname=args.fname)
blend_df = my_blend.htsd_blend

print(blend_df.tail())

