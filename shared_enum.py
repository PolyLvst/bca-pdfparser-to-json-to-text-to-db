class Pattern:
    AMOUNT_PATTERN = r'\b\d{1,3}(,\d{3})*\.\d{2}\b'
    DATE_PATTERN = r'^(0[1-9]|[12][0-9]|3[01])\/(0[1-9]|1[0-2])$'
    SALDO_AWAL = "SALDO AWAL"
    YEAR_PATTERN = r"\b\d{4}\b" # 1000 - 9999 / 1999 - 2025
    ACCOUNT_NUMBER_PATTERN = r"\b\d{10}\b" # 1234567890
    BERSAMBUNG = r"(?i)Bersambung ke Halaman berikut"

class Transaction:
    ADD = "balance + amount"
    SUB = "balance - amount"
    INIT = "balance"
    TYPES = {
        "SALDO AWAL": INIT,
        "TRSF E-BANKING CR": ADD,
        "BUNGA": ADD,
        "BI-FAST CR": ADD,
        "SWITCHING CR": ADD,
        "KR OTOMATIS": ADD,
        "CR KOREKSI BUNGA": ADD,
        "KARTU KREDIT": ADD,
        "TRSF E-BANKING DB": SUB,
        "KARTU KREDIT/PL": SUB,
        "BIAYA ADM": SUB,
        "PAJAK BUNGA": SUB,
        "BYR VIA E-BANKING": SUB,
        "TARIKAN TUNAI": SUB,
        "BI-FAST DB": SUB,
        "SWITCHING DB": SUB,
        "KARTU DEBIT": SUB,
        "TARIKAN ATM": SUB,
        "TRANSAKSI DEBIT": SUB,
        "DB DEBIT": SUB,
        "BA JASA E-BANKING": SUB,
    }