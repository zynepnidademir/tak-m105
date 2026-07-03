\# Klinik Rehber \& İlaç Etkileşim Güvenliği RAG Asistanı



Doktorların hasta epikrizi ile ilaç prospektüslerini eşleştirip risk analizi yapan,

klinik kılavuzlardan referans göstererek yanıt veren bir RAG (Retrieval-Augmented

Generation) sistemi.



\## 🎯 Proje Amacı



Doktorlar yeni bir ilaç yazarken hastanın mevcut kronik hastalık dökümanlarını ve

klinik tedavi rehberlerini anlık olarak tarayamazlar. Yanlış ilaç kombinasyonları

tıbbi risk doğurur. Bu sistem, ilaç prospektüslerini (KÜB) vektörleştirip saklayan

ve doktorun sorusuna, dokümanlardaki bilgiye sadık kalarak, kaynak göstererek

cevap veren bir asistandır.



\## 🗂️ Mevcut Veri Kaynakları



\- \*\*Warfmadin\*\* 5mg tablet (Varfarin sodyum)

\- \*\*Artril\*\* 600mg film tablet (İbuprofen)

\- \*\*Amaryl\*\* 2mg tablet (Glimepirid)

\- \*\*Atamet\*\* 1000mg film kaplı tablet (Metformin HCl)



\## ⚙️ Teknik Mimari

PDF (KÜB) → Metin Çıkarma → Chunking (1000/200) → Gemini Embedding



→ ChromaDB → Retrieval → Gemini LLM → Streamlit Arayüzü



\- \*\*Vektör veritabanı:\*\* ChromaDB (kalıcı, yerel)

\- \*\*Embedding modeli:\*\* `gemini-embedding-001`

\- \*\*LLM:\*\* `gemini-2.5-flash`

\- \*\*Arayüz:\*\* Streamlit





\## 🚀 Kurulum ve Çalıştırma



\### 1. Gereksinimleri kurun



```bash

pip install -r requirements.txt

```



\### 2. Gemini API key'i ayarlayın



\[Google AI Studio](https://aistudio.google.com/apikey) üzerinden ücretsiz bir API

key alın, ardından ortam değişkeni olarak ayarlayın:



\*\*Windows:\*\*

```bash

setx GEMINI\_API\_KEY "kendi\_key\_iniz"

```

(Ayarladıktan sonra terminali kapatıp yeniden açın.)



\*\*Mac/Linux:\*\*

```bash

export GEMINI\_API\_KEY="kendi\_key\_iniz"

```



\### 3. Vektör veritabanını oluşturun



Bu adım, `data/chunks.json` dosyasındaki tüm metin parçalarını embed edip

kendi bilgisayarınızda yerel bir `chroma\_db` klasörü oluşturur. \*\*Her

geliştiricinin kendi bilgisayarında bir kere çalıştırması gerekir\*\* (chroma\_db

klasörü GitHub'a yüklenmez, `.gitignore` ile hariç tutulmuştur).



```bash

cd klinik-rag-asistan

python chromadb\_yukle.py

```



Bu işlem birkaç dakika sürebilir (180 chunk embed ediliyor).



\### 4. Arayüzü başlatın



```bash

streamlit run app.py

```



Tarayıcınızda otomatik olarak `http://localhost:8501` açılacaktır.



\## 🧪 Test Etme



Sistemin farklı senaryolarda (basit etkileşim, çoklu ilaç, dozaj, kontrendikasyon,

kapsam dışı soru, belirsiz soru) nasıl davrandığını görmek için:



```bash

python test\_sorulari.py

```



\## 📁 Klasör Yapısı

klinik-rag-asistan/



├── data/



│   ├── ilaclar/            # Orijinal KÜB PDF'leri



│   ├── ilaclar\_metin/      # PDF'lerden çıkarılan metinler



│   ├── guidelines/         # Klinik kılavuzlar (varsa)



│   └── chunks.json         # Chunklanmış ve metadata'lanmış veri



├── chunk\_yap.py            # PDF metinlerini chunk'lara böler



├── chromadb\_yukle.py       # Chunk'ları embed edip ChromaDB'ye yükler



├── rag\_sorgula.py          # Retrieval + LLM cevap üretimi (çekirdek RAG mantığı)



├── app.py                  # Streamlit sohbet arayüzü



├── test\_sorulari.py        # Test senaryoları



└── requirements.txt        # Python bağımlılıkları





\## ⚠️ Önemli Notlar



\- Sistem \*\*yalnızca\*\* yüklenen KÜB dokümanlarındaki bilgilere dayanarak cevap

&#x20; verir; dokümanda olmayan bilgi için "yeterli klinik veri bulunamadı" der

&#x20; (halüsinasyon engelleme).

\- Bu bir \*\*prototiptir\*\*, tıbbi tavsiye yerine geçmez. Nihai karar her zaman

&#x20; hekime aittir.

\- `chroma\_db/` klasörü ve API key'ler `.gitignore` ile hariç tutulmuştur,

&#x20; GitHub'a yüklenmezler.

