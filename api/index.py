from flask import Flask, request, jsonify
import requests
import re

app = Flask(__name__)

def extract_text(text):
    pattern = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]+')
    matches = pattern.findall(text)
    return ' '.join(matches) if matches else "No response text found"

@app.route('/check_visa', methods=['GET'])
def check_visa():
    visa_data = request.args.get('visa')
    
    if not visa_data:
        return jsonify({'error': 'Please provide visa data in format: card|month|year|cvv'}), 400
    
    try:
        card_number, month, year, cvv = visa_data.split('|')
    except ValueError:
        return jsonify({'error': 'Invalid format. Use: card|month|year|cvv'}), 400
    
    cookies = {
        'OTZ': '8178671_44_48_171240_44_319500',
        '__Secure-ENID': '28.SE=PTeBA7BBHK3_SWp8A8QwkyWQ0NV2M6jrKe4lof9MMpzxuICErWtDvATtFm8rd7U0aB9yGNxZ2IMXzWRtIEIUkioKphf4htJA97i0z7zmJpFdJDGz_Cu0LuTfmIvOuPfAO9PoSmjDcSglULgqp1EtEktt0JCd2Y6DpQMXh9DAuDhkHeYs_Om9WJOx5ZYM--O_IlAUF5En',
        'AEC': 'AVh_V2heWGGWR6RJaCA3moYCqStgFwI4jiCbc15w80TlB4YShHtN3EFoH7M',
        'NID': '525=ikO_se4-1r-FYmWnCcNNAtdDGChW-nZpocwBnz1oVOo4CnXpYC_JmmXTzUbo1j8k6Hcd-C2m_fDyr_sqJqGBPniwnOQdNyj2To8Zs7ZNyDhqJuW1iVVY71GuqSbgdXEVUf1PqcpEnyxIMhspDyLzlLaFFkV3xC6p7UtpBYcS9z8WXM4dCtlPc51DtxWDXU-AGnVCGngSK3YoWPlauUFPDzkkmu4yA5q4ZA9otV4ehKGN7gJwUbd7IuDpa1RYcXzWXacJjebE3Bv3ShnDFtPGJw7IRi5CZ5ZQWpF82wMCX1Eg4ezjNjeEJLsL94w8KziSHNVHYt-FYUyQo_taQGUlqhUr7CE2vfrK4jcYcwzi0uS_18yvhe01NDjRjyb_D6gBsy_agImx_n5QQ2RSPdgKQFhuNLbuRTrAJbnj212FbMlNELf20C2jbC6QcWtks5k42W9ZFPg4P1gSE-dBw0PwPPGkWthwlMWoJFneE4ND3hc2uBqMFKlln_ImLag2MWkPmeTzDjmdHKmegwYDKmSb21hdw96qQbwF5uTXhKMXOVKbVJXIlwoXSQwNWhSMK2rwF1jIBZCtKymygKTfIy4T0XpMZruE48nZeRMqW-WlQ2N1B-4YeRtwKzF0C-OBDmHIpL5a3NQ4tDtE0etR-UbKmlPgnKJHQ_ZyQc_1sVDePBrI0xyxcYsHfL1TGL2YSJDvnbqdWXOqU3Ln1DFWqb7bRuf93LGsl62UBsjUn0lPsJq2NNLunNAMdxJ0vqVR2Tsf3Yj0SXzm6bHkYOZ6PD05EZrVEyRGvHLr_Lg8zLGm6ikn2ITENAHfVy0J99eZoJrEH5oSnRq7KlX03gSRLhsaaOyU_wpr9wiDwyRWWKSIy9UkOcGG2RhxKp4HcHqfCgNiSzMwb3dbBsD4bfYCWVIz_3hwHjG98ypih-49tKgYQBHYDDfFdgzgiDb8iHSpIDdDN7p13ZUhMAnj7Ow15iaKKFaGM5CIFoTsHO-DBwVgDTDP9XwXMrP8zq5_BFZC6IR6AmAN6QOybVF5345rN82ElDOXs-3UXDQXbax5KC2254hDbStvgcR-L3H9-Hgk0Pvygd_n9w5Otx6buaEShVhn6SEC-BMvpZyvmSxHao5SYMIzk15Obmo7NSjGwGnJZpUV-49kBlj43g_-3GftQjDEDRmJxwo5k3Ofzzb2j0b9EYHgC9gewSnkiZFs_AOCmY21zGolvxVFmRReD__hE8vy7GY4Gu3XU-vVSPZaQfe3-BLLs8bQMip4c-InfRu4b-VfwdxMQhz8gaY-XERDN1u3X6iDSjHWZ374fb06Pe2WIYXlIYGH9S1tmv4JX6ve4cOomqz5de9hlMY6Nf1IroIYjIZkuFLXVf6l20Co3mjcZobEuBkSxhZ3UKCLz6AbuLVT_XnTHuUB_cxCeqNUZYPRsctB1upIIBlJvd8S6TZdYY8aCpwdTp_BTw6PLCg',
        '__utma': '207539602.2100594883.1742201890.1754402052.1754405992.18',
        '__utmc': '207539602',
        '__utmz': '207539602.1754405992.18.18.utmcsr=wallet.google.com|utmccn=(referral)|utmcmd=referral|utmcct=/',
        '__utmt': '1',
        'SID': 'g.a000zwiGj06BhkhVqEo5BYRuh_VJLlGFwHjQWESKm5mPlz9Cs5OFm9NUpoLD3RVSrcmadKZoEAACgYKASQSARYSFQHGX2MiPBizAyRYaHFpAu249zuMJxoVAUF8yKpRaVk1Oeqz8H8e2lbMNe5w0076',
        '__Secure-1PSID': 'g.a000zwiGj06BhkhVqEo5BYRuh_VJLlGFwHjQWESKm5mPlz9Cs5OFmjZUKdm5wPv5TYrWcMvZ3wACgYKAQkSARYSFQHGX2MiMkDcVTieV5aD_kYkOct4BBoVAUF8yKp1mcvZTjvs0A5WV8j_MddJ0076',
        '__Secure-3PSID': 'g.a000zwiGj06BhkhVqEo5BYRuh_VJLlGFwHjQWESKm5mPlz9Cs5OFDLMKsJI-tK-lD078Nft8UQACgYKARcSARYSFQHGX2MiF4b_zhtdA_lHtEeVmYUdJhoVAUF8yKoSDW7_gb2NmW9rMIWMwn2S0076',
        'HSID': 'AX6vHCdlWDXn1kD2Y',
        'SSID': 'AKlXKIQsKBjNCh6-f',
        'APISID': '36DHgD9_2ik0HEZ0/ALpzk4sI6Km3OgybG',
        'SAPISID': 'l36_yvuIn4OioL92/AE6do6fxgQaZuFUMB',
        '__Secure-1PAPISID': 'l36_yvuIn4OioL92/AE6do6fxgQaZuFUMB',
        '__Secure-3PAPISID': 'l36_yvuIn4OioL92/AE6do6fxgQaZuFUMB',
        '__utmb': '207539602.8.8.1754406177113',
        'SIDCC': 'AKEyXzVA3kjvvaTmBu1vEf82ISUhNfM-Pb_GCv_CyO-mcffSJTfpT2vmkZ2burNw916Kzd8RdA',
        '__Secure-1PSIDCC': 'AKEyXzXG3S87Tfx9PJom1H6VwLSMNtUqqJrxJAiwAD6gmS7kZ4G5Kxd07pqGLLbVJF00Ne3LqHA',
        '__Secure-3PSIDCC': 'AKEyXzUYPI-tXUZv1ggfiGGlj5HUGb3tz9sSORnI4u8k36i1Ay0F9n6AB4f3EcXwO7oTyXWP5pM',
        'S': 'billing-ui-v3=8K7dY7LGplDnDajd7I7I2bpW-tynemF3:billing-ui-v3-efe=8K7dY7LGplDnDajd7I7I2bpW-tynemF3',
    }

    headers = {
        'authority': 'payments.google.com',
        'accept': '*/*',
        'accept-language': 'ar-AE,ar;q=0.9,en-IN;q=0.8,en;q=0.7,en-US;q=0.6,he;q=0.5',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://payments.google.com',
        'referer': 'https://payments.google.com/payments/u/1/embedded/instrument_manager',
        'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
        'x-requested-with': 'XmlHttpRequest',
    }

    params = {
        'ait': 'GAIA',
        'cn': '$p_zgxan3cqur80',
        'eo': 'https://wallet.google.com',
        'hostOrigin': 'aHR0cHM6Ly93YWxsZXQuZ29vZ2xlLmNvbQ..',
        'ipi': 'corpcm8ll9h6',
        'hl': 'ar',
        'mm': 'e',
        'origin': 'https://wallet.google.com',
        'si': '923024884411451',
        'style': ':m2',
        'cst': '1754406173652',
        'wst': '1754406168231',
        's7e': '3.1.0.0;3.1.0.1',
        'rt': 'j',
        's': '3',
    }

    data = {
        'xsrf': 'AJWlU2PnH_Tz3TVACCgfSlWq4x-UXtfwVA:1754406175633',
        '3.1.0.0': card_number,
        '3.1.0.1': cvv,
        'msg': '[[null,"ACo329ybiQMaonjyTdNtAs4mu0MXxNoUVXRsWkgMU4n+deInC7Rq9RBIBixU3FqJ1PPxjsvL1xX/7G8bQxFfd/DfWLN+Z65ydDWKHjgdL/Q9mL2kfPTiDomNxfIyIbT/nke5Wql5f23G4R5fm2dy8a4NBzYh2s2I44wi+BTnANgbiVdK1cBJoQ7383MlI+oDc77KStEQpfT9KZlY/54S2xdxd0lwUs0QgxOue1fSLIzH5KNTWStZnsPvlCg/wEPHCGlG3qKhSonUE",null,[null,[null,null,null,["!Li2lLXXNAAZAdzQfYHdC-uONdNLm8sA7ADQBEArZ1KnJK6NYjAxjkcLd5z9XpUs9CGchOT74-eTKBTFi2_cRHVP_MswbMqE3jmyUB315AgAAB5JSAAAAMGgBB34ATFdDoRwh1-xtagN63homNShL5nm0wetAykzOCBH-XSQt2k1GvXCVh0JY_9C3x7WdIsXiaahWccBXPwGlRgPQl9ZZgtM3bFyAxP5QL3yZCCgPu18FrqfoaAWbEBHoFWVqms4VUCGXpExqtK6fpXKviI0sH0ZolTd5zWB57wkpxRTyfUWgLE10LcNdFAAF6tX2_DCNwSZkG-PY2lvqHdtGsWMFlWDVg6Ml0PnQWPuuMH0VCINZpLlM6vqvMOunB_a9H4pev4-pxCk8IJtLnSNl9r-2CLns7X4ZwOjTxnvnhBWTi6Q1OSEkxwa5LhYHTr8l8qZS9d1WGYxOkI9czVS14FPT0eI0JU5hJDfBf1f8awjyMYiKKtijdSOTUca_1-PQmb4arHrMTFo2PZV0GDltoliuEGQx8152p773EH6agpioWTTC0yq4AEAmfRgqYx2LLSg-u7UfyYh5_opN2J-CKJC0u6kG4s1hwYg2whdQ4G35FcMsc7VWxrjDaMZx_EUz-tMW1McGhg3frSYwJUd55yMb5kHrqgszXUtLRtzcfrMdvilM_iHaMO62tW_2BBTcITQedHuRiCpa6IUG9CnwqkAwAAXHlCU4k3_pBd75wg5qlMPzeApfujrU15UY36iQT1eCs6M3Rw9P_Gd-6tkQmANfceiM60oCE1d8JTDBWNNfXU0yzqvIJxuvx3PgNKZDToOrv-h1vVjVTqq50X9kmvCxiHaXbz6koW47ysXskNoljKSqvI8Xahuz3i0OZG6aasKnt3VokqdGfZtvrIIGHns1-Or2s9SJDGc6cbX_VD90t7ySPxq13tNcNwR3dj1o-ReUZk2Euq7XYmIZ97Al9tNrnMWCmpJiKjLYWlo3d0gWEOXFHU9I9WPJXGI8bxObfNp7wKq4GFTHML_RUAPgQjUB-7pNcRk9rj3E2fwV0dy3d20mTsoBAjY54GtnvbRM9MJy6tPeVHwLc6OQp7bJUPa726IPV2A6skSCMNK1sU5S_wl2GI53JGA2OdkkkEABdJQQOAXZQFNu9C6v1AiX8onSE4juShdS1SuLsIr5_6m4UjYFVOTped5gQAira210ujxqKlSztlb2u8qraWQVRddi6eWb2CQoB10EEuXZLgBQQohA4ToJnZIY2A7V_qSpFbi1h8i6VKoSVf0VMiAyLVwleZG1Sjy9MR56kEEk1yq_2cNInf-kWf7i3QhetgEiYgMwhYt14m_VW6gNNj57P87kR_RF420B0YhXlI7JR3pS9NwAbvBIPcQ-S5XfT3nBYUDtPTJ2_y6aPjZfw00a7xUgVqoj4XqFYf_L22hq4t8pgpbpmwRqqHNR61Ik_1laxuJSNtj7ukoFloxHTtGlhk6gMqMK0570msF2t9r7VcuAt33aLabNj6xuaecwTkZiX4qj_cX7XmBwJuaLWAeYaABJsswL3UM5hUXzHFxTB865iLZZIqOd6YtjztasL2aj0Ad0f4YqzjKP81q_91Ahn9zyQ4i3S8byp_5QxGt0bGgCnQK0IAa3_0Xk2bEiNbuzgvJ0mO9W2K2nQB3RPncrMYwcVJXDrEaSC1kE_7vcouScnAXmXbcR1xORrJM2eVAvC-mAz1Y1M9qMvzinXJ5EVZ8JRHWu0xLVAZFw2NlbvmaWB1A1xyBgoZf0xmZKBcSqCPTCGN1BGjhAEfIQ7gT8887qahKIvRavz2VWcrIrZBxPC5i-Xiu1o5sgcZ4u747jVyiKVHBDAWG4FzWl8LrXVqOAyrHtRD0DLckTakm2XPM60zeOgqZC_nU04O0udyRbuQ5mXF4gfHakvBpslSDwt9UtDdI-cBblRgN_8jbgiT7iNOjmlj3WPH1Xe2dFbw5_89CYj8Mlsq0pnEdycoDv0Td4Hna29SnfLjnv0ALN3c_M32QVf0kDhFtBwNJWmaI6yVs0GizVbTTS7XHn6nBMXPzO9tNNoJYohjMOwbOZ_5bh3Rd_fDUYPEcVZSYal4wdvENdkH_6HOuAk2PYOYJkKxyfevzeDfLcbAVu-Qo-tSG_beBfcA9hKmft-n0C8B9cbKrTu8J9bqubPUqLZQFFMabV6U_TbIVzoOzZ-qW1qIj7KyYRl_mcmZKdDEkBiPbqrgYCk4TdqokMmnrRHDcuqGK5WOkQ383dN6Ippbl-XcWtFdyzVUuG8WCFUvCV_c9ENzhXzyoXuL1LAPDOs5CyIz7-72EbuKfGb-Yb03MXbKst1ya0b55XrO1ApzrSV32kzLKSFvZDGayxF1hvRWDBXZ4Us-JOMzTyGl0F4IXrHoCXQsmuLGuNukwH3p3mYu-rzvk56fPY8uYzhs91-phcTmK-sqNxJtL1kWLme5XbRwhp6lBvs0z4RgTEc-DcUBLstIBGKumTA-7-XhSchkIEWhIh5VvqFgYPrJXwiiuUt2jX3FtPl3kqmG7r3ALTnlfSE7pDQxfYpoXP3nKnVCeJY2U4GfwXQ1DN6cqodaTERHG1T7sQFia7fnYP3avPqml3hrnai2dNFhRaKafHRu7R_2cGDoHzq1Q26qLYonzMORRRlRlWAykCjeI5u_36dEOeUKemPviFt-_OP9h275k42g_xlua8FbJbQKSiETilP6yR32m-7JJB8GTLnh1JiJA3cthm_wnkVFDuBULDD31m6ARLlDX16bqo26VZ-ziDA5COSSK49Hfn7ZIR9Mxe1JbtCPg97LRTfyknTAf-t-rl67AX3Jv3SIZgiI7Zqun72U_bapr-afsA6EaEL5keVGXeXlNtSg41SgMv3Z2ok5lh2HqrtGJ9ARjpfKKRSjS8Zm1J_juvbUXYzNblHFNaaPdFqI1OlmHrAUFWDASAD0PumREXrNHinHKzV8jNeBGnDcLD4pQQjumVBGy8LruJqFgBaNG6Rru8WFY"]],null,null,"ar",1,1],null,null,[null,[["__secure_field__4fa1d0a7","__secure_field__4fa1d0a7",9,2026,null,"5168",null,"__s7e_data__61bb463a","Mr cnn",[["US",null,"TX",null,"Plano",null,null,null,null,null,null,"75074",null,["098 Fairwood Village","Oisoddn"]],null,null,null,"billingAddress",null,"CggIxLmJwwIQAQ==",2001],"CAEQAxogEgJVUxoDVVNEMAhAAFABYPWnBGoCCgCgARSoARSwARQ=","0.buyertos/US/6/20/en,0.privacynotice/ZZ/5/9/ar","creditCardForm-1"]]]]',
        'kt': 'Rs2.0.8:billing_ui_v3::s11,2,26b5e19,1,140,a063ebe9,0,2b6,edd98bac,0,18,4863fd35,0,140,cb2d5c6f,0,2b6,6ad47c6c,2,e8,7bdb49f6,0,95,b6540200,0,140,eea820b6,1,236,1aa4331,0,"Linux armv81,f54683f2,0,"Google Inc.,af794515,0,"5.0 28Linux3b Android 103b K29 AppleWebKit2f537.36 28KHTML2c like Gecko29 Chrome2f137.0.0.0 Mobile Safari2f537.36,d81723d1,0,"ar2dAE,5cc3ab5f,1,"Mozilla2f5.0 28Linux3b Android 103b K29 AppleWebKit2f537.36 28KHTML2c like Gecko29 Chrome2f137.0.0.0 Mobile Safari2f537.36,24a66df6,0,-b4,"Thu Jan 01 1970 023a003a00 GMT2b0200 282a48424a2a 343142 234831482827 27443133454a29,770c67fc,0,5:a21,3,1987ac1c4b2,10,"cardnumber,"ccmonth,"ccyear,"cvc,"ccname,"COUNTRY,"ORGANIZATION,"RECIPIENT,"ADDRESS_LINE_1,"ADDRESS_LINE_2,"LOCALITY,"POSTAL_CODE,"PHONE_NUMBER,"embedderHostOrigin,"xsrf,"sri,84,2a7:a40,"f,1987ac1c759,"n,0,0,"t,1987ac1bc37,0,0,0,0,1987ac1bc45,1987ac1bc45,1987ac1bc45,1987ac1bc45,1987ac1bc45,0,1987ac1bc51,1987ac1c010,1987ac1c033,1987ac1c037,1987ac1c4d6,1987ac1c4d6,1987ac1c802,1987ac1c916,1987ac1c917,1987ac1c96d:a10:a31,3,"h,1,"p,108,56,"m,115,bfa,1808,ae8,20f8,a93'
    }

    try:
        session = requests.Session()
        session.headers.update(headers)
        
        response = session.post(
            'https://payments.google.com/efe/payments/u/1/instrument_manager_save_page',
            params=params,
            cookies=cookies,
            data=data,
            timeout=15
        )
        
        content = extract_text(response.text)
        
        return jsonify({
            'status': 'success' if response.status_code == 200 else 'failed',
            'status_code': response.status_code,
            'response': content
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
