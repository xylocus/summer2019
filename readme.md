# Setup:

**Git**
1. Clone this repo.

**Folder structure**
2. With the ‘Makefile’ file in folder where repo is cloned, run `make init` to automatically create the standardized folder structure.

**Data download**
3. Download data.zip from [this Google Drive](https://drive.google.com/file/d/19kf-TO5XSbtqTDIgS0lW3btXuTtTNxI4/view?usp=sharing)
and unzip into /data/external.

**Virtual environment**
4. `cd` to that directory, make sure Pipfile is located there, then run `pipenv shell` followed by `pipenv install` to install all of the package dependencies.

To use this virtual environment, run `pipenv shell`
and to use it in a jupyter notebook, run `pipenv run jupyter notebook` when the shell is activated.

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


**Other references for Visualizing and Analyzing Data**
[Locus DB guide](https://github.com/LocusAnalytics/locus_db)

[Locus Handler guide](https://pypi.org/project/locushandler/#description)

[Locus geoviz tutorial](https://locusanalytics.github.io/files/geoviz_tutorial.html)

[Pandas cheatsheet](https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf)

[Ipywidgets tutorial](https://towardsdatascience.com/interactive-controls-for-jupyter-notebooks-f5c94829aee6)

[General guideline to visualization tools](https://docs.google.com/document/d/1zCktFbAPwyzxRcTPvQ9dQKPdgYANo6hdsUM3y0LRbyg/edit?ts=5bb247a0)
