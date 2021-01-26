from zakupki_parser import  parse_api, to_html, get_date_from
import rkgovru_parser
import pandas

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

rkgovru_parser.download_all_pdf(rkgovru_parser.get_doc_list(1))
with open('test_rk.html', 'w') as f_out:
    f_out.write(rkgovru_parser.to_html(rkgovru_parser.get_text_from_pdf()))