# Budget_analysis


this repository collects the code for the water budget analysis for alpine basins.
data

  - group_by_month_nc.ipynb groups the daily ERA5 datasets on a monthly basis

  - monthly_budget_funcions.py is a collection of functions that are exploited in the rest of the repository for aggregating the daily discharge measurments on a monthly basis and clip the era5 dataset on a specific Basin

 -  MAKE_CSV.ipynb is the notebook where inputs to the above-mentioned functions should be defined
 
 - Finally, Comparison.ipynb is the notebook where the precipitation, evapotranspiration, and discharge are compared.
