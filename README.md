# YouTube Playlist İndirici

Bu Python projesi, YouTube playlistlerini indirmek için bir GUI uygulaması oluşturur. Aşağıda projenin tüm özellikleri ve açıklamaları bulunmaktadır.

## Özellikler:

### 1. **YouTube Playlist İndirme:**
   - Kullanıcı, bir veya birden fazla YouTube playlist URL'si girebilir.
   - Seçilen kaliteye göre video indirilebilir (En Yüksek Kalite, 1080p, 720p, 360p).
   - Playlist'teki videolar sırayla indirilir.

### 2. **İlerleme Durumu Gösterimi:**
   - İndirme işlemi sırasında ilerleme yüzdesi bir progress bar üzerinde gösterilir.
   - İndirme tamamlandığında bir toast bildirimi (Windows 10 için) ile kullanıcıya bilgi verilir.

### 3. **Klasör Seçimi:**
   - Kullanıcı, indirilen videolar için bir klasör seçebilir.

### 4. **Kalite Seçimi:**
   - Kullanıcı, video kalitesini seçebilir (En Yüksek Kalite, 1080p, 720p, 360p).

### 5. **Sistem Kaynakları İzleme:**
   - CPU ve RAM kullanımı her 2 saniyede bir güncellenir ve ekranda gösterilir.

### 6. **Gece/Gündüz Modu:**
   - Kullanıcı arayüzünü "Gece Modu" ve "Gündüz Modu" arasında değiştirebilir.

### 7. **Düşük Seviyeli Socket Timeout Ayarı:**
   - İndirme işlemi sırasında bağlantı zaman aşımına karşı güvenlik önlemleri alınır.

### 8. **Multithreading:**
   - İndirme işlemleri bir thread üzerinde çalışır, bu sayede GUI donmaz.

### 9. **Playlist İndirme Seçenekleri:**
   - Playlist'teki her video tek tek indirilir (playlist'in tüm videoları topluca indirilmez).

### 10. **Tema Özelleştirmeleri:**
   - Koyu ve açık tema seçenekleri mevcut.
   - Tema, butonlar, yazılar ve arka planlar dinamik olarak güncellenebilir.

---

## Kullanım:

1. **İndirme Başlatma:**
   - "İndirmeye Başla" butonuna tıklayarak YouTube playlistlerini indirmeye başlayabilirsiniz.

2. **Klasör Seçme:**
   - "Klasör Seç" butonuna tıklayarak indirilen videolar için bir klasör seçebilirsiniz.

3. **Kalite Seçme:**
   - "Kalite Seçin" dropdown menüsünden video kalitesini belirleyebilirsiniz.

4. **İlerleme Durumu:**
   - İndirme sırasında ilerleme yüzdesi bir progress bar üzerinden izlenebilir.


## Gereksinimler
- Python 3.x
- `yt-dlp` (YouTube video indirme kütüphanesi)
- `psutil` (Sistem kaynaklarını izlemek için)
- `win10toast` (Windows 10'da bildirimler için)
- `tkinter` (GUI oluşturma)
- `threading` (İndirme işlemini arka planda çalıştırma)
