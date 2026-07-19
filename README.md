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
Daily Scrum: Daily Scrum toplantıları whatsapp üzerinden gerçekleştirilmiştir.Günlük notlar ortak word dosyasında tutulmuştur.https://istanbulstunv-my.sharepoint.com/:w:/g/personal/sumeyye_agir_istun_edu_tr/IQBfnHyNTka2QqJG93As4EGYARcI0udwbVqhLLohXYJFLSs?e=n2VJF5.
Sprint board update: Sprint board görünümü ve kart durumları için: <img width="1277" height="578" alt="image" src="https://github.com/user-attachments/assets/2fb3aaa6-5d55-4bba-82e1-4a34612fb5e8" />


Ürün Durumu: Sprint 1 sonunda ChromaDB kurulumu, veri toplama, chunking, ChromaDB + Gemini embedding entegrasyonu, Gemini LLM ile retrieval, Streamlit arayüzü ve hata dayanıklılığı (retry mekanizması) tamamlanmıştır. 
<img width="1265" height="693" alt="image" src="https://github.com/user-attachments/assets/3c217eaa-25ae-4d60-a529-c14664873eee" />

Sprint Review:
Alınan kararlar: Uçtan uca çalışan bir RAG sistemi (ChromaDB + Gemini + Streamlit) başarıyla oluşturulmuştur. Sistemin hata dayanıklılığı (retry mekanizması) ve prompt tutarlılığı iyileştirilmiştir. Ekstra olarak konuşma hafızası ve soru sınıflandırma (router) özelliklerinin eklenmesine karar verilmiştir. Sprint Review katılımcıları: Rümeysa Akkora,Sümeyye Ağır,Sefa Bulut

Sprint Retrospective:

Ekip içi görev dağılımının branch/PR workflow'una geçilerek daha net hale getirilmesi kararı alınmıştır
Ortak dosyalar (rag_sorgula.py) üzerinde çalışırken çakışmaları önlemek için herkesin ayrı feature branch açması gerektiği belirlenmiştir
Prompt ve test senaryoları için ayrılan efor bir sonraki sprintte arttırılmalıdır.


Sprint 2
Backlog Düzeni ve Story Seçimleri
Sprint 2'de backlog, Sprint 1'de kurulan çekirdek RAG altyapısının olgunlaştırılmasına ve ölçeklenmesine yönelik story'lere göre önceliklendirilmiştir. Story'ler; performans/güvenilirlik iyileştirmeleri (cache, router, timeout), veri seti genişletme, prompt/test kapsamının artırılması ve entegrasyon yönetimi olmak üzere görev bazında bölünmüştür. Ekip, Sprint Retrospective'te alınan karar doğrultusunda artık branch/PR workflow'u üzerinden çalışmıştır; her ekip üyesi kendi feature branch'inde (zeynep, prompt, ui, gorev-b-backend) geliştirme yapmış, tamamlanan işler Pull Request ile main branch'e alınmıştır.
Daily Scrum
Daily Scrum toplantıları Sprint 1'de olduğu gibi WhatsApp üzerinden gerçekleştirilmiştir. Günlük notlar ortak Word dosyasında tutulmaya devam edilmiştir: https://istanbulstunv-my.sharepoint.com/:w:/g/personal/sumeyye_agir_istun_edu_tr/IQBfnHyNTka2QqJG93As4EGYARcI0udwbVqhLLohXYJFLSs?e=n2VJF5

Sprint Board Update
Sprint board görünümü ve kart durumları Trello üzerinden takip edilmiştir. 
<img width="1157" height="528" alt="trello1" src="https://github.com/user-attachments/assets/13d7cbc5-3778-419c-bba4-b6ea11fe0e17" />


Ürün Durumu

<img width="1278" height="677" alt="image" src="https://github.com/user-attachments/assets/cd306c8b-c030-42d9-a75d-d62d9df944f6" />
<img width="1280" height="643" alt="image" src="https://github.com/user-attachments/assets/b55c4c98-3422-4d0e-a115-1963a49923ff" />
<img width="985" height="473" alt="image" src="https://github.com/user-attachments/assets/03ba5376-9e45-4731-84f2-e885f881361a" />



Sprint 2 sonunda:

