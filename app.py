
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

st.sidebar.subheader("")
st.sidebar.subheader("Per verificare anche la coerenza con info personali deve avere anche le seguenti colonne scritte esattamente così:")
st.sidebar.text("Nome")
st.sidebar.text("Cognome")
st.sidebar.text("Sesso")
st.sidebar.text("Data di nascita")
st.sidebar.text("Luogo di nascita")




uploaded_file = st.sidebar.file_uploader("Choose a file", type = 'xlsx')
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    Result = pd.DataFrame()

    uu = df.columns 
    if 'c.f.' not in uu:
        st.write("ATTENZIONE: nel file excel non esiste una colonna che si chiama esattamente Codice fiscale")
        st.write("ATTENZIONE: elaborazione interrotta")
        st.write("ATTENZIONE: verificare il file e riprovare")
        st.stop()

    else:
        st.write("VERIFICA DELLA CORRETTA FORMA DEL CODICE FISCALE (NON CONTROLLA COERENZA CON I DATI PERSONALI)")
        for cf in df['c.f.']:
            valid = np.nan
            valido = ""
            try:
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
            except:
                pass
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



        #CONTROLLO SE CI SONO ALTRE COLONNE
        Result_2 = pd.DataFrame()
        st.write("")
        st.write("")
        st.write("")
        st.write("ORA CONTROLLO COERENZA CON I DATI PERSONALI")
        
        if "Nome" not in uu:
            st.write("Nel file manca una colonna che si chiama esattamente Nome")
            st.write("Verificare il file e riprovare")
            st.stop()
        if "Cognome" not in uu:
            st.write("Nel file manca una colonna che si chiama esattemente Cognome")
            st.write("Verificare il file e riprovare")
            st.stop()
        if "Sesso" not in uu:
            st.write("Nel file manca una colonna che si chiama esattemente Sesso")   
            st.write("Verificare il file e riprovare")
            st.stop()
        if "Data di nascita" not in uu:
            st.write("Nel file manca una colonna che si chiama esattemente Data di nascita")
            st.write("Verificare il file e riprovare")
            st.stop()
        if "Luogo di nascita" not in uu:
            st.write("Nel file manca una colonna che si chiama esattemente Luogo di nascita")                 
            st.write("Verificare il file e riprovare")
            st.stop()

        for pp in range(0,len(df)):
            nome = ""
            cognome = ""
            sesso = ""
            data = ""
            luogo = "" 


            nome = df['Nome'][pp]
            cognome = df['Cognome'][pp]
            sesso = df['Sesso'][pp]
            data = df['Data di nascita'][pp]
            luogo = df['Luogo di nascita'][pp]
            cf = df['Codice fiscale'][pp]
            
            cf_recode = codicefiscale.encode(
                    lastname=cognome,
                    firstname=nome,
                    gender=sesso,
                    birthdate=data,
                    birthplace=luogo,
                )
            
            if cf == cf_recode:
                coerenza = "CF COERENTE CON DATI PERSONALI"
            else:
                coerenza = "CF NON COERENTE CON DATI PERSONALI"

            df_ciclo_2 = pd.DataFrame(columns = ['Nome','Cognome','Sesso','Data di nascita','Luogo di nascita','Codice fiscale','Coerenza'])
            df_ciclo_2.loc[0] = [nome, cognome, sesso, data, luogo, cf, coerenza]

            Result_2 = pd.concat([Result_2, df_ciclo_2], axis = 0)            
            
        st.dataframe(Result_2)

        # buffer to use for excel writer
        buffer = io.BytesIO()

        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            # Write each dataframe to a different worksheet.
            Result_2.to_excel(writer, sheet_name='Sheet1', index=False)

            writer.close()

            download = st.download_button(
                label="Download data as Excel",
                data=buffer,
                file_name='verifica_coerenza_codici_fiscali.xlsx',
                mime='application/vnd.ms-excel'
            )
