import numpy as np
import pandas as pd

public_holidays = ['2020-03-08','2020-03-25','2020-03-30','2020-03-31']
dti= pd.bdate_range(start='03/02/2020', end='03/05/2020', freq = 'C',
                    holidays=public_holidays,
                    weekmask = 'Mon Tue Wed Thu Fri Sat')
print(dti)
