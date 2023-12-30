# ppy
csv viewer w/ tk_____Urmarind ghidul am observat ca, de exemplu, folosind setul de date data.csv daca
scriam Durata=6 nu se intampla nimic la apasarea ENTER. Aplicatia era facuta doar pentru stringrui, nu si pentru valori numerice.
Asa ca am vrut sa convertesc din muneric in string folosind str() in argumentul functiei .str.contains dar asta nu a fost de-ajuns.
A trebuit sa convertesc coloanele dataframe-ului in string si am folosit
.astype(str)
https://www.w3schools.com/python/pandas/ref_df_astype.asp


A doua imbunatatire este aceea ca atunci cand dau drop la un fisier care nu este csv ridic o eroare si acest fisier nu intra in listbox
pentru exceptii: https://www.w3schools.com/python/python_try_except.asp
functia .suffix din pathlib: https://stackoverflow.com/questions/5899497/how-can-i-check-the-extension-of-a-file
si am afisat eroare folosind messagebox.showinfo
+am adaugat comentarii peste noul cod din part3
