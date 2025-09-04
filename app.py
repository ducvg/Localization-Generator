import gspread
import translators as ts
from gspread.utils import rowcol_to_a1

gc = gspread.oauth(
    credentials_filename='credentials.json',
    authorized_user_filename='authorized_user.json'
)

sh = gc.open("Grillin it")
worksheet = sh.sheet1

key_txts = worksheet.col_values(1)[1:]
languages = [lang[-3:-1] for lang in worksheet.row_values(1)[1:]]

all_translations = []

for lang in languages:
    if lang == "en":
        all_translations.append(key_txts)
        continue

    translated_list = []
    for j, text in enumerate(key_txts, start=2):
        translated = ts.translate_text(
            text,
            from_language="en",
            to_language=lang,
            translator="google"
        )
        translated_list.append(translated)

    all_translations.append(translated_list)

# Rotate cols → rows
rows = list(zip(*all_translations))

# Bulk update once
start = "B2"
end = rowcol_to_a1(len(key_txts)+1, len(languages)+1)
worksheet.update(f"{start}:{end}", rows)
