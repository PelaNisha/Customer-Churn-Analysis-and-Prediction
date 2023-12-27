import pandas as pd
from datetime import datetime
def conv_excel(f, t):
    print("t is ", t)
    # df = pd.read_excel(f)
    df1 = pd.read_excel(f, sheet_name="Data Dict")
    df2 = pd.read_excel(f, sheet_name="E Comm")
    # print(df)
    # df.to_excel(str(t) + "data.xlsx", index=False)
    with pd.ExcelWriter(str(t) + "\\data.xlsx", engine='xlsxwriter') as writer:
    # Write each DataFrame to a different sheet
        df1.to_excel(writer, sheet_name='Data Dict', index=False)
        df2.to_excel(writer, sheet_name='E Comm', index=False)
    print("file saved successfully!")
    