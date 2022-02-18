# Budget_analysis


this repository collects the code for the water budget analysis for alpine basins.
data

  - group_by_month_nc.ipynb groups the daily ERA5 dataset for Evapotranspiration on a monthly basis

  - monthly_budget_f.py is a collection of functions that are exploited in the rest of the repository for aggregating the daily discharge measurments on a monthly basis and clip the era5 dataset on a specific Basin
 
 - Finally, BUDGET_ANALYSIS.ipynb is the notebook where the precipitation, evapotranspiration, and discharge are compared.