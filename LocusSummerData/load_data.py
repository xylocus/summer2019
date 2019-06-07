import os
import pandas as pd
import glob
from tqdm import tqdm, tqdm_notebook

MODULE_PATH = os.path.dirname(os.path.realpath(__file__))
FUNC_DATA = os.path.join(MODULE_PATH, os.pardir, 'data', 'functional')
OUTCOME_DATA = os.path.join(MODULE_PATH, os.pardir, 'data', 'outcome')
METADATA = os.path.join(MODULE_PATH, os.pardir, 'data', 'metadata')


def _load_data_from_paths(paths, geo_level, column_set, notebook):
    """Helper method to load CBP data from given list of file paths.

    Arguments:
        :: paths {list} -- list of paths to data that needed to be loaded
        :: geo_level {str} -- 'msa' or 'county'
        :: column_set {str} -- variables to load.
        'all': load all available columns.
        'strict': only load the most essential columns.
        :: notebook {bool} -- is the module running in a Jupyter notebook?
        The only purpose is to correctly display progress bar.
        (default: True)
    Return:
        single pandas Dataframe of data from specified paths.
    """
    strict_column_set = {'msa': ['MSA', 'YEAR', 'NAICS', 'emp_imputed', 'PAYANN', 'ESTAB'],
                         'county': ['FIPS', 'YEAR', 'naics_level',
                                    'naics', 'emp_imputed', 'PAYANN', 'ESTAB']}

    progress_bar = tqdm_notebook if notebook else tqdm
    res = []

    for path in progress_bar(paths):
        try:
            df = pd.read_csv(path, dtype='str')
            if column_set == 'strict':
                df = df[strict_column_set[geo_level]]
            res.append(df)
        except FileNotFoundError as e:
            print(e)
    return pd.concat(res)


def load_by_year(years, geo_level='county', column_set='strict', notebook=True):
    """
    Load functional data only for selected years
    column_set is 'strict': only a subset of columns present in all years
    will be loaded or 'all': all columns are loaded

    Arguments:
        :: years {list of int or str} -- desired years.
        :: geo_level {str} -- 'msa' or 'county' (default: 'county')
        :: column_set {str} -- variables to load. 'all': load all available columns.
        'strict': only load the most essential columns.
        (default: 'strict')
        :: notebook {bool} -- is the module running in a Jupyter notebook?
        The only purpose is to correctly display progress bar.
        (default: True)
    Return:
        pandas Dataframe of desired functional data.
    """
    paths = []
    for year in years:
        path = os.path.join(FUNC_DATA, 'year', geo_level,
                            f'cbp_year_{geo_level}_{year}.csv')
        paths.append(path)
    return _load_data_from_paths(paths, geo_level, column_set, notebook)


def load_by_naics(naics=[], naics_level=None, geo_level='county', column_set='strict', notebook=True):
    """
    Load functional data only for selected naics codes
    column_set is 'strict': only a subset of columns present in all years
    will be loaded or 'all': all columns are loaded

    Arguments:
        :: naics {list of str} -- desired naics codes. {default: []}
        :: naics_level {int} -- If int, load all naics at that level.
        If specified, argument naics must then be empty. {default: 2}
        :: geo_level {str} -- 'msa' or 'county' (default: 'county')
        :: column_set {str} -- variables to load. 'all': load all available columns.
        'strict': only load the most essential columns.
        (default: 'strict')
        :: notebook {bool} -- is the module running in a Jupyter notebook?
        The only purpose is to correctly display progress bar.
        (default: True)
    Return:
        pandas Dataframe of desired functional data.
    """
    # naics level specified, no naics specified
    if naics_level:
        if naics:
            raise ValueError(
                'if naics_level is specified, naics must be empty list')
        # each ? will match with any 1 digit, thus multiply ? by naics_level
        wild_card = '?' * naics_level
        glob_path = os.path.join(FUNC_DATA, 'naics', geo_level,
                                 f'cbp_naics_{geo_level}_{wild_card}.csv')
        paths = glob.glob(glob_path)

    # naics specified, not level
    else:
        if naics_level:
            raise ValueError(
                'if naics is specified, naics_level must be None'
            )
        paths = []
        for code in naics:
            path = os.path.join(FUNC_DATA, 'naics', geo_level,
                                f'cbp_naics_{geo_level}_{code}.csv')
            paths.append(path)

    return _load_data_from_paths(paths, geo_level, column_set, notebook)


