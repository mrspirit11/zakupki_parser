from zakupki_parser import  parse_api, to_html, get_date_from
import rkgovru_parser, ed_sevas
import pandas

# Выгрузка Крым, Севастополь 
krym_sevas_30kk = parse_api({"af": "on",
                             "pa": "on",
                             "pc": "on",
                             "ca": "on",
                             "fz44": "on", 
                             "fz223": "on", 
                             "ppRf615": "on",
                             'updateDateFrom': get_date_from(),
                             "delKladrIds": "8408974, 8408975",
                             "priceFromGeneral": 30000000})

sev_gu = parse_api({"af": "on",
                    "pa": "on", 
                    "pc": "on",
                    "ca": "on",
                    'updateDateFrom': get_date_from(),
                    "customerInn": "9201012877"})

out_list = krym_sevas_30kk.get_full_data() + sev_gu.get_full_data()

# df = pandas.DataFrame(out_list)
# df.to_excel(f'{get_date_from()}.xlsx')

with open('krym_sevas.html', 'w') as f_out:
    f_out.write(to_html(out_list))

# Выгрузка ед поставщик Крым с rk.gov.ru
try:
    rkgovru_parser.download_all_pdf(rkgovru_parser.get_doc_list('all'))

    with open('rk_gov_ru.html', 'w') as f_out:
        f_out.write(rkgovru_parser.to_html(rkgovru_parser.get_text_from_pdf()))
except Exception as e:
    print(e)
    
# Выгрузка ед поставщик Севастополь из реестра контрактов
ed_sevas.main()
