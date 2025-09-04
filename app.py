import gspread
import translators as ts
import httpx
from gspread.utils import rowcol_to_a1
import time

gc = gspread.oauth(
    credentials_filename='credentials.json',
    authorized_user_filename='authorized_user.json'
)

start_time = time.time()

sh = gc.open("Grillin it")
worksheet = sh.sheet1

key_txts = worksheet.col_values(1)[1:]
delimiter = " ||| "
joined_keys = delimiter.join(key_txts)
# print(joined_keys)
languages = [lang[-3:-1] for lang in worksheet.row_values(1)[1:]] # extract language codes

for i in range(len(languages)):
    if languages[i] == "en": # skip translate en to en
        continue

    translated_keys = ts.translate_text(
        joined_keys,
        from_language="en",
        to_language=languages[i],
        translator="bing",
        http_client="httpx"
    )

    #split into 2d array strings
    translated_list = translated_keys.split(delimiter)
    lang_col = [[t] for t in translated_list]

    start = rowcol_to_a1(2, i+2)                 
    end = rowcol_to_a1(len(key_txts) + 1, i+2)   
    worksheet.update(range_name=f"{start}:{end}", values=lang_col)

end_time = time.time()
print(f"Time taken: {end_time - start_time} seconds")
