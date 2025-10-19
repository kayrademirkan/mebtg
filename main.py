#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram Öğretmen Kazanım Botu
MEB kazanımlarını haftalık olarak gösteren Telegram botu
"""

import json
import os
import logging
from datetime import datetime, timedelta
from typing import Dict, Any

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# Logging ayarları
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Environment variables yükle
load_dotenv()

# Global değişkenler
USER_DATA = {}  # Kullanıcı verilerini saklamak için

class KazanimBot:
    def __init__(self):
        self.kazanimlar = self.load_kazanimlar()
        
    def load_kazanimlar(self) -> Dict[str, Any]:
        """JSON dosyasından kazanımları yükler"""
        try:
            with open('data/kazanımlar.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error("kazanımlar.json dosyası bulunamadı!")
            return {}
        except json.JSONDecodeError:
            logger.error("JSON dosyası geçersiz!")
            return {}
    
    def get_week_number(self, date: datetime) -> int:
        """Verilen tarihin hangi hafta olduğunu hesaplar (Eylül 15 = 1. hafta)"""
        # Eğitim yılı başlangıcı: 15 Eylül
        year = date.year
        if date.month < 9 or (date.month == 9 and date.day < 15):
            year -= 1
            
        education_start = datetime(year, 9, 15)
        days_diff = (date - education_start).days
        
        if days_diff < 0:
            # Geçen yılın son haftaları
            return 1
            
        week_number = (days_diff // 7) + 1
        
        # Maksimum 40 hafta (bir eğitim yılı)
        return min(week_number, 40)
    
    def get_week_range(self, date: datetime) -> str:
        """Verilen tarihin hafta aralığını döndürür"""
        week_start = date - timedelta(days=date.weekday())
        week_end = week_start + timedelta(days=6)
        
        return f"{week_start.day}–{week_end.day} {self.get_month_name(week_start.month)}"
    
    def get_month_name(self, month: int) -> str:
        """Ay numarasını Türkçe ay adına çevirir"""
        months = {
            1: "Ocak", 2: "Şubat", 3: "Mart", 4: "Nisan",
            5: "Mayıs", 6: "Haziran", 7: "Temmuz", 8: "Ağustos",
            9: "Eylül", 10: "Ekim", 11: "Kasım", 12: "Aralık"
        }
        return months.get(month, "")
    
    def get_kazanim(self, sinif: str, brans: str, hafta: int) -> str:
        """Belirtilen sınıf, branş ve hafta için kazanımı döndürür"""
        try:
            if brans in self.kazanimlar and sinif in self.kazanimlar[brans]:
                kazanimlar = self.kazanimlar[brans][sinif]
                if str(hafta) in kazanimlar:
                    return kazanimlar[str(hafta)]
                else:
                    return f"Bu hafta için {brans} dersi kazanımı bulunamadı."
            else:
                return f"{brans} dersi için {sinif}. sınıf kazanımları bulunamadı."
        except Exception as e:
            logger.error(f"Kazanım alınırken hata: {e}")
            return "Kazanım alınırken bir hata oluştu."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Bot başlatma komutu"""
    user_id = update.effective_user.id
    USER_DATA[user_id] = {}
    
    # Sınıf seçimi klavyesi
    keyboard = [
        ['9', '10'],
        ['11', '12']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    
    await update.message.reply_text(
        "🎓 **MEB Kazanım Botu'na Hoş Geldiniz!**\n\n"
        "Bu bot ile haftalık MEB kazanımlarınızı kolayca görebilirsiniz.\n\n"
        "📚 Önce sınıfınızı seçin:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def handle_class_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sınıf seçimi işlemi"""
    user_id = update.effective_user.id
    sinif = update.message.text
    
    if sinif not in ['9', '10', '11', '12']:
        await update.message.reply_text("Lütfen geçerli bir sınıf seçin (9, 10, 11, 12)")
        return
    
    USER_DATA[user_id]['sinif'] = sinif
    
    # Branş seçimi klavyesi
    keyboard = [
        ['Biyoloji', 'Kimya'],
        ['Fizik', 'Matematik']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    
    await update.message.reply_text(
        f"✅ {sinif}. sınıf seçildi!\n\n"
        "📖 Şimdi branşınızı seçin:",
        reply_markup=reply_markup
    )

async def handle_subject_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Branş seçimi ve kazanım gösterimi"""
    user_id = update.effective_user.id
    brans = update.message.text
    
    if brans not in ['Biyoloji', 'Kimya', 'Fizik', 'Matematik']:
        await update.message.reply_text("Lütfen geçerli bir branş seçin")
        return
    
    if user_id not in USER_DATA or 'sinif' not in USER_DATA[user_id]:
        await update.message.reply_text("Önce sınıfınızı seçmelisiniz. /start komutu ile başlayın.")
        return
    
    sinif = USER_DATA[user_id]['sinif']
    USER_DATA[user_id]['brans'] = brans
    
    # Bot instance oluştur
    bot = KazanimBot()
    
    # Bugünün tarihi
    today = datetime.now()
    hafta = bot.get_week_number(today)
    hafta_araligi = bot.get_week_range(today)
    
    # Kazanımı al
    kazanim = bot.get_kazanim(sinif, brans, hafta)
    
    # Mesajı formatla
    message = (
        f"🗓️ **{hafta_araligi}**\n"
        f"📘 **{sinif}. sınıf {brans} dersi, {hafta}. hafta**\n"
        f"➡️ {kazanim}"
    )
    
    await update.message.reply_text(
        message,
        reply_markup=ReplyKeyboardRemove(),
        parse_mode='Markdown'
    )
    
    # Tekrar başlatma seçeneği
    keyboard = [['🔄 Yeniden Başlat']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    
    await update.message.reply_text(
        "Başka bir sınıf/branş için tekrar başlamak ister misiniz?",
        reply_markup=reply_markup
    )

async def handle_restart(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Yeniden başlatma işlemi"""
    if update.message.text == "🔄 Yeniden Başlat":
        await start(update, context)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Yardım komutu"""
    help_text = (
        "🤖 **MEB Kazanım Botu Yardım**\n\n"
        "📋 **Komutlar:**\n"
        "• /start - Botu başlat\n"
        "• /help - Bu yardım mesajını göster\n"
        "• /hafta <numara> - Belirli bir haftayı görüntüle\n\n"
        "📚 **Nasıl Kullanılır:**\n"
        "1. /start komutu ile başlayın\n"
        "2. Sınıfınızı seçin (9, 10, 11, 12)\n"
        "3. Branşınızı seçin (Biyoloji, Kimya, Fizik, Matematik)\n"
        "4. Bot otomatik olarak bu haftanın kazanımını gösterecek\n\n"
        "📅 **Hafta Hesaplama:**\n"
        "Bot, eğitim yılının başlangıcını (15 Eylül) baz alarak hafta numarasını hesaplar."
    )
    
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def week_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Belirli hafta görüntüleme komutu"""
    user_id = update.effective_user.id
    
    if user_id not in USER_DATA or 'sinif' not in USER_DATA[user_id] or 'brans' not in USER_DATA[user_id]:
        await update.message.reply_text(
            "Önce sınıf ve branşınızı seçmelisiniz. /start komutu ile başlayın."
        )
        return
    
    try:
        hafta_numara = int(context.args[0]) if context.args else None
        
        if not hafta_numara or hafta_numara < 1 or hafta_numara > 40:
            await update.message.reply_text(
                "Lütfen geçerli bir hafta numarası girin (1-40 arası).\n"
                "Örnek: /hafta 5"
            )
            return
        
        sinif = USER_DATA[user_id]['sinif']
        brans = USER_DATA[user_id]['brans']
        
        # Bot instance oluştur
        bot = KazanimBot()
        
        # Kazanımı al
        kazanim = bot.get_kazanim(sinif, brans, hafta_numara)
        
        # Mesajı formatla
        message = (
            f"📘 **{sinif}. sınıf {brans} dersi, {hafta_numara}. hafta**\n"
            f"➡️ {kazanim}"
        )
        
        await update.message.reply_text(message, parse_mode='Markdown')
        
    except (ValueError, IndexError):
        await update.message.reply_text(
            "Lütfen geçerli bir hafta numarası girin.\n"
            "Örnek: /hafta 5"
        )

def main() -> None:
    """Ana fonksiyon"""
    # Bot token'ını al
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        logger.error("TELEGRAM_BOT_TOKEN environment variable bulunamadı!")
        return
    
    # Application oluştur
    application = Application.builder().token(token).build()
    
    # Handler'ları ekle
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("hafta", week_command))
    
    # Mesaj handler'ları
    application.add_handler(MessageHandler(filters.Regex(r'^(9|10|11|12)$'), handle_class_selection))
    application.add_handler(MessageHandler(filters.Regex(r'^(Biyoloji|Kimya|Fizik|Matematik)$'), handle_subject_selection))
    application.add_handler(MessageHandler(filters.Regex(r'^🔄 Yeniden Başlat$'), handle_restart))
    
    # Bot'u başlat
    print("Bot aktif 🚀")
    logger.info("Bot başlatıldı")
    
    # Polling başlat
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
