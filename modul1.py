 import pandas as pd
 
 def excelden_faturalari_oku(excel_path):
     df = pd.read_excel(excel_path)
 

    faturalar_df = pd.DataFrame({
        "excel_ref": df.iloc[:, 0],
        "fatura_no": (
            df.iloc[:, 6]
            .astype("string")
            .str.strip()
            .str.replace(r"\.0$", "", regex=True)
        ),
        "bakiye_excel": pd.to_numeric(df.iloc[:, 10], errors="coerce")
    })
 
     faturalar_df = faturalar_df[faturalar_df["fatura_no"] != "nan"]
 
     return faturalar_df
 
EOF
)
