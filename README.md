# Yapay Sinir Ağı Simülatörü

Bu proje, yapay sinir ağlarının çalışma prensiplerini görselleştirmek ve anlamak için geliştirilmiş bir simülasyon aracıdır.

## Özellikler

- Çok katmanlı yapay sinir ağı simülasyonu
- Görsel ağ yapısı gösterimi
- Gerçek zamanlı eğitim ve tahmin
- Eğitim sürecinin görselleştirilmesi
- Loss değeri grafiği
- Parametrelerin detaylı gösterimi

### Aktivasyon Fonksiyonları

Simülatör iki farklı aktivasyon fonksiyonu sunar:

1. **ReLU (Rectified Linear Unit)**
   - f(x) = max(0, x)
   - Gradyan problemi yaşamaz
   - Hızlı hesaplama
   - Seyrek aktivasyon özelliği

2. **Sigmoid**
   - f(x) = 1 / (1 + e^(-x))
   - Çıktıyı [0,1] aralığına sıkıştırır
   - Sınıflandırma problemleri için uygundur
   - Biyolojik nöronlara benzer davranış

### Loss Fonksiyonları

İki farklı loss fonksiyonu mevcuttur:

1. **Mean Square Error (MSE)**
   - Regresyon problemleri için uygundur
   - Tahmin ve gerçek değer arasındaki farkın karesini kullanır
   - Genel amaçlı kullanım için idealdir

2. **Cross Entropy**
   - Sınıflandırma problemleri için optimize edilmiştir
   - Sigmoid aktivasyon fonksiyonu ile mükemmel uyum sağlar
   - Daha iyi gradyan akışı sağlar
   - [0,1] aralığındaki çıktılar için uygundur

## Kurulum

1. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

2. Programı çalıştırın:
```bash
python main.py
```

## Kullanım

1. **Ağ Yapısını Belirleme**
   - Giriş katmanı nöron sayısı
   - Gizli katman sayısı ve her katmandaki nöron sayıları
   - Çıkış katmanı nöron sayısı

2. **Parametreleri Ayarlama**
   - Başlangıç ağırlıkları ve bias değerleri
   - Aktivasyon fonksiyonu seçimi (ReLU veya Sigmoid)
   - Loss fonksiyonu seçimi (MSE veya Cross Entropy)
   - Learning rate ve epoch sayısı

3. **Eğitim ve Tahmin**
   - Gerçek değerleri girin
   - Eğitimi başlatın
   - Loss grafiğini takip edin
   - Güncellenmiş parametreleri inceleyin
   - Tahminleri görüntüleyin

## Öneriler

- Sigmoid aktivasyon fonksiyonu ile Cross Entropy loss fonksiyonunu birlikte kullanmanız önerilir
- ReLU aktivasyonu genel amaçlı kullanım için uygundur
- Learning rate değerini problem özelinde ayarlayın
- Epoch sayısını loss değerinin değişimine göre belirleyin

## Teknik Detaylar

- Python 3.x ile geliştirilmiştir
- Tkinter ve ttkbootstrap ile modern bir arayüz
- Numpy ile matris işlemleri
- Matplotlib ile görselleştirme
- Modüler ve genişletilebilir yapı

## Lisans

Bu proje MIT lisansı altında dağıtılmaktadır. 