
import os
import streamlit as st 
import numpy as np 
import pandas as pd 
from codicefiscale import codicefiscale
import io
import xlsxwriter

### SIDEBAR 
st.sidebar.subheader("Verifica Codice Fiscali")
st.sidebar.subheader("Carica file excel")
st.sidebar.subheader("Il file excel deve avere una colonna che si chiama esattamente Codice fiscale")



uploaded_file = st.sidebar.file_uploader("Choose a file", type = 'xlsx')
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    Result = pd.DataFrame()

    uu = df.columns 
    if 'Codice fiscale' not in uu:
        st.write("ATTENZIONE: nel file excel non esiste una colonna che si chiama esattamente Codice fiscale")
        st.write("ATTENZIONE: elaborazione interrotta")
        st.write("ATTENZIONE: verificare il file e riprovare")

    else:
        for cf in df['Codice fiscale']:
            valid = np.nan
            valido = ""
            valid = codicefiscale.is_valid(cf)
            if valid == True:
                st.write("Il codice fiscale " + cf + " è OK")
                valido = "OK"
            else:
                st.write("Il codice fiscale " + cf + " NON è OK")
                valido = "NON OK"

            df_ciclo = pd.DataFrame(columns = ['Codice fiscale','Valido'])
            df_ciclo.loc[0] = [cf, valido]

            Result = pd.concat([Result, df_ciclo], axis = 0)
            
            
        st.dataframe(Result)


        # buffer to use for excel writer
        buffer = io.BytesIO()

        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            # Write each dataframe to a different worksheet.
            Result.to_excel(writer, sheet_name='Sheet1', index=False)

            writer.close()

            download = st.download_button(
                label="Download data as Excel",
                data=buffer,
                file_name='verifica_codici_fiscali.xlsx',
                mime='application/vnd.ms-excel'
            )