# 🧠 MEB Kazanım Botu

Telegram üzerinden öğretmenlerin sınıf ve branş seçimine göre haftalık MEB kazanımlarını gösteren basit bir bot.

> ⚠️ **ÖNEMLİ NOT**: Bu bot **test amaçlı** geliştirilmiştir. Tam müfredat henüz eklenmemiştir ve **eğitilmesi gerekmektedir**. İsteğe göre genişletilebilir veya proje kullanılabilir.

## 🎯 Özellikler

- 📚 **Sınıf Seçimi**: 9, 10, 11, 12. sınıflar
- 🔬 **Branş Seçimi**: Biyoloji, Kimya, Fizik, Matematik
- 📅 **Otomatik Hafta Hesaplama**: Eğitim yılı başlangıcına göre (15 Eylül)
- 📋 **Kazanım Gösterimi**: Haftalık MEB kazanımları
- 🔍 **Manuel Hafta Görüntüleme**: `/hafta` komutu ile belirli haftaları görüntüleme

## 🚀 Kurulum

### Gereksinimler
- Python 3.11+
- Telegram Bot Token

### Adımlar

1. **Repository'yi klonlayın:**
```bash
git clone https://github.com/kayra/mebtg.git
cd mebtg
```

2. **Bağımlılıkları yükleyin:**
```bash
pip install -r requirements.txt
```

3. **Environment dosyasını oluşturun:**
```bash
cp .env.example .env
```

4. **`.env` dosyasını düzenleyin:**
```
TELEGRAM_BOT_TOKEN=your_bot_token_here
```

5. **Botu çalıştırın:**
```bash
python main.py
```

## 🤖 Bot Komutları

- `/start` - Botu başlat ve sınıf seçimi yap
- `/help` - Yardım mesajını göster
- `/hafta <numara>` - Belirli bir haftayı görüntüle (örn: `/hafta 5`)

## 📱 Kullanım

1. Bot ile konuşmaya başlayın (`/start`)
2. Sınıfınızı seçin (9, 10, 11, 12)
3. Branşınızı seçin (Biyoloji, Kimya, Fizik, Matematik)
4. Bot otomatik olarak bu haftanın kazanımını gösterecek

### Örnek Çıktı
```
🗓️ 20–26 Ekim
📘 12. sınıf Biyoloji dersi, 4. hafta
➡️ 12.1.1.4 DNA'nın kendini eşlemesini açıklar.
```

## 📁 Proje Yapısı

```
mebtg/
├── main.py                 # Ana bot kodu
├── data/
│   └── kazanımlar.json    # MEB kazanım verileri
├── requirements.txt        # Python bağımlılıkları
├── .env                   # Environment variables (git'te yok)
├── .gitignore            # Git ignore dosyası
└── README.md             # Bu dosya
```

## 🔧 Teknik Detaylar

- **Framework**: python-telegram-bot v20.3
- **Veri Formatı**: JSON
- **Hafta Hesaplama**: Eğitim yılı başlangıcı (15 Eylül) baz alınarak
- **Kodlama**: UTF-8 (Türkçe karakter desteği)

## 📊 Kazanım Verisi

Kazanımlar `data/kazanımlar.json` dosyasında saklanır. Bu dosya şu yapıda organize edilmiştir:

```json
{
  "Branş": {
    "Sınıf": {
      "Hafta": "Kazanım metni"
    }
  }
}
```

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 📞 İletişim

- **Geliştirici**: Kayra
- **GitHub**: [@kayrademirkan](https://github.com/kayrademirkan)

## 💝 Bağış Yapın

Bu proje açık kaynak olarak geliştirilmiştir. Eğer projeyi beğendiyseniz ve geliştirilmesine katkıda bulunmak istiyorsanız:

- ⭐ **GitHub'da yıldız verin**
- 🍴 **Fork yapın ve katkıda bulunun**
- 🐛 **Hata bildirin**
- 💡 **Önerilerinizi paylaşın**

### 🚀 Proje Geliştirme

Bu bot test amaçlı geliştirilmiştir. Tam müfredatın eklenmesi ve geliştirilmesi için:

- MEB müfredat verilerinin tam olarak eklenmesi
- Daha fazla branş ve sınıf desteği
- Gelişmiş özellikler (PDF çıktı, takvim entegrasyonu vb.)
- Kullanıcı arayüzü iyileştirmeleri

**İsteğe göre proje genişletilebilir ve kullanılabilir!**

## 🙏 Teşekkürler

- MEB (Milli Eğitim Bakanlığı) kazanım verileri için
- python-telegram-bot kütüphanesi için
- Tüm katkıda bulunanlar için

---

⭐ Bu projeyi beğendiyseniz yıldız vermeyi unutmayın!
