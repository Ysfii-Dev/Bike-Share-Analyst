# Submission Dicoding "Belajar Data Analytics dengan Python"

## Project Data Analytics

Repository ini berisi proyek data analytics dari Dicoding yang saya kerjakan. Deployment in **Streamlit**

## Deskripsi

Proyek ini bertujuan untuk menganalisis data pada Bike Sharing Dataset. Dengan tujuan untuk menghasilkan wawasan dan informasi yang berguna dari data yang dianalisis.

## Struktur Direktori

- **/dashboard**: Direktori ini berisi main.py yang digunakan untuk membuat dashboard hasil analisis data.
- **/bike_dataset**: Direktori ini berisi semua data yang digunakan dalam proyek, dalam format .csv.
- **/Proyek_Analisis_Bike_Data.ipynb**: File ini yang digunakan untuk melakukan analisis data.
- **requirements.txt** : File ini berisi library atau pustaka yang diperlukan

## Instalasi Environment

### Pastikan Anda memiliki lingkungan Python yang sesuai dan pustaka-pustaka yang diperlukan. Anda dapat menginstal pustaka-pustaka tersebut dengan menjalankan perintah berikut:

```shell
mkdir proyek_analisis_data
cd proyek_analisis_data
python -m pip install --user virtualenv
python -m venv myenv
myenv\Scripts\activate
pip install -r requirements.txt
```

## Penggunaan

### Masuk ke direktori proyek (Local):

```shell
cd proyek_analisis_data/dashboard/
streamlit run dashboard.py
```