Cevap önbellekleme (cache) mekanizması eklenmiştir; tekrarlanan sorularda gereksiz API çağrısı yapılmayarak hem yanıt süresi hem de API kotası korunmuştur. Cache kayıtlarına 7 günlük geçerlilik süresi (expiry) eklenmiş, başarısız/hatalı cevapların önbelleğe kalıcı olarak yazılması önlenmiştir.
Çoklu ilaç router (soru sınıflandırma) mantığı geliştirilmiştir: bir soruda birden fazla ilaç adı geçtiğinde, her ilaç için ayrı ayrı retrieval yapılarak hiçbir ilacın sonuçlardan kaybolmaması garanti altına alınmıştır. Bu mantık hem 2 ilaçlı hem 3+ ilaçlı senaryolarda test edilmiştir.
n_results ve chunk optimizasyonu için karşılaştırmalı testler yapılmış, router mantığının bu ihtiyacı doğrudan çözdüğü doğrulanmıştır.
API çağrılarına 30 saniyelik zaman aşımı (timeout) koruması eklenmiştir; ayrıca rate limit (429), sunucu yoğunluğu (503) ve bağlantı hatalarında otomatik yeniden deneme mekanizması güçlendirilmiştir.
Veri seti genişletilmiştir: mevcut 4 ilaca ek olarak 5 yeni ilaç (Delix Plus, Plavix, Lipitor, Norvasc, Beloc Zok) prospektüsleri eklenmiş, toplam chunk sayısı 180'den 391'e çıkarılmıştır. Yeni ilaçlar router'ın anahtar kelime haritasına da başarıyla entegre edilmiştir.
Prompt iyileştirmesi: Sistem promptu, yanıtları standart bir klinik rapor formatında (ÖZET / BULGULAR / RİSK SEVİYESİ / KAYNAKLAR) üretecek şekilde yeniden yapılandırılmıştır.
Test kapsamı genişletilmiştir: test_sorulari.py'ye yeni senaryolar (çoklu ilaç, kapsam dışı sorular, belirsiz sorular, doz soruları) ve router regresyon testi eklenmiştir.
Model/kota yönetimi: Geliştirme sürecinde gemini-3.5-flash modelinin günlük ücretsiz kota limitinin (20 istek) yetersiz kaldığı tespit edilmiş, sistem daha stabil kotaya sahip gemini-2.5-flash modeline geri döndürülmüştür.
Sprint boyunca açılan feature branch'ler (prompt, ui, zeynep) Pull Request süreciyle main branch'e entegre edilmiş, entegrasyon sonrası uçtan uca test yapılarak sistemin bütünlüğü doğrulanmıştır.

Sprint Review
Alınan kararlar:

Router (soru sınıflandırma) ve cache mekanizmalarının Sprint 1 sonunda planlanan hedefe uygun şekilde başarıyla tamamlandığına karar verilmiştir.
Ücretsiz API kotasının sprint sunumu/demo günü risk oluşturabileceği değerlendirilmiş; gerekirse demo öncesi geçici olarak ücretli (pay-as-you-go) katmana geçiş yapılması kararı alınmış, bu karar sprint sonuna bırakılmıştır.
Veri setinin 9 ilaca genişletilmesiyle sistemin ölçeklenebilirliği gerçek koşullarda test edilmiş ve doğrulanmıştır.
Bir ekip üyesinin (Backend) PR'ı, kapsam ve test edilebilirlik açısından yeterli görülmediği için bu sprintte main'e alınmamasına karar verilmiştir; ilgili görevlerin bir sonraki sprintte netleştirilerek yeniden ele alınması planlanmıştır.

Sprint Review katılımcıları: Zeynep Nida Demir, Rümeysa Akkora, Sümeyye Ağır,Sefa Bulut
Sprint Retrospective

Branch/PR workflow'una geçiş genel olarak başarılı olmuş, ancak birden fazla kişinin aynı dosyada (rag_sorgula.py) eş zamanlı çalışması zaman zaman merge çakışmalarına yol açmıştır; bir sonraki sprintte dosya/modül bazlı sorumluluk paylaşımının netleştirilmesi gerektiği belirlenmiştir.
Main branch'in her zaman "çalışır ve test edilmiş" durumda tutulması ilkesi benimsenmiş, bunun için tüm PR'ların merge öncesi entegrasyon testinden geçirilmesi standart hale getirilmiştir.
API kota yönetiminin proje başında daha net planlanması gerektiği, model değişikliklerinin (ör. LLM_MODEL) ekip içinde önceden iletişilmeden yapılmasının kota/kararlılık sorunlarına yol açabildiği görülmüştür.
Prompt ve test senaryolarına ayrılan efor Sprint 1'deki karara uygun şekilde artırılmış ve bu alanda somut ilerleme (yapılandırılmış cevap formatı, genişletilmiş test seti) sağlanmıştır; bu yaklaşımın bir sonraki sprintte de sürdürülmesine karar verilmiştir.

