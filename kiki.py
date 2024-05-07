import streamlit as st  
import requests  # Import requests library bach n9dro ndirou HTTP requests
import pandas as pd  

def get_nationality(name):
    response = requests.get(f"https://api.nationalize.io?name={name}")  # Nsiftou GET request to nationalize.io API
    if response.status_code == 200:
        return response.json()  # Return the JSON data
    else:
        return None  


def display_nationality(data):
    if data and 'country' in data:  # If data is not empty and contains 'country' key
        results = []  
        countries = []  
        probabilities = []  
        for country in data['country']:  # Ndirou loop 3la kol country f data
            countries.append(country['country_id'])  
            probabilities.append(country['probability']*100) 
            result = {
                "Pays": country['country_id'],  # Save the country ID
                "Probabilité (%)": f"{country['probability']*100:.2f}"  
            }
            results.append(result)  # Append the result to the list
        st.bar_chart(pd.DataFrame({'Pays': countries, 'Probabilité (%)': probabilities}), use_container_width=True, height=500)  
        st.write("Probabilités par pays:")  
        for country, probability in zip(countries, probabilities):  # Iterate over countries and probabilities
            st.write(f"{country}: {probability:.2f}%")  # Affichi chaque pays w sa probabilité
        return pd.DataFrame(results)  # Return the results as a DataFrame
    else:
        st.write("Aucune donnée trouvée pour ce nom de famille.")  # Display a message if no data is found
        return pd.DataFrame()  # Return an empty DataFrame

st.title('Devinez l’origine des noms de famille')  # Set the title of the app

name_input = st.text_input('Entrez un nom de famille:', '')  # Text input field for entering a last name

if st.button('Devinez l’origine'):  # Button to trigger the prediction
    if name_input:  # If a last name is entered
        data = get_nationality(name_input)  # Jib nationality dyal le nom
        result_df = display_nationality(data)  # Affichiw l nationality
        st.download_button(
            label="Télécharger les données",
            data=result_df.to_csv(index=False).encode('utf-8'),
            file_name=f"{name_input}_origins.csv",
            mime='text/csv',
        )  # Button to download the data as a CSV file