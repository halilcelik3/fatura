import re


def temiz_tutar(tutar_str):
    """
    4.950.660,00 -> 4950660.00 (float)
    """
    if not tutar_str:
        return None
    return float(tutar_str.replace(".", "").replace(",", "."))


def toplam_tutar_bul(text):
    """
    Mal / Hizmet / Ürün / Hizmet / Mal ve Hizmet
    Toplam Tutarı yakalar (mevcut sistemi bozmadan genişletilmiş)
    """

    pattern = re.compile(
        r"("
        r"Mal\s*(/|ve)?\s*Hizmet\s*Toplam\s*Tutarı|"
        r"Ürün\s*(/|ve)?\s*Hizmet\s*Toplam\s*Tutarı"
        r")"
        r"[^\d]*([\d\.\,]+)\s*TL?",
        re.IGNORECASE
    )

    match = pattern.search(text)
    if match:
        return temiz_tutar(match.group(4))

    return None


def fatura_bilgilerini_al(text):
    """
    PDF içinden:
    - Fatura No (toplam 16 haneli, harf + rakam)
    - Fatura Tarihi
    - Toplam Tutar
    alır
    """

    sonuc = {
        "fatura_no": None,
        "fatura_tarihi": None,
        "toplam_tutar": None
    }

    # 🔹 FATURA NO (HARF + RAKAM, TOPLAM 16 KARAKTER)
    fatura_no_eslesme = re.search(
        r"Fatura\s*No\s*[:\-]?\s*([A-Z0-9]+)",
        text,
        re.IGNORECASE
    )

    if fatura_no_eslesme:
        aday = fatura_no_eslesme.group(1).strip()
        if len(aday) == 16:
            sonuc["fatura_no"] = aday

    # 🔹 FATURA TARİHİ (mevcut yapı korunuyor)
    tarih = re.search(
        r"Fatura\s*Tarihi\s*[:\-]?\s*([0-9]{2}[\/\-\s][0-9]{2}[\/\-\s][0-9]{4})",
        text
    )
    if tarih:
        sonuc["fatura_tarihi"] = tarih.group(1)

    # 🔹 TOPLAM TUTAR
    sonuc["toplam_tutar"] = toplam_tutar_bul(text)

    return sonuc
