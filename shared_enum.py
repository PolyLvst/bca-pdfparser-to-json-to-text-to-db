class Pattern:
    AMOUNT_PATTERN = r'\b\d{1,3}(,\d{3})*\.\d{2}\b'
    DATE_PATTERN = r'^(0[1-9]|[12][0-9]|3[01])\/(0[1-9]|1[0-2])$'
    SALDO_AWAL = "SALDO AWAL"

class Transaction:
    ADD = "balance + amount"
    SUB = "balance - amount"
    INIT = "balance"
    TYPES = {
        "SALDO AWAL": INIT,
        "TRSF E-BANKING CR": ADD,
        "BUNGA": ADD,
        "BI-FAST CR": ADD,
        "TRSF E-BANKING DB": SUB,
        "KARTU KREDIT/PL": SUB,
        "BIAYA ADM": SUB,
        "PAJAK BUNGA": SUB
    }