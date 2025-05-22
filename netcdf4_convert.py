import pandas as pd
import yaml
import xarray as xr
import numpy as np
import glob

with open("config.yaml") as stream:
    config = yaml.safe_load(stream)

files = glob.glob('*.xlsx')
for filename in files:
    print(filename)
    data = pd.read_excel(filename, sheet_name=None, index_col=0, skiprows=0)

    output = {}
    for name in config[filename]['data'].keys():
        output[name] = xr.DataArray(data=data[name].values.squeeze(),
                                    coords={k: np.linspace(
                                        *config[filename][k], 
                                        data[name].values.shape[k_ind])
                                        for k_ind, k in enumerate(config[filename]['axes'])},
                                    dims=config[filename]['axes'],
                                    attrs={'units':config[filename]['data'][name]['units'],
                                           'longname':config[filename]['data'][name].get('longname', name)})

    xr.Dataset(output).to_netcdf(filename.replace('xlsx', 'nc'))
