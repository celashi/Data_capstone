import pandas as pd
import statsmodels.api as sm

def multiple_linear(table, factor_num, result_num, result_name):
    x = sm.add_constant(table[table.columns.values[-factor_num-result_num:-result_num]])
    y = table[result_name]
    model = sm.OLS(y, x)
    result = model.fit()
    predict_value = result.fittedvalues
    print(result.summary())
    return result, predict_value

if __name__ == '__main__':
    table = pd.read_excel('Data.xlsx', sheet_name='Sheet6')
    factor_num = 3
    result_num = 1
    result_name = 'Y'
    multiple_linear(table,factor_num,result_num,result_name)
