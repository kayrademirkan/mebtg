# 🧠 Telegram Öğretmen Kazanım Botu

## 🎯 Amaç
Öğretmenlerin Telegram üzerinden haftalık MEB kazanımlarını kolayca görmesini sağlayan bir bot yapılacak.

Kullanıcı akışı:
1. /start komutu ile başlar.
2. Hoca sınıfını seçer (örnek: 9, 10, 11, 12).
3. Ardından branşını seçer (örnek: Biyoloji, Kimya, Fizik, Matematik).
4. Bot, otomatik olarak bugünkü tarihe bakar.
5. Tarihe göre o haftanın aralığını (örnek: 20–26 Ekim) ve hafta numarasını belirler.
6. JSON dosyasındaki uygun kazanımı bulur ve aşağıdaki gibi yanıt verir:

```
🗕 20–26 Ekim  
📘 12. sınıf Biyoloji dersi, 4. hafta  
➡️ 12.1.1.4 DNA'nın kendini eşlemesini açıklar.
```

---

## ⚙️ Teknolojiler
- Python 3.11+
- python-telegram-bot (v20.3)
- JSON veri dosyası (`data/kazanımlar.json`)

---

## 📁 Proje Yapısı
```
teacher-learning-bot/
├── main.py
├── data/
│   └── kazanımlar.json
├── requirements.txt
├── README.md
└── .env  (Telegram bot token burada)
```

---

## 📘 `data/kazanımlar.json` Örneği
```json
{
  "Biyoloji": {
    "12": {
      "4": "12.1.1.4 DNA'nın kendini eşlemesini açıklar.",
      "5": "12.1.1.5 Protein sentezinin aşamalarını açıklar."
    },
    "11": {
      "4": "11.1.1.4 Fotosentezin önemini açıklar."
    }
  },
  "Kimya": {
    "12": {
      "4": "12.2.1.4 Elektrokimya uygulamalarını örneklerle açıklar."
    }
  }
}
```

---

## 🤉 Gereksinimler
`requirements.txt` içeriği:
```
python-telegram-bot==20.3
python-dotenv
```

---

## 🐍 Yapılacaklar
1. `main.py` içinde Telegram botu kurulacak.
2. /start → sınıf seçimi (ReplyKeyboardMarkup ile)
3. Ardından branş seçimi
4. Günün tarihine göre haftayı hesapla (Eylül 15 → 1. hafta kabul)
5. JSON’dan ilgili haftanın kazanımını çek
6. Bot, yukarıdaki örnek formatta kullanıcıya mesaj göndersin.
7. Token `.env` dosyasından okunacak.
8. Bot başlatıldığında terminalde “Bot aktif 🚀” yazsın.

---

## 🧾 README.md İçeriği
```markdown
# 🧠 Öğretmen Kazanım Botu

Telegram üzerinden öğretmenlerin sınıf ve branş seçimine göre haftalık MEB kazanımlarını gösteren basit bir bot.

## Kurulum
```bash
pip install -r requirements.txt
python main.py
```

`.env` dosyasına kendi Telegram bot token'ınızı ekleyin:
```
TELEGRAM_BOT_TOKEN=xxxxxxxxxxxxxxxx
```
```

---

## 💡 Ekstra İyileştirmeler
- `/hafta 5` komutu → belirli haftayı manuel görüntüleme
- `/arama dna` → kavram arama
- Haftalık özet PDF veya tablo gönderimi (ileride)

---

## 🌟 İstek
Bu tanıma göre:
- Basit ama çalışır bir Telegram botu oluştur.
- `main.py`, `requirements.txt`, `README.md`, ve `data/kazanımlar.json` dosyaları dahil olsun.
- Kod temiz, açıklamalı ve direkt çalışabilir şekilde olsun.