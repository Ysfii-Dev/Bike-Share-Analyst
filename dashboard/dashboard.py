
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')


# Fungsi untok memproses total penyewaan sepeda

def penyewaan_sepeda_df(df):
    # groupby berdasarkan hari dan hitung total penyewaan
    penyewaan_sepeda = df.groupby(by="dteday").agg({
        "registered": "sum",
        "casual": "sum",
        "cnt": "sum"
    }).reset_index()
    penyewaan_sepeda.rename(columns={
        "registered": "total_registered",
        "casual": "total_casual",
        "cnt": "total_customer"
    }, inplace=True)

    return penyewaan_sepeda

# Fungsi untuk memproses total penyewaan sepeda per jam


def penyewaan_sepeda_per_jam(df):
    # Groupby berdasarkan jam dan hitung total penyewaan sepeda
    penyewaan_perjam = df.copy()

    # rename column
    penyewaan_perjam.rename(columns={
        "cnt": "total_customer"
    }, inplace=True)

    return penyewaan_perjam


# Fungsi untuk memproses pola penyewaan harian


def tren_penyewaan_harian(df):
    # Groupby berdasarkan hari dalam minggu dan hitung rata-rata penyewaan
    tren_harian = df.groupby(by='weekday').agg({
        'cnt': 'mean'
    }).reindex(['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'])
    tren_harian.rename(columns={
        "cnt": "average_customer"
    }, inplace=True)

    return tren_harian


# Fungsi untuk menghitung rata-rata penyewaan sepeda per jam

def tren_penyewaan_per_jam(df):
    # Groupby berdasarkan jam dan hitung rata-rata penyewaan sepeda
    tren_perjam = df.groupby(by="hr").agg({
        'cnt': 'mean'
    }).reset_index()

    # Mengganti nama kolom 'cnt' menjadi 'average_customer'
    tren_perjam.rename(columns={
        "cnt": "average_customer"
    }, inplace=True)

    return tren_perjam


# Fungsi untuk menghitung tren penyewaan sepeda berdasarkan bulan

def tren_penyewaan_bulanan(df):
    # Menghitung tren penyewaan berdasarkan bulan dan menghitung rata-rata penyewaan
    tren_bulanan = df.groupby(by='month').agg({
        'cnt': 'mean'
    }).reindex(['January', 'February', 'March', 'April', 'May', 'June',
                'July', 'August', 'September', 'October', 'November', 'December'])
    tren_bulanan.rename(columns={
        "cnt": "average_customer"
    }, inplace=True)

    return tren_bulanan

# fungsi untuk menghitung total penyewaan berdasarkan cuaca


def pengaruh_cuaca(df):
    # Menghitung total penyewaan berdasarkan cuaca
    cuaca_df = df.groupby(by='weather_description')['cnt'].mean().reset_index()
    cuaca_df.rename(columns={
        'cnt': 'total_customer'
    }, inplace=True)

    return cuaca_df

    # Fungsi untuk mengubah label menjadi numerik pada dataframe baru


def convert_labels_to_numeric(df):
    # Salin df untuk memproses data baru
    ganti_label = df.copy()

    # Mengembalikan nilai label yang sebelumnya ke nilai numerik
    ganti_label['weekday'] = ganti_label['weekday'].map({
        'Sunday': 0, 'Monday': 1, 'Tuesday': 2, 'Wednesday': 3, 'Thursday': 4, 'Friday': 5, 'Saturday': 6
    })

    ganti_label['month'] = ganti_label['month'].map({
        'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
        'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12
    })

    ganti_label['season'] = ganti_label['season'].map({
        'Spring': 1, 'Summer': 2, 'Autumn': 3, 'Winter': 4
    })

    ganti_label['weather_description'] = ganti_label['weather_description'].map({
        'Clear': 1, 'Partly Cloudy': 2, 'Light Snow/Rain': 3, 'Severe Weather': 4
    })

    return ganti_label


# Fungsi untuk clustering berdasarkan temperatur

def clustering_by_temp(df):
    # Menentukan cluster berdasarkan suhu
    df['temp_cluster'] = pd.cut(
        df['temp'],
        bins=[0, 0.3, 0.6, 1],
        labels=['Rendah', 'Sedang', 'Tinggi']
    )

    # Menganalisis rata-rata penyewaan untuk setiap cluster
    clustering = df.groupby('temp_cluster')['cnt'].mean().reset_index()

    return clustering


# load data
data_hour_df = pd.read_csv("./bike_dataset/all_data_hour.csv")
data_day_df = pd.read_csv("./bike_dataset/all_data_day.csv")

# data_hour_df = pd.read_csv(
#     r'D:\Coding\Bike_Sharing_Analysis\bike_dataset\all_data_hour.csv')
# data_day_df = pd.read_csv(
#     r'D:\Coding\Bike_Sharing_Analysis\bike_dataset\all_data_day.csv')

# Columns to convert to datetime
datetime_columns = ["dteday"]

# Process data_hour_df
data_hour_df.sort_values(by="dteday", inplace=True)
# Avoid adding extra index column
data_hour_df.reset_index(drop=True, inplace=True)
for column in datetime_columns:
    data_hour_df[column] = pd.to_datetime(data_hour_df[column])

min_date_hour = data_hour_df["dteday"].min()
max_date_hour = data_hour_df["dteday"].max()

# Process data_day_df
data_day_df.sort_values(by="dteday", inplace=True)
# Avoid adding extra index column
data_day_df.reset_index(drop=True, inplace=True)
for column in datetime_columns:
    data_day_df[column] = pd.to_datetime(data_day_df[column])

min_date_day = data_day_df["dteday"].min()
max_date_day = data_day_df["dteday"].max()


with st.sidebar:
    # Title
    st.title("Yusfi Syawali")

    # Logo Image
    st.image("./dashboard/dicoding.jpg")
    # st.image(r'D:\Coding\Bike_Sharing_Analysis\dashboard\profil.jpg')

    # Menentukan rentang tanggal untuk data_hour_df
    start_date_hour, end_date_hour = st.date_input(
        label='Rentang Waktu (Hourly Data)',
        min_value=min_date_hour,
        max_value=max_date_hour,
        value=[min_date_hour, max_date_hour]
    )

    # Menentukan rentang tanggal untuk data_day_df
    start_date_day, end_date_day = st.date_input(
        label='Rentang Waktu (Daily Data)',
        min_value=min_date_day,
        max_value=max_date_day,
        value=[min_date_day, max_date_day]
    )

# Filter data_hour_df berdasarkan rentang waktu yang dipilih
hour_df = data_hour_df[
    (data_hour_df["dteday"] >= pd.Timestamp(start_date_hour)) &
    (data_hour_df["dteday"] <= pd.Timestamp(end_date_hour))
]

# Filter data_day_df berdasarkan rentang waktu yang dipilih
day_df = data_day_df[
    (data_day_df["dteday"] >= pd.Timestamp(start_date_day)) &
    (data_day_df["dteday"] <= pd.Timestamp(end_date_day))
]

penyewaan_sepeda_day = penyewaan_sepeda_df(day_df)
penyewaan_perjam = penyewaan_sepeda_per_jam(hour_df)
tren_harian = tren_penyewaan_harian(day_df)
tren_perjam = tren_penyewaan_per_jam(hour_df)
tren_bulanan = tren_penyewaan_bulanan(day_df)
cuaca_df = pengaruh_cuaca(day_df)
ganti_label = convert_labels_to_numeric(hour_df)
clustering = clustering_by_temp(day_df)

st.header('Bike Sharing Dashboard 🚲🚲')

col1, col2, col3 = st.columns(3)

with col1:
    total_sewa = penyewaan_sepeda_day.total_customer.sum()
    st.metric("Total Penyewaan", value=total_sewa)

with col2:
    total_registered = penyewaan_sepeda_day.total_registered.sum()
    st.metric("Total Penyewa Terdaftar", value=total_registered)

with col3:
    total_casual = penyewaan_sepeda_day.total_casual.sum()
    st.metric("Total Penyewa Kasual", value=total_casual)

fig, ax = plt.subplots(figsize=(20, 12))
ax.plot(
    penyewaan_sepeda_day["dteday"],
    penyewaan_sepeda_day["total_customer"],
    marker='o',
    linewidth=2,
    color="#FF6F61"
)
ax.set_xlabel("Bulan & Tahun", fontsize=15)
ax.set_ylabel("Total Penyewa", fontsize=15)
ax.set_title("Grafik Total Penyewaan Sepeda)", fontsize=20)
ax.tick_params(axis='y', labelsize=12)
ax.tick_params(axis='x', labelsize=12)
ax.grid(True)

st.pyplot(fig)

with st.expander("Deskripsi Grafik"):
    st.write("""
    **Insight Grafik Total Penyewaan Sepeda**

    Grafik di bawah menunjukkan jumlah total penyewaan sepeda yang terjadi setiap hari dari tahun 2011 hingga 2012.
    Beberapa pola musiman dapat diamati:
    - Penyewaan meningkat pada musim panas.
    - Penurunan terlihat signifikan pada musim dingin.

    Informasi ini bermanfaat untuk menganalisis tren musiman dan kebutuhan penyesuaian layanan.
    """)

st.subheader('Distribusi Data Penyewaan Sepeda Yang Dikumpulkan Per Hari')

fig, ax = plt.subplots(figsize=(20, 12))
sns.histplot(penyewaan_sepeda_day['total_customer'],
             bins=30, color='skyblue', kde=True)
ax.set_title("Distribusi Data Penyewaan Sepeda Per Hari", fontsize=20)
ax.set_xlabel("Total Penyewa", fontsize=15)
ax.set_ylabel("Frekuensi", fontsize=15)
ax.tick_params(axis='y', labelsize=12)
ax.tick_params(axis='x', labelsize=12)
ax.grid(True)

st.pyplot(fig)

with st.expander("Deskripsi Grafik"):
    st.write("""
    **Insight Grafik Distribusi Penyewaan Sepeda Yang Dikumpulkan Per Hari**
    - **Distribusi Penyewaan**: Jumlah penyewaan harian cenderung mengikuti distribusi normal, dengan mayoritas berada di kisaran **4000-6000 penyewaan** per hari. Ini menunjukkan tingkat penggunaan yang konsisten.
    - **Outlier Potensial**: Ada beberapa hari dengan jumlah penyewaan ekstrem (di bawah 2000 dan di atas 8000), yang bisa dianalisis lebih lanjut untuk faktor penyebab seperti cuaca, hari libur, atau event tertentu.""")


st.subheader('Distribusi Data Penyewaan Sepeda Yang Dikumpulkan Per Jam')

fig, ax = plt.subplots(figsize=(20, 12))
sns.histplot(penyewaan_perjam['total_customer'],
             bins=50, color='skyblue', kde=True)
ax.set_title("Distribusi Data Penyewaan Sepeda Per Jam", fontsize=20)
ax.set_xlabel("Total Penyewa", fontsize=15)
ax.set_ylabel("Frekuensi", fontsize=15)
ax.tick_params(axis='y', labelsize=12)
ax.tick_params(axis='x', labelsize=12)
ax.grid(True)

st.pyplot(fig)

with st.expander("Deskripsi Grafik"):
    st.write("""
    **Insight dari Histogram**
    1. **Distribusi Data**:
    - Data jumlah penyewaan per jam terlihat memiliki distribusi yang sangat miring ke kanan (right-skewed).
    - Ada banyak nilai kecil di sekitar 0–100, menunjukkan bahwa sebagian besar waktu jumlah penyewaan rendah.
    2. **Puncak Distribusi**:
    - Puncak tertinggi berada di nilai rendah (sekitar 0–50). Ini mungkin menunjukkan waktu di mana aktivitas penyewaan sepeda rendah, seperti dini hari atau malam.
    3. **Rentang Nilai**:
    - Penyewaan tertinggi mendekati 1000, tetapi itu jarang terjadi.
    4. **Variasi Jumlah Penyewaan**:
    - Ada ketimpangan yang signifikan antara jumlah penyewaan rendah dan tinggi. Anda bisa mengeksplorasi faktor yang memengaruhi pola ini, seperti:
        - Waktu (jam, hari kerja/libur).
        - Cuaca (cerah, hujan).
        - Suhu dan faktor lingkungan lainnya.""")


st.subheader('Tren Penyewaan Sepeda')

tab1, tab2, tab3 = st.tabs(['Tren Harian', 'Tren Per Jam', 'Tren Bulanan'])

with tab1:

    fig, ax = plt.subplots(figsize=(20, 12))
    sns.lineplot(x=tren_harian.index, y='average_customer',
                 data=tren_harian, marker='o', color='skyblue')
    ax.set_title("Tren Penyewaan Sepeda Harian", fontsize=20)
    ax.set_xlabel("Hari dalam Seminggu", fontsize=15)
    ax.set_ylabel("Rata-rata Penyewa", fontsize=15)
    ax.tick_params(axis='y', labelsize=12)
    ax.tick_params(axis='x', labelsize=12)
    ax.grid(True)

    st.pyplot(fig)

    with st.expander("Deskripsi Grafik"):
        st.write("""
        **Insight Grafik Tren Penyewaan Sepeda Harian**
        - **Pola Harian**: Penggunaan sepeda cenderung rendah pada akhir pekan (Sabtu dan Minggu) dan meningkat secara bertahap sepanjang hari kerja, dengan puncaknya pada hari Jumat.
        Ini menunjukkan bahwa aktivitas penyewaan sepeda lebih banyak dilakukan selama hari kerja, kemungkinan terkait dengan perjalanan rutin atau aktivitas profesional.""")


with tab2:

    fig, ax = plt.subplots(figsize=(20, 12))
    sns.lineplot(x=tren_perjam['hr'], y='average_customer',
                 data=tren_perjam, marker='o', color='skyblue')
    ax.set_title("Tren Penyewaan Sepeda Per Jam", fontsize=20)
    ax.set_xlabel("Jam", fontsize=15)
    ax.set_ylabel("Rata-rata Penyewa", fontsize=15)
    ax.tick_params(axis='y', labelsize=12)
    ax.tick_params(axis='x', labelsize=12)
    ax.grid(True)

    st.pyplot(fig)

    with st.expander("Deskripsi Grafik"):
        st.write("""
        **Insight Grafik Tren Penyewaan Sepeda Per Jam**
        - **Pola per jam**: Tren per jam menunjukkan bahwa penyewaan sepeda cenderung meningkat pada pagi hari (jam 6–9) dan sore hari (jam 15–18).
        - **Puncak Penyewaan**: Puncak tertinggi terjadi pada jam 8 dan 17, yang mungkin terkait dengan jam berangkat dan pulang kerja.
        - **Penyewaan Malam**: Penyewaan sepeda cenderung menurun setelah jam 18, menunjukkan bahwa aktivitas penyewaan sepeda lebih sedikit di malam hari.""")


with tab3:

    fig, ax = plt.subplots(figsize=(20, 12))
    sns.lineplot(x=tren_bulanan.index, y='average_customer',
                 data=tren_bulanan, marker='o', color='skyblue')
    ax.set_title("Tren Penyewaan Sepeda Bulanan", fontsize=20)
    ax.set_xlabel("Bulan", fontsize=15)
    ax.set_ylabel("Rata-rata Penyewa", fontsize=15)
    ax.tick_params(axis='y', labelsize=12)
    ax.tick_params(axis='x', labelsize=12)
    ax.grid(True)

    st.pyplot(fig)

    with st.expander("Deskripsi Grafik"):
        st.write("""
        **Insight Grafik Tren Penyewaan Sepeda Bulanan**
        - **Pola Musiman**: Tren bulanan menunjukkan bahwa penyewaan sepeda cenderung meningkat selama musim panas (Juni, Juli, Agustus) dan menurun selama musim dingin (Desember, Januari, Februari).
        - **Puncak Penyewaan**: Puncak tertinggi terjadi pada bulan-bulan musim panas, yang mungkin terkait dengan cuaca yang lebih hangat dan aktivitas luar ruangan yang lebih banyak.
        - **Penurunan Penyewaan**: Penurunan terjadi pada bulan-bulan musim dingin, yang mungkin disebabkan oleh cuaca yang lebih dingin dan kurangnya aktivitas luar ruangan.""")


st.subheader('Faktor-Faktor yang Mempengaruhi Penyewaan Sepeda')

tab1, tab2, tab3 = st.tabs(
    ['Grafik Korelasi antar Variabel', 'Scatter Plot suhu dan Penyewaan Sepeda', 'Grafik Pengaruh Cuaca'])

with tab1:

    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(ganti_label.corr(), annot=True, cmap='coolwarm', fmt='.2f')
    ax.set_title("Korelasi antar Variabel", fontsize=20)

    st.pyplot(fig)

    with st.expander("Deskripsi Grafik"):
        st.write("""
        **Insight Grafik Korelasi antar Variabel**
        - **Korelasi Positif**: Variabel 'registered' dan 'casual' memiliki korelasi sangat tinggi (0.97), menunjukkan hubungan kuat antara jumlah pelanggan terdaftar dan tidak terdaftar.
        - **Korelasi Positif Lainnya**: Variabel 'cnt' berkorelasi tinggi dengan 'registered' (0.97) dan 'casual' (0.69), menandakan kontribusi signifikan kedua jenis pelanggan terhadap total jumlah pelanggan.
        - **Korelasi Lemah**: Variabel 'weather_description' memiliki korelasi lemah terhadap sebagian besar variabel, menunjukkan pengaruh kecil kondisi cuaca terhadap jumlah pelanggan.
        """)


