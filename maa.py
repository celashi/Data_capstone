import pandas as pd
from statsmodels.stats.api import anova_lm
from statsmodels.formula.api import ols

datas = pd.read_excel('Data.xlsx', sheet_name='Sheet4')
model_main_factors = ols("Bubble_count ~ C(Mass_of_sugar,Sum) * C(Fermentation_temperature,Sum)", datas).fit()
anova_main_factors = anova_lm(model_main_factors)
print(anova_main_factors)
