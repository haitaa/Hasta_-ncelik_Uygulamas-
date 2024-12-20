from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
import heapq

app = FastAPI()

class Hasta:
    def __init__(self, id, oncelik, sure):
        self.id = id
        self.oncelik = oncelik
        self.sure = sure

    def __lt__(self, other):
        if self.oncelik == other.oncelik:
            return self.sure < other.sure  # Öncelik eşitse, süreye göre sıralama
        return self.oncelik < other.oncelik  # Öncelik küçükse, önceki hasta seçilir


class HastaneAcilServis:
    def __init__(self):
        self.heap = []
        self.toplam_sure = 0
        self.gun_limit = 420  # 7 saatlik limit (dakika cinsinden)
        self.tedavi_edilenler = []
        self.tedavi_edilemeyenler = []

    def heap_olustur(self, hastalar):
        for hasta in hastalar:
            heapq.heappush(self.heap, hasta)

    def hasta_ekle(self, id, oncelik, sure):
        yeni_hasta = Hasta(id, oncelik, sure)
        heapq.heappush(self.heap, yeni_hasta)
        
        # Dosyaya da yeni hasta ekleme
        with open("input.txt", "a") as file:
            file.write(f"{yeni_hasta.id},{yeni_hasta.oncelik},{yeni_hasta.sure}\n")

    def tedavi_simulasyonu(self):
        while self.heap and self.toplam_sure + self.heap[0].sure <= self.gun_limit:
            hasta = heapq.heappop(self.heap)
            self.toplam_sure += hasta.sure
            self.tedavi_edilenler.append(hasta)

        while self.heap:
            self.tedavi_edilemeyenler.append(heapq.heappop(self.heap))

    def raporla(self):
        heap_sirasi = [
            {"HastaID": hasta.id, "Oncelik": hasta.oncelik, "Sure": hasta.sure}
            for hasta in self.heap
        ]
        tedavi_edilenler = [
            {"HastaID": hasta.id, "Oncelik": hasta.oncelik, "Sure": hasta.sure}
            for hasta in self.tedavi_edilenler
        ]
        tedavi_edilemeyenler = [
            {"HastaID": hasta.id, "Oncelik": hasta.oncelik, "Sure": hasta.sure}
            for hasta in self.tedavi_edilemeyenler
        ]
        return {
            "Heap Sırası": heap_sirasi,
            "Tedavi Edilen": tedavi_edilenler,
            "Tedavi Edilemeyen": tedavi_edilemeyenler,
        }

    def dosya_giris(self, dosya_yolu):
        try:
            with open(dosya_yolu, "r") as file:
                hastalar = []
                for line in file.readlines():
                    parts = line.strip().split(',')
                    id, oncelik, sure = map(int, parts)
                    hastalar.append(Hasta(id, oncelik, sure))
                self.heap_olustur(hastalar)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Dosya okuma hatası: {str(e)}")

    def dosya_cikis(self, dosya_yolu):
        try:
            with open(dosya_yolu, "w") as file:
                file.write("Tedavi Edilen Hastalar:\n")
                for hasta in self.tedavi_edilenler:
                    file.write(f"Hasta ID: {hasta.id}, Öncelik: {hasta.oncelik}, Süre: {hasta.sure} dakikalar\n")
                file.write("\nTedavi Edilemeyen Hastalar:\n")
                for hasta in self.tedavi_edilemeyenler:
                    file.write(f"Hasta ID: {hasta.id}, Öncelik: {hasta.oncelik}, Süre: {hasta.sure} dakikalar\n")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Dosya yazma hatası: {str(e)}")

    def dosya_baslangic_verileri(self, dosya_yolu):
        try:
            with open(dosya_yolu, "w") as file:
                baslangic_hastalar = [
                    Hasta(101, 5, 30),
                    Hasta(102, 3, 40),
                    Hasta(103, 8, 20),
                    Hasta(104, 1, 60),
                    Hasta(105, 7, 15),
                    Hasta(106, 2, 50),
                    Hasta(107, 4, 45),
                    Hasta(108, 6, 25),
                    Hasta(109, 3, 35),
                    Hasta(110, 2, 30),
                    Hasta(111, 8, 10)
                ]
                for hasta in baslangic_hastalar:
                    file.write(f"{hasta.id},{hasta.oncelik},{hasta.sure}\n")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Başlangıç verilerini dosyaya yazma hatası: {str(e)}")

# Simülasyon sınıfı
tedavi_servis = HastaneAcilServis()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def anasayfa(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/hasta-ekle")
def hasta_ekle(request: Request, id: int = Form(...), oncelik: int = Form(...), sure: int = Form(...)):
    try:
        tedavi_servis.hasta_ekle(id, oncelik, sure)
        return templates.TemplateResponse("index.html", {"request": request, "message": "Hasta başarıyla eklendi."})
    except Exception as e:
        return templates.TemplateResponse("index.html", {"request": request, "message": f"Hata: {str(e)}"})

@app.post("/simulasyon")
def simulasyon(request: Request):
    try:
        tedavi_servis.tedavi_simulasyonu()
        rapor = tedavi_servis.raporla()
        tedavi_servis.dosya_cikis("output.txt")  # Simülasyon sonucu çıktıyı dosyaya yaz
        return templates.TemplateResponse("index.html", {"request": request, "rapor": rapor})
    except Exception as e:
        return templates.TemplateResponse("index.html", {"request": request, "message": f"Hata: {str(e)}"})
