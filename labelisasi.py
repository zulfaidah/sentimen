import pandas as pd
from googletrans import Translator
from textblob import TextBlob

from labelisasi import labelisasi_teks, preprocessing_data, analisis_sentimen

# Menggunakan Translator dari googletrans untuk menerjemahkan teks
df = pd.DataFrame(judul.judul)
translator = Translator()
translations = {}
for column in df.columns:
    unique_elements = df[column].unique()
    for element in unique_elements:
        translations[element] = translator.translate(element).text

# Memasukkan hasil terjemahan ke kolom baru 'translated_text'
judul['translated_text'] = df.replace(translations)
judul['translated_text'] = judul['translated_text'].str.replace('([^0-9A-Za-z \t])|(\w+:\/\/\S+)', ' ')
judul['translated_text'] = judul['translated_text'].str.lower()


# Fungsi untuk menghitung subjektivitas
def subjektivitas(tr_text):
    return TextBlob(tr_text).sentiment.subjectivity

# Fungsi untuk menghitung polaritas
def polaritas(tr_text):
    return TextBlob(tr_text).sentiment.polarity

# Fungsi untuk menghasilkan label sentimen
def hasilSentimen(nilai):
    if nilai < 0:
        return 'negative'
    elif nilai == 0:
        return 'neutral'
    else:
        return 'positive'

# Menghitung subjektivitas dan polaritas, serta menambahkan kolom sentimen ke dataframe
judul['subjektivitas'] = judul['translated_text'].apply(subjektivitas)
judul['polaritas'] = judul['translated_text'].apply(polaritas)
judul['sentimen'] = judul['polaritas'].apply(hasilSentimen)


# Menyimpan hasil labelisasi ke dalam file CSV
df = judul[['judul','translated_text','sentimen']]
df.to_csv("drive/MyDrive/Skripsi.lnk/Data Preprocessing/labelisasi_judul.csv", index=False)

# Menyimpan hasil labelisasi yang hanya berisi judul dan sentimen ke file CSV
df = judul[['judul', 'sentimen']]
df.to_csv("drive/MyDrive/Skripsi.lnk/Data Preprocessing/labelisasi_langsung.csv", index=False)
