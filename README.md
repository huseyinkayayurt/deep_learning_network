# Yapay Sinir Ağı Simülatörü

Bu proje, yapay sinir ağlarının (YSA) temel prensiplerini görselleştirmek, eğitim ve tahmin süreçlerini adım adım
deneyimlemek için geliştirilmiş modern bir simülasyon uygulamasıdır.

---

## Kurulum ve Çalıştırma

### 1. Python Kurulumu

- Python 3.8 veya üzeri bir sürüm gereklidir.
- [Python İndir](https://www.python.org/downloads/)

### 2. Bağımlılıkların Yüklenmesi

Aşağıdaki komut ile gerekli tüm kütüphaneleri yükleyin:

```bash
pip install -r requirements.txt
```

> **Not:** Tkinter çoğu Python dağıtımında dahili gelir. Eğer Linux/Mac kullanıyorsanız ve Tkinter yüklü değilse:
> - **Linux:** `sudo apt-get install python3-tk`
> - **Mac:** `brew install python-tk@3.8`

### 3. Projeyi Çalıştırma

```bash
python main.py
```

---

## Uygulama Akışı ve Pencereler

### 1. Ağ Yapılandırma Penceresi

- **Amaç:** Ağın katman sayısı, giriş/çıkış/gizli katman nöron sayıları gibi temel mimariyi belirlemek.
- **Kullanıcıdan Beklenen:**
    - Giriş katmanı nöron sayısı
    - Gizli katman sayısı ve her birinin nöron sayısı
    - Çıkış katmanı nöron sayısı
    - "Devam" ile bir sonraki adıma geçiş

### 2. Ağ Parametreleri Penceresi

- **Amaç:** Kullanıcıdan ağırlıklar, biaslar ve giriş değerlerinin manuel veya rastgele girilmesi.
- **Kullanıcıdan Beklenen:**
    - Her nöron için giriş değeri
    - Her katman için bias değerleri
    - Katmanlar arası ağırlık matrisleri
    - "Rastgele Ata" ile otomatik değer üretme
    - "Temizle" ile sıfırlama
    - "Parametreleri Onayla" ile devam

### 3. Tahmin ve Eğitim Penceresi

- **Amaç:**
    - Aktivasyon ve loss fonksiyonu seçimi
    - Gerçek değerlerin girilmesi
    - Eğitim parametrelerinin (epoch, learning rate) ayarlanması
    - Eğitimi başlatma ve loss grafiğini izleme
    - Tahmin sonuçlarını ve loss değerini görme
- **Kullanıcıdan Beklenen:**
    - Aktivasyon fonksiyonu seçimi (ReLU, Sigmoid)
    - Loss fonksiyonu seçimi (MSE, Cross Entropy)
    - Gerçek çıkış değerlerinin girilmesi
    - Epoch ve learning rate ayarlanması
    - "Eğitimi Başlat" ile eğitim sürecini başlatma
    - "Tahmin Et" ile güncel ağı kullanarak tahmin yapma
    - "Karşılaştırmayı Göster" ile tahmin ve gerçek değerleri karşılaştırma

### 4. Eğitim Sonrası Güncellenmiş Parametreler Penceresi

- **Amaç:** Eğitim tamamlandıktan sonra güncellenmiş ağırlık ve bias değerlerini detaylı ve scrollable bir ekranda
  göstermek.
- **Kullanıcıdan Beklenen:**
    - Tüm parametreleri inceleyebilmek için pencereyi kaydırmak (scroll)
    - Pencereyi kapatmak için "Kapat" butonunu kullanmak

---

## Aktivasyon ve Loss Fonksiyonları

- **Aktivasyon Fonksiyonları:**
    - ReLU (Rectified Linear Unit)
    - Sigmoid
- **Loss Fonksiyonları:**
    - Mean Square Error (MSE)
    - Cross Entropy

## Lisans

Bu proje MIT lisansı ile açık kaynak olarak sunulmaktadır. 