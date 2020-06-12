# vcsv2df

A script to create python dataframe, which then can be processed altered in python. The script `vcsv2df.py` processes a single vcsv file<sup>[1](#fn1)</sup>, while the other file `vcsv_merge.py` takes multiple vcsv files as arguments and creates one merged dataframe. It has an option to write out the dataframe into a csv file with the detected column names.

<a name="fn1">1</a>: vcsv files are ASCII export files from Cadence ViVA waveform viewer.

# Usage
```python
$ python3 vcsv_merge.py slvtnfet_*.vcsv -o slvtnfet.csv
```

The scripts have built-in usage help text:
```bash
$ python3 vcsv_merge.py  -h
usage: vcsv_merge.py [-h] [-o O] f_in [f_in ...]

Read in a VCSV file (from Cadence ViVA waveform data) into a python dataframe
with detected column names and write it out as a csv file

positional arguments:
  f_in        input vcsv file name(s)

optional arguments:
  -h, --help  show this help message and exit
  -o O        output csv file name

$ python3 vcsv2df.py -h
usage: vcsv2df.py [-h] fname_in

Read in a VCSV file (from Cadence ViVA waveform data) into a python dataframe

positional arguments:
  fname_in    input vcsv file

optional arguments:
  -h, --help  show this help message and exit
```
