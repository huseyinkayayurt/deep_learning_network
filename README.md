# Yapay Sinir Ağı Görselleştirme ve Eğitim Arayüzü

Bu proje, yapay sinir ağlarının yapılandırılması, eğitilmesi ve test edilmesi için görsel bir arayüz sunar. Modern ve kullanıcı dostu bir tasarıma sahip olan uygulama, yapay sinir ağı kavramlarını interaktif bir şekilde deneyimlemenizi sağlar.

## Özellikler

- Çok katmanlı yapay sinir ağı oluşturma
- Dinamik katman ve nöron sayısı belirleme
- Ağırlık ve bias değerlerini manuel veya otomatik ayarlama
- Gerçek zamanlı ağ görselleştirme
- Eğitim sürecini görselleştirme
- Loss değeri takibi
- Tahmin sonuçlarını karşılaştırma

## Kurulum

### Gereksinimler

- Python 3.8 veya üzeri
- pip (Python paket yöneticisi)

### Adımlar

1. Projeyi GitHub'dan klonlayın:
```bash
git clone <repo-url>
cd <proje-klasörü>
```

2. Sanal ortam oluşturun (opsiyonel ama önerilen):
```bash
python -m venv venv
```

3. Sanal ortamı aktifleştirin:
- Windows için:
```bash
venv\Scripts\activate
```
- macOS/Linux için:
```bash
source venv/bin/activate
```

4. Gerekli kütüphaneleri yükleyin:
```bash
pip install -r requirements.txt
```

## Kullanım

1. Ana uygulamayı başlatmak için:
```bash
python main.py
```

2. Uygulama başladığında yapmanız gerekenler:
   - Giriş katmanı nöron sayısını belirleyin
   - Gizli katman sayısını belirleyin
   - Çıkış katmanı nöron sayısını belirleyin
   - "Yapılandırmayı Onayla" butonuna tıklayın

3. Gizli katman yapılandırması:
   - Her gizli katman için nöron sayılarını girin
   - "Yapılandırmayı Tamamla" butonuna tıklayın

4. Ağ parametreleri:
   - Ağırlık ve bias değerlerini manuel girin veya
   - "Rastgele Değerler Ata" butonunu kullanın
   - "Parametreleri Onayla" butonuna tıklayın

5. Tahmin ve eğitim:
   - Gerçek Y değerlerini girin
   - Aktivasyon ve loss fonksiyonlarını seçin
   - "Tahmin Et" butonu ile anlık tahmin yapın
   - Eğitim parametrelerini ayarlayın ve eğitimi başlatın

## Proje Yapısı

- `main.py`: Ana uygulama penceresi ve temel UI bileşenleri
- `network_visualizer.py`: Ağ yapısının görsel temsilini oluşturan modül
- `network_parameters.py`: Ağ parametrelerinin yapılandırma arayüzü
- `network_prediction.py`: Tahmin ve eğitim işlemlerinin arayüzü
- `network_functions.py`: Yapay sinir ağı matematiksel işlemleri ve fonksiyonları

## Teknik Detaylar

### Aktivasyon Fonksiyonları
- ReLU (Rectified Linear Unit)

### Loss Fonksiyonları
- MSE (Mean Square Error)

### Ağ Mimarisi
- Tam bağlantılı (fully connected) katmanlar
- Xavier/Glorot başlangıç ağırlık ataması
- Bias değerleri için küçük pozitif başlangıç değerleri

### Eğitim
- Batch gradient descent
- Ayarlanabilir öğrenme oranı
- Epoch bazlı eğitim takibi
- Gerçek zamanlı loss grafiği

## Hata Giderme

1. GUI başlatma hatası:
   - tkinter kurulumunu kontrol edin
   - Python sürümünün uyumlu olduğundan emin olun

2. Matplotlib hatası:
   - Backend ayarlarının doğru olduğundan emin olun
   - macOS kullanıcıları için: `matplotlib.use('TkAgg')` ayarı otomatik yapılmaktadır

3. Bellek hatası:
   - Çok büyük ağ yapıları oluşturmaktan kaçının
   - Sistem RAM'inizin yeterli olduğundan emin olun

## Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/AmazingFeature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add some AmazingFeature'`)
4. Branch'inizi push edin (`git push origin feature/AmazingFeature`)
5. Pull Request oluşturun

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakın. 