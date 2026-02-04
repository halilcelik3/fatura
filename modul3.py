import os
import pdfplumber
import pandas as pd
from modul2 import fatura_bilgilerini_al

# === MODÜL 3: PDF -> TEXT -> MODÜL 2 ===

def pdflerden_faturalari_oku(pdf_klasoru):
    """
    PDF klasöründen:
    - fatura_no
    - toplam_tutar
    bilgilerini okur ve DataFrame döner
    """

    sonuclar = []

    for dosya in os.listdir(pdf_klasoru):
        if dosya.lower().endswith(".pdf"):
            pdf_yolu = os.path.join(pdf_klasoru, dosya)

            try:
                with pdfplumber.open(pdf_yolu) as pdf:
                    tam_metin = ""
                    for sayfa in pdf.pages:
                        sayfa_metin = sayfa.extract_text()
                        if sayfa_metin:
                            tam_metin += sayfa_metin + "\n"

                bilgi = fatura_bilgilerini_al(tam_metin)

                sonuc = {
                    "dosya": dosya,
                    "fatura_no": bilgi.get("fatura_no"),
                    "toplam_tutar": bilgi.get("toplam_tutar")
                }

                sonuclar.append(sonuc)

            except Exception as e:
                sonuclar.append({
                    "dosya": dosya,
                    "fatura_no": None,
                    "toplam_tutar": None,
                    "hata": str(e)
                })

    return pd.DataFrame(sonuclar)
