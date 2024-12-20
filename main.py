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

# Simülasyon sınıfı
tedavi_servis = HastaneAcilServis()

#Başlangıç hasta listesi
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

tedavi_servis.heap_olustur(baslangic_hastalar)

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
        return templates.TemplateResponse("index.html", {"request": request, "rapor": rapor})
    except Exception as e:
        return templates.TemplateResponse("index.html", {"request": request, "message": f"Hata: {str(e)}"})
