# Hastane Acil Servis Tedavi Simülasyonu

Bu proje, bir hastane acil servisinin tedavi süreçlerini simüle etmek için geliştirilmiştir. Hastalar, önceliklerine ve tedavi sürelerine göre sıralanarak tedavi edilir. Tedavi edilemeyen hastalar daha sonra kaydedilir.

## Proje Özeti

Bu uygulama, **FastAPI** ile yazılmıştır ve hastaların tedavi sırasını **min-heap** yapısını kullanarak yönetir. Hastaların öncelikleri, tedavi süreleri ve sıralama mantığına göre tedavi edilir. Günlük tedavi limitine ulaşıldığında tedavi edilemeyen hastalar kaydedilir.

## Teknolojiler

- **Python 3.x**
- **FastAPI**
- **Jinja2 (HTML Template Engine)**
- **Heapq (Min-Heap Yönetimi)**
- **HTML, CSS (Basit UI için)**

## Özellikler

- **Hastalar Sıralaması:** Hastalar, acil durum önceliğine ve tedavi sürelerine göre sıralanır.
- **Tedavi Simülasyonu:** Günlük tedavi süresi limiti olan 7 saat (420 dakika) içinde tedavi edilebilecek hastalar işleme alınır.
- **Raporlama:** Tedavi edilen ve tedavi edilemeyen hastaların listeleri raporlanır.
- **Yeni Hasta Ekleme:** Kullanıcılar, yeni hasta bilgilerini girerek hasta ekleyebilirler.

## Kullanım

1. Projeyi indirin ve gerekli paketleri yükleyin:

   ```bash
   git clone https://github.com/your-repo/hastane-acil-servis-simulasyonu.git
   cd hastane-acil-servis-simulasyonu
   pip install -r requirements.txt
   ```

2. FastAPI uygulamasını başlatın:

   ```bash
   uvicorn main:app --reload
   ```

3. Uygulamayı tarayıcıda açın:

   ```
   http://127.0.0.1:8000
   ```

4. Kullanıcı arayüzü üzerinden:
   - Yeni hasta ekleyebilir ve hastanın **HastaID**, **Öncelik** ve **Tedavi Süresi** bilgilerini girebilirsiniz.
   - **Simülasyon başlatma** butonuna basarak, tedavi simülasyonunu başlatabilirsiniz.
   - Tedavi edilen ve edilemeyen hastalar raporlanacaktır.

## API Sonuçları

### Tedavi Simülasyonu Raporu

- **Hastalar Sırası:** Henüz tedavi edilmemiş hastaların sırasıdır.
- **Tedavi Edilen:** Günlük limit dahilinde tedavi edilen hastaların listesi.
- **Tedavi Edilemeyen:** Tedavi edilemeyen hastaların listesi.