def load_by_geo(geo_codes, geo_level, column_set='strict', notebook=True):
    """
    Load functional data only for selected fips or msa codes
    column_set is 'strict': only a subset of columns present in all years
    will be loaded or 'all': all columns are loaded

    Arguments:
        :: geo_codes {list} -- desired fips or msa codes.
        :: geo_level {str} -- 'msa' or 'county'. Needs to be in agreement with
        geo_codes.
        :: column_set {str} -- variables to load. 'all': load all available columns.
        'strict': only load the most essential columns.
        (default: 'strict')
        :: notebook {bool} -- is the module running in a Jupyter notebook?
        The only purpose is to correctly display progress bar.
        (default: True)
    Return:
        pandas Dataframe of desired functional data.
    """
    paths = []
    for code in geo_codes:
        path = os.path.join(FUNC_DATA, 'geo', geo_level,
                            f'cbp_{geo_level}_{code}.csv')
        paths.append(path)
    return _load_data_from_paths(paths, geo_level, column_set, notebook)


def load_functional_data(geo_level='county'):
    """Load all functional (CBP) data to a dataframe.
    Could be very slow & consumes a lot of memory.

    Keyword Arguments:
        :: geo_level {str} -- 'county' or 'msa' (default: {'county'})

    Returns:
        pandas Dataframe of functional data.
    """
    print('Warning: This may take over 5 minutes & consumes > 10GB of memory')
    path = os.path.join(FUNC_DATA, f'cbp_{geo_level}.csv')
    return pd.read_csv(path, dtype=str)


def load_outcome_data(geo_level='county', dataset='cleaned'):
    """Load outcome data to a data frame.

    Keyword Arguments:
        :: geo_level {str} -- 'county' or 'msa' (default: {'county'})
        :: dataset {str} -- 'all' or 'cleaned' (default: {'cleaned'})
    Returns:
        pandas Dataframe of CBP data.
    """
    path = os.path.join(OUTCOME_DATA, f'acs_{dataset}_{geo_level}.csv')
    return pd.read_csv(path, dtype=str)


def load_outcome_metadata():
    path = os.path.join(METADATA, 'outcome_metadata.csv')
    return pd.read_csv(path, dtype=str)


def long_to_wide(df, geo):
    """Given df in long format, convert to wide on variable column"""
    df['year_geo'] = df['YEAR'] + '_'+df[geo]
    pivot = df[['year_geo', 'value', 'explanation']].set_index(
        ['year_geo']).pivot(values='value', columns='explanation')
    pivot = pivot.reset_index()
    pivot['YEAR'] = pivot['year_geo'].apply(lambda x: x.split('_')[0])
    pivot[geo] = pivot['year_geo'].apply(lambda x: x.split('_')[1])
    pivot = pivot.drop('year_geo', axis=1)
    return pivot


def get_data_from_metadata(query, nf, geo_level):
    """
    Given metadata query - a DataFrame with at least these columns:
    year, variable_name, topic, explanation
    And nf - a DataFrame containing functional data with at least
    YEAR & variable column (which has format topic_variable_name)
    Return the data for these year + variable_name + topic combination
    at the specified geographical level.
    """
    d = {'msa': 'MSA', 'county': 'FIPS'}
    geo = d[geo_level]
    nf = nf[['YEAR', geo, 'variable', 'value']]
    nf = nf[
        nf[geo] != 'Id2'
    ]
    query['variable'] = query['topic'] + '_' + query['variable_name']
    query = query.rename(columns={'year': 'YEAR'})
    merged = nf.merge(query, on=['YEAR', 'variable'])
    return long_to_wide(merged, geo)
