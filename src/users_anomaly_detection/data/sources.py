"""Mapa das fontes de log do CERT r4.2: arquivo, colunas úteis e validações."""

LOG_COLUMNS = {
    "logon": ["date", "user", "pc", "activity"],
    "device": ["date", "user", "pc", "activity"],
    "http": ["date", "user", "pc", "url"],
    "email": ["date", "user", "pc", "from", "to", "cc", "bcc", "size", "attachments"],
    "file": ["date", "user", "pc", "filename"],
}

# Conjuntos de valores válidos onde existem
VALID_ACTIVITIES = {
    "logon": {"Logon", "Logoff"},
    "device": {"Connect", "Disconnect"},
}
