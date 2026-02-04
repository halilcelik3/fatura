import os
import sys
import logging
from datetime import datetime

from modul1 import excelden_faturalari_oku
from modul3 import pdflerden_faturalari_oku
from modul4 import excel_pdf_eslestir


# ===============================
# PATH TESPİTİ (EXE + PY UYUMLU)
# ===============================
if getattr(sys, 'frozen', False):
    ana_klasor = os.path.dirname(sys.executable)
else:
    ana_klasor = os.path.dirname(os.path.abspath(__file__))

excel_yolu = os.path.join(ana_klasor, "Fatura Örneklem.xlsx")
pdf_klasoru = os.path.join(ana_klasor, "Pdfler")


# ===============================
# 🔹 SONUC KLASÖRÜ (YENİ)
# ===============================
sonuc_klasoru = os.path.join(ana_klasor, "sonuc")
os.makedirs(sonuc_klasoru, exist_ok=True)


# ===============================
# LOG AYARLARI
# ===============================
log_dosyasi = os.path.join(
    sonuc_klasoru,   # 🔹 artık sonuc içinde
    f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
)

logging.basicConfig(
    filename=log_dosyasi,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


def main():
    print("=== FATURA EŞLEŞTİRME OTOMASYONU BAŞLADI ===")
    logging.info("Otomasyon başlatıldı")

    try:
        # === MODÜL 1 ===
        logging.info("Excel okunuyor")
        df_excel = excelden_faturalari_oku(excel_yolu)
        logging.info(f"Excel kayıt sayısı: {len(df_excel)}")

        # === MODÜL 3 ===
        logging.info("PDF'ler okunuyor")
        df_pdf = pdflerden_faturalari_oku(pdf_klasoru)
        logging.info(f"PDF kayıt sayısı: {len(df_pdf)}")

        # === MODÜL 4 ===
        logging.info("Excel ↔ PDF eşleştirme yapılıyor")
        df_sonuc = excel_pdf_eslestir(df_excel, df_pdf)

        # ===============================
        # 🔹 ÇIKTI (sonuc klasörü)
        # ===============================
        cikti_yolu = os.path.join(
            sonuc_klasoru,
            f"eslestirme_sonucu_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        )

        df_sonuc.to_excel(cikti_yolu, index=False)

        print("✔ Eşleştirme tamamlandı")
        print("✔ Çıktı:", cikti_yolu)

        logging.info("Eşleştirme başarıyla tamamlandı")
        logging.info(f"Çıktı dosyası: {cikti_yolu}")

    except Exception as e:
        print("❌ KRİTİK HATA:", e)
        logging.exception("KRİTİK HATA OLUŞTU")
        sys.exit(1)

    print("=== OTOMASYON TAMAMLANDI ===")
    print("Log dosyası:", log_dosyasi)
    logging.info("Otomasyon tamamlandı")


if __name__ == "__main__":
    main()
