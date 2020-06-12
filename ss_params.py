# I will use vcsv2df to create one big dataframe with all simualted small-signal paramters

from vcsv2df import vcsv2df
import argparse
import pandas as pd
from functools import reduce

debug = False

parser = argparse.ArgumentParser(description="""Read in a VCSV file (from Cadence ViVA waveform data) into a python dataframe""")
parser.add_argument("f_in", help="input vcsv file name(s)", nargs='+', type=str) # type=argparse.FileType('r'))
parser.add_argument("-o", help="output csv file name", type=str) # type=argparse.FileType('r'))
args = parser.parse_args()

if debug:
	print(args.f_in)
	for f in args.f_in:
		print(vcsv2df(f))

df_merged = reduce(lambda  left,right: pd.merge(left,right, how='outer'), [vcsv2df(f) for f in args.f_in])
df_merged.to_csv(args.o, index=False)
print(df_merged)