with tab2:

    fig, ax = plt.subplots(figsize=(12, 8))
    sns.scatterplot(x='temp', y='cnt', data=day_df, color='skyblue')
    ax.set_title("Scatter Plot Suhu dan Penyewaan Sepeda", fontsize=20)
    ax.set_xlabel("Suhu", fontsize=15)
    ax.set_ylabel("Total Penyewa", fontsize=15)
    ax.tick_params(axis='y', labelsize=12)
    ax.tick_params(axis='x', labelsize=12)
    ax.grid(True)

    st.pyplot(fig)

    with st.expander("Deskripsi Grafik"):
        st.write("""
        **Insight Scatter Plot Suhu dan Penyewaan Sepeda**
        - **Hubungan Positif**: Terdapat hubungan positif antara suhu dan jumlah penyewaan sepeda. 
        - **Peningkatan Penyewaan**: Ketika suhu meningkat, jumlah penyewaan sepeda juga cenderung meningkat.
        - **Pola Linier**: Terdapat pola linier yang menunjukkan bahwa suhu yang lebih tinggi cenderung meningkatkan jumlah penyewaan.""")

with tab3:

    st.markdown("Berikut adalah pengaruh cuaca terhadap total penyewaan sepeda:")

    for index, row in cuaca_df.iterrows():
        st.markdown(
            f"- **{row['weather_description']
                   }: ** {int(row['total_customer'])} penyewaan"
        )

    fig, ax = plt.subplots(figsize=(20, 12))
    sns.boxplot(x='weather_description', y='cnt',
                data=day_df, hue='weather_description', palette='pastel', legend=True)
    ax.set_title("Grafik Pengaruh Cuaca", fontsize=20)
    ax.set_xlabel("Kondisi Cuaca", fontsize=15)
    ax.set_ylabel("Total Penyewa", fontsize=15)
    ax.tick_params(axis='y', labelsize=12)
    ax.tick_params(axis='x', labelsize=12)
    ax.grid(True)

    st.pyplot(fig)

    with st.expander("Deskripsi Grafik"):
        st.write("""
        **Insight Grafik Pengaruh Cuaca**
        - **Cuaca Cerah**: Cuaca cerah memiliki jumlah penyewaan tertinggi, menunjukkan bahwa kondisi cuaca yang baik meningkatkan minat penyewaan sepeda.
        - **Cuaca Berawan**: Cuaca berawan memiliki jumlah  penyewaan yang sedang, menunjukkan bahwa kondisi cuaca yang tidak terlalu cerah atau hujan tidak mempengaruhi minat penyewaan sepeda.
        - **Hujan Ringan/Salju**: Cuaca hujan ringan/salju memiliki jumlah penyewaan terendah, menunjukkan bahwa kondisi cuaca yang buruk mengurangi minat penyewaan sepeda.""")


st.subheader('Clustering Berdasarkan Temperatur')

st.markdown("Berikut adalah clustering berdasarkan temperatur/Suhu:")
# rename column
clustering.rename(columns={
    'temp_cluster': 'Cluster Suhu',
    'cnt': 'Total Penyewa'
}, inplace=True)
st.write(clustering)

st.markdown("Visualisasi clustering berdasarkan temperatur:")
fig, ax = plt.subplots(figsize=(12, 8))
sns.barplot(x='Cluster Suhu', y='Total Penyewa',
            data=clustering, palette='viridis')
ax.set_title("Clustering Berdasarkan Temperatur/Suhu", fontsize=20)
ax.set_xlabel("Cluster Suhu", fontsize=15)
ax.set_ylabel("Total Penyewa", fontsize=15)
ax.tick_params(axis='y', labelsize=12)
ax.tick_params(axis='x', labelsize=12)
ax.grid(True)

st.pyplot(fig)

with st.expander("Deskripsi Grafik"):
    st.write("""
    **Insight Clustering Berdasarkan Temperatur**
    - **Cluster Suhu**: Data dibagi menjadi 3 cluster berdasarkan suhu: Rendah, Sedang, dan Tinggi.
    - **Total Penyewa**: Cluster suhu tinggi memiliki jumlah penyewaan tertinggi, diikuti oleh cluster suhu sedang dan rendah.
    - **Pola Penyewaan**: Penyewaan sepeda cenderung lebih tinggi pada suhu yang tinggi, menunjukkan preferensi pengguna untuk kondisi suhu yang nyaman.""")


st.caption('Copyright© Yusfi Syawali 2025')
