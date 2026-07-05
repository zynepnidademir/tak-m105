Takım İsmi

Takım-105

Ürün İle İlgili Bilgiler

Takım Elemanları


Zeynep Nida Demir: Scrum Master / Developer
Rumeysa Akkora: Product Owner / Developer
Sümeyye Ağır: Developer (Prompt & Test)
Sefa Bulut: Developer (Backend)


Ürün İsmi

--Klinik Rehber & İlaç Etkileşim Güvenliği RAG Asistanı--

Ürün Açıklaması

Doktorların hasta epikrizi ile ilaç prospektüslerini (KÜB) hızlıca eşleştirip ilaç etkileşimi risklerini analiz edebildiği, klinik kılavuzlardan referans göstererek yanıt üreten bir RAG (Retrieval-Augmented Generation) asistanıdır. Sistem, ChromaDB üzerinde tutulan vektörleştirilmiş ilaç ve kılavuz verilerini Gemini LLM ile birleştirerek doktorlara güvenli ve kaynaklı klinik yanıtlar sunar.

Ürün Özellikleri


İlaç prospektüslerinden (KÜB) otomatik chunking ve embedding çıkarımı
ChromaDB tabanlı semantik arama ile ilgili doküman parçalarının getirilmesi
Gemini LLM ile bağlama dayalı, kaynak gösteren yanıt üretimi
İlaç-ilaç etkileşimi risklerinin tespiti (örn. warfarin-ibuprofen kanama riski)
Klinik kılavuzlardan referans gösterme
Streamlit tabanlı sohbet arayüzü
API çağrılarında otomatik yeniden deneme (retry) ile hata dayanıklılığı



Hedef Kitle


Hastanelerde ve kliniklerde görev yapan doktorlar
Eczacılar ve klinik eczacılar
Reçete güvenliğinden sorumlu sağlık personeli
Tıp fakültesi öğrencileri ve asistan hekimler


Product Backlog URL

https://trello.com/b/vC556Wu1/yzta-bootcamp-klinik-rehber-i%CC%87lac-etkilesim-guvenligi-rag-asistani


Sprint 1


Backlog düzeni ve Story seçimleri: Backlog, ilk sprintte tamamlanması hedeflenen çekirdek RAG altyapısına göre önceliklendirilmiştir. Story'ler; veri hazırlama, ChromaDB entegrasyonu, LLM entegrasyonu ve arayüz geliştirme olmak üzere görev (task) bazında bölünmüştür. Görevler Trello board üzerinde Backlog, Sprint 1 - To Do, In Progress ve Done listeleri altında takip edilmektedir.
Daily Scrum: Daily Scrum toplantı notları Trello board üzerindeki "Daily Notes" listesinde, her gün için açılan kart üzerinden ekip üyelerinin yorumlarıyla tutulmaktadır.
Sprint board update: Sprint board görünümü ve kart durumları için: <img width="1277" height="578" alt="image" src="https://github.com/user-attachments/assets/2fb3aaa6-5d55-4bba-82e1-4a34612fb5e8" />


Ürün Durumu: Sprint 1 sonunda ChromaDB kurulumu, veri toplama, chunking, ChromaDB + Gemini embedding entegrasyonu, Gemini LLM ile retrieval, Streamlit arayüzü ve hata dayanıklılığı (retry mekanizması) tamamlanmıştır. 
Sprint Review:
Alınan kararlar: Uçtan uca çalışan bir RAG sistemi (ChromaDB + Gemini + Streamlit) başarıyla oluşturulmuştur. Sistemin hata dayanıklılığı (retry mekanizması) ve prompt tutarlılığı iyileştirilmiştir. Ekstra olarak konuşma hafızası ve soru sınıflandırma (router) özelliklerinin eklenmesine karar verilmiştir. Sprint Review katılımcıları: Rümeysa Akkora,Sümeyye Ağır,Sefa Bulut
Sprint Retrospective:

Ekip içi görev dağılımının branch/PR workflow'una geçilerek daha net hale getirilmesi kararı alınmıştır
Ortak dosyalar (rag_sorgula.py) üzerinde çalışırken çakışmaları önlemek için herkesin ayrı feature branch açması gerektiği belirlenmiştir
Prompt ve test senaryoları için ayrılan efor bir sonraki sprintte arttırılmalıdır
