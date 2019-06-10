# Setup:

Clone this repo:
Download data.zip from [this Google Drive](https://drive.google.com/file/d/19kf-TO5XSbtqTDIgS0lW3btXuTtTNxI4/view?usp=sharing)
and unzip into /data/external.
`cd` to that directory, in your environment, `pip install -e .`
or from any location, `pip install -e /path/to/LocusSummerDataDirectory/`

# Use:

All data loading functions will return pandas DataFrame.

```python
from LocusSummerData import load_data
```

## For functional data (organized by NAICS codes)

You can load data selectively by geography (FIPS or MSA codes),
NAICS codes or NAICS levels, or by year.
For loading data by NAICS or geography, choose to load data
at the MSA or county level. The default is county.

```python
# This will load data for these 2 NAICS codes
load_data.load_by_naics(naics=['813410', '313221'], geo_level='county')

# This will load data for all 2-digit level NAICS codes
load_data.load_by_naics(naics_level=2, geo_level='msa')

# This will load data for these 3 MSAs.
# Specify column_set='all' to get all available columns
# by default only the columns present across all years are loaded
# and no flag columns are loaded
load_data.load_by_geo(['13380', '14340', '49260'], 'msa', column_set='all')

# This will load data by year
load_data.load_by_year(years=[2001])
```

You can also load all functional data at once, then do your own filtering. However, this can be very slow (> 5 minutes) and memory-consuming (>10GB):

```python
load_data.load_all_functional_data(geo_level='county')
```
