from flask import Flask, request, jsonify
import requests
import urllib3
import re

# تعطيل تحذارات SSL غير الضرورية
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)

def extract_arabic_text(text):
    # استخراج النص العربي فقط من الاستجابة
    arabic_pattern = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]+')
    matches = arabic_pattern.findall(text)
    return ' '.join(matches) if matches else "لا يوجد نص عربي في الاستجابة"

@app.route('/check_visa', methods=['GET'])
def check_visa():
    # استقبال بيانات الفيزا من query parameters
    visa_data = request.args.get('visa')
    
    if not visa_data:
        return jsonify({'error': 'يجب تقديم بيانات الفيزا في الصيغة: رقم_الفيزا|الشهر|السنة|cvv'}), 400
    
    try:
        # تقسيم بيانات الفيزا إلى مكوناتها
        card_number, month, year, cvv = visa_data.split('|')
    except ValueError:
        return jsonify({'error': 'صيغة البيانات غير صحيحة. يجب أن تكون: رقم_الفيزا|الشهر|السنة|cvv'}), 400
    
    # تعريف الكوكيز المحدثة
    cookies = {
        'OTZ': '8178671_44_48_171240_44_319500',
        '__Secure-ENID': '28.SE=PTeBA7BBHK3_SWp8A8QwkyWQ0NV2M6jrKe4lof9MMpzxuICErWtDvATtFm8rd7U0aB9yGNxZ2IMXzWRtIEIUkioKphf4htJA97i0z7zmJpFdJDGz_Cu0LuTfmIvOuPfAO9PoSmjDcSglULgqp1EtEktt0JCd2Y6DpQMXh9DAuDhkHeYs_Om9WJOx5ZYM--O_IlAUF5En',
        'AEC': 'AVh_V2heWGGWR6RJaCA3moYCqStgFwI4jiCbc15w80TlB4YShHtN3EFoH7M',
        'NID': '525=ikO_se4-1r-FYmWnCcNNAtdDGChW-nZpocwBnz1oVOo4CnXpYC_JmmXTzUbo1j8k6Hcd-C2m_fDyr_sqJqGBPniwnOQdNyj2To8Zs7ZNyDhqJuW1iVVY71GuqSbgdXEVUf1PqcpEnyxIMhspDyLzlLaFFkV3xC6p7UtpBYcS9z8WXM4dCtlPc51DtxWDXU-AGnVCGngSK3YoWPlauUFPDzkkmu4yA5q4ZA9otV4ehKGN7gJwUbd7IuDpa1RYcXzWXacJjebE3Bv3ShnDFtPGJw7IRi5CZ5ZQWpF82wMCX1Eg4ezjNjeEJLsL94w8KziSHNVHYt-FYUyQo_taQGUlqhUr7CE2vfrK4jcYcwzi0uS_18yvhe01NDjRjyb_D6gBsy_agImx_n5QQ2RSPdgKQFhuNLbuRTrAJbnj212FbMlNELf20C2jbC6QcWtks5k42W9ZFPg4P1gSE-dBw0PwPPGkWthwlMWoJFneE4ND3hc2uBqMFKlln_ImLag2MWkPmeTzDjmdHKmegwYDKmSb21hdw96qQbwF5uTXhKMXOVKbVJXIlwoXSQwNWhSMK2rwF1jIBZCtKymygKTfIy4T0XpMZruE48nZeRMqW-WlQ2N1B-4YeRtwKzF0C-OBDmHIpL5a3NQ4tDtE0etR-UbKmlPgnKJHQ_ZyQc_1sVDePBrI0xyxcYsHfL1TGL2YSJDvnbqdWXOqU3Ln1DFWqb7bRuf93LGsl62UBsjUn0lPsJq2NNLunNAMdxJ0vqVR2Tsf3Yj0SXzm6bHkYOZ6PD05EZrVEyRGvHLr_Lg8zLGm6ikn2ITENAHfVy0J99eZoJrEH5oSnRq7KlX03gSRLhsaaOyU_wpr9wiDwyRWWKSIy9UkOcGG2RhxKp4HcHqfCgNiSzMwb3dbBsD4bfYCWVIz_3hwHjG98ypih-49tKgYQBHYDDfFdgzgiDb8iHSpIDdDN7p13ZUhMAnj7Ow15iaKKFaGM5CIFoTsHO-DBwVgDTDP9XwXMrP8zq5_BFZC6IR6AmAN6QOybVF5345rN82ElDOXs-3UXDQXbax5KC2254hDbStvgcR-L3H9-Hgk0Pvygd_n9w5Otx6buaEShVhn6SEC-BMvpZyvmSxHao5SYMIzk15Obmo7NSjGwGnJZpUV-49kBlj43g_-3GftQjDEDRmJxwo5k3Ofzzb2j0b9EYHgC9gewSnkiZFs_AOCmY21zGolvxVFmRReD__hE8vy7GY4Gu3XU-vVSPZaQfe3-BLLs8bQMip4c-InfRu4b-VfwdxMQhz8gaY-XERDN1u3X6iDSjHWZ374fb06Pe2WIYXlIYGH9S1tmv4JX6ve4cOomqz5de9hlMY6Nf1IroIYjIZkuFLXVf6l20Co3mjcZobEuBkSxhZ3UKCLz6AbuLVT_XnTHuUB_cxCeqNUZYPRsctB1upIIBlJvd8S6TZdYY8aCpwdTp_BTw6PLCg',
        'SID': 'g.a000zwiGj6-ZM0WU5iNgNBycEBfllIm41w6BoDZUN0M2tW1jtId68diM8BeDu1aixQLuSCN0DwACgYKAY8SARYSFQHGX2Mi5HRUzPoG1P33l7g2unNloBoVAUF8yKpm6Dx6Sww9wIHloGGdX2fF0076',
        '__Secure-1PSID': 'g.a000zwiGj6-ZM0WU5iNgNBycEBfllIm41w6BoDZUN0M2tW1jtId6p7AkvU1pFR7oVeavX5_v8AACgYKAVwSARYSFQHGX2Mi4EJiYZZ3GZvUl2IMQrvYNRoVAUF8yKoGMLP194cVmQmDc9V27Bu90076',
        '__Secure-3PSID': 'g.a000zwiGj6-ZM0WU5iNgNBycEBfllIm41w6BoDZUN0M2tW1jtId6Voiez-RlEfxWvlTyaXOa-QACgYKAe8SARYSFQHGX2MiQT08W8NPeV59uM43wXJPwhoVAUF8yKpJXW9rtvG4NiRkzapnP8NW0076',
        'HSID': 'AgBH_CTA7aRR34nUi',
        'SSID': 'AdfAPnx3xyR8KnwVE',
        'APISID': 'zUNax8nba0AdRyw7/A2an76LjrFAXx3zbQ',
        'SAPISID': 'sRnoT44095ds5-Z7/A7_snYLrG8J-pRR34',
        '__Secure-1PAPISID': 'sRnoT44095ds5-Z7/A7_snYLrG8J-pRR34',
        '__Secure-3PAPISID': 'sRnoT44095ds5-Z7/A7_snYLrG8J-pRR34',
        '__utma': '207539602.2100594883.1742201890.1753969377.1754402052.17',
        '__utmc': '207539602',
        '__utmz': '207539602.1754402052.17.17.utmcsr=wallet.google.com|utmccn=(referral)|utmcmd=referral|utmcct=/',
        '__utmt': '1',
        'S': 'billing-ui-v3=zRVbvtPRocoP52E7aV2R3MwKXLlgZbrq:billing-ui-v3-efe=zRVbvtPRocoP52E7aV2R3MwKXLlgZbrq',
        '__utmb': '207539602.4.9.1754402136569',
        'SIDCC': 'AKEyXzWNo-vMibFuoAB9UhjC4PfGeVlDxwkkHQKaKo6MyA-wSoQLA3oGPkJXny3ow6rKsa1pEw',
        '__Secure-1PSIDCC': 'AKEyXzU1WNBIzzPwfA0bxvWOciCKmkVdi9dXFBmHlb2Z0JmtukE7hWRXdql7RQHn0GUEfe8IdB0',
        '__Secure-3PSIDCC': 'AKEyXzUfL3UE8T0KXhw-xXA5B-LBbUkcDGyS103tFEdGPveRuNtyR_gOkDuW329JLN459r4GpSs',
    }

    # تعريف الهيدرات المحدثة
    headers = {
        'authority': 'payments.google.com',
        'accept': '*/*',
        'accept-language': 'ar-AE,ar;q=0.9,en-IN;q=0.8,en;q=0.7,en-US;q=0.6,he;q=0.5',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://payments.google.com',
        'referer': 'https://payments.google.com/payments/u/2/embedded/instrument_manager?tc=96%2C87&wst=1754402040007&cst=1754402049430&si=3762931366960241&pet&sri=2&hmi=false&ipi=q5bfyuh9wujw&hostOrigin=aHR0cHM6Ly93YWxsZXQuZ29vZ2xlLmNvbQ..&eo=https%3A%2F%2Fwallet.google.com&origin=https%3A%2F%2Fwallet.google.com&ancori=https%3A%2F%2Fwallet.google.com&mm=e&hl=ar&style=%3Am2&ait=GAIA&cn=%24p_wl069yfpvw0y0&fms=true&actionToken=CiQIASICVVNoAXAAeAGaAQ8KByDO%2BsrSugIg9acEYgDAAgD4AwE%3D&spul=502&cori=https%3A%2F%2Fwallet.google.com',
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

    # تعريف البارامترات المحدثة
    params = {
        'ait': 'GAIA',
        'cn': '$p_wl069yfpvw0y0',
        'eo': 'https://wallet.google.com',
        'hostOrigin': 'aHR0cHM6Ly93YWxsZXQuZ29vZ2xlLmNvbQ..',
        'ipi': 'q5bfyuh9wujw',
        'hl': 'ar',
        'mm': 'e',
        'origin': 'https://wallet.google.com',
        'si': '3762931366960241',
        'style': ':m2',
        'cst': '1754402049430',
        'wst': '1754402040007',
        's7e': '3.1.0.0;3.1.0.1',
        'rt': 'j',
        's': '3',
    }

    # تعريف بيانات الطلب المحدثة
    data = {
        'xsrf': 'AJWlU2O8npT5wiFL-iWtuZx-58LvlwUppw:1754402051482',
        '3.1.0.0': card_number,
        '3.1.0.1': cvv,
        'msg': '[[null,"ACo329x7mTbyjb619D4tHrTthbwG8P9Gosp0eGf63p/5wkyZw/9x2zumeH1W9rLs1jOoj2VmCkCQEW69UJZYGvLfQPOS19y9sH0+YUi2TvfWB+lgcV0ZF6ogasHBnw/NzLeiyiw3dUGa37U1DDrxTba5mGySrkCdIkufBQk12a2epSOzwCVe5lf6oHgUmA7fNodfsAlxjUdIBAlIg9DJOoypc621+JeFqVPYtAUOFLYbKDM/GbAcsyKkXqL2kTaBoonXb9oo9vRn",null,[null,[null,null,null,["!h4SlhNzNAAavhfsHj4VCAUy-YvXw0cU7ADQBEArZ1PjcAjqsbSXFkDiJTyzRes_ZjN8-BkYk7LPrYNeJL-etgYyjoDFiusQbAlC9qmIsAgAACilSAAAAN2gBB34ATNZB7-qEFTPvZWtylQ62o-jZHJWyIcoJ9-JQYlYkuU5-VkS0oaNm22uxOnpylQKQ9npMlarKEIAK0F82h7YYCtr02v1KWgorj6zMDo6ZCONjHTdtriVlHAmz9xEoXmfg0830miXB3qPaV_ES5TvrttOYABs6ptXSq4jyFATTatIdvX6JRdoZohEQcDvZ3zT1qT9NMVR1jtriMGfLtgfOCQ14JKePiD9AJrKrMVnmy4CMYTezFmNBtuNPSqSHRMdKlwaMlmhrSPkeQo5OccmQpBe8hjNGoR8d4QvRWddVuAU4PcdXR414xTTDQGpX7pcofNZd4t3IDQYnLS-7PDs0yogX0jfeZT-GuDeDbNd3VZjPzZ-Ah2pSHx3Y4FjmlOdlcHPIC5UFYUMdTyGeXN8h9kRUOQHCqlQbCdhmrkKE9Pr1oUv_-SNxZM8hBtvSqE4Xy7OgD8bPkOASCNrmdrADn0dILS15jSyB_UI08t9tvIZqhOkz5-Qljdpz27pcGLHH_VShgt5Q_eT7-j_tG-11pvCiJds_FucUmDOu2RDrz1D8MkU3VUsWO6MZBo6VH2nRjqNeICQ_EfWI_4mI4R8cwVZ3i1xK0rWUL_WM-w8mrvxTaSfmbsAXOt6E5BrPxAjYuR6eTZbj0TPAUm2Xhg2gYhNTYlZEoJT0h_fQFCoXjj2aBM6xE4hEXbSVL-bzxbwA4arlwZylLwctoEbuih9IT2akyRqOaMdotnyU5f2MTcRSPF0SNQ1YXub3Angyu8kw6b6v_6PreK6nf-Thcx-3SGRDDwcLW1jFzZgM2WZjDSBCuA6CKkXgao5hwANqLr79rY3idaRUTL-e66EsA7kwUFr_I6cKv3gzQjkgNMpODpQz-fOOGCaeDQrP8DdF9NpM7HcgsNd_8EA2sn3iSzA5-0VjY7WGCY-uiXq37sT15fxvSjQeR1p1qlcbz5uOKWESpxwkkHDWP5dGUtx_ddJw1LVJMfLUmTBRqdla4U3dGL1Bkq1gEI-XUTpl95w3cZWyQ2ioCsXXRbVHtA5QStK7fqrXpRWyCnG1psjMdyqUCUKt8TdqEPgV1fKcij9UNAKsGLq8EJAD-z71PIPbGbpLiDgfXe_XJzDrIM1Agji4wYsUSoje5OXNE0rHIBX6Mb6ymZN-SrW6E_7Mvb0tEFrQaYfSVstg9DDmua7Hwz9whcdQvayKNwXqfQxzMdusreA3TO3_UiL25_UAQxmH6ue499V9QjuGh0bMD0RkLPynl92mzNkyl13k6-oCBla5BzcdqT6lz75pffugu5Y8iKC3UpirJyaB_RisvhBdQVd1R219YUnLo_HIMT-bqhrPemPZ4HcIdMnvaRiXkbh9e8cPJ-QLBSo0FX5BJfqF468afcQUm2jausZlUPwEWTm8DW1dvWnXeq_gbTTgNQcr4eqMxKFHQbHtTV9S_sHYmSS1Y5dZDF-RdWzU2B-ftiIBxc4vhqJbM1DWxRguj4XJG5zExriCcL0dFpgYoBhPt8jMoSGV8LDvAe4JDPbCulPH4reOyYAvr6fXjQdpSldF1UF4gH71imcdcBuKK_qojbXPz4C26P3vAfMMRDKRmyjX3OZJ76CPK54a3Jw8zqT2onoI2-F3zj6gAuvH2hIlyuJnM3kjEyZvwQiwTp5luoY4G-WoerMZXDPrx9Q7U_lfmIfjrlBXOSgCKn9JmEpCulTgsJFnRkH-SOucGt0P62pUFtQVQt2UDGhdThSkQzPxG6OyyPhvdpd_ztenut8wA65dmxtQQVp9BxBiy_kCsUayHiW5raN79_U25ZHbl1aYX2lFEza616ZdlGE9DBSkuPzkwqy7eZXnNfelm1zJRkfMrepILwvUpHKLmBLhQ6hYF0T9SyXB-GqT9Cqt2TfAItMQ4q3D7ev69NWYTllOOsPr9bwWeUdtAxUovHoG4TTAdrhFV08Mt3IItwcSlAeGQOlxfRAaNdWYYmm2zgVAKJbdaprIuCC_tZOz_zSZOyxuc4rOp-aUSo-rk5m_nCgY7MDHtS0F_AuLnJgL3uyp0pcMAiqveAZMm3aCf4uGYwMgtTl2VlNxnq5P53DlCcaj9FVywWdiTUWE_2GW_6eXtbtDhvFWj7-uebSgFiR6sMQ-4OBDg-T_D54l1U8SOBhV8970KoOu6SFscKIqRNjB3CtNd00kmOLxxsm1LCNxS7MsZcjiuvtrUr6Bk9-VE0GJy7kG0vsrjUe1yFYaFbtPXHFB5IAzrdFm2WtdNNxxncL1P9FwHGGSe4IxBuag7qMU9a7qu9eM5UywEOhyoMpAH_4uRoMfbpaMclYnYkom2B4O1FaA7-CbrivUHX5CVdtDQdkTZTXNGwJDThRnK3Doiped_rQ64T4n9Pf5SkgxN1iqVIHImurqndHBCq7lpmi7MxZwm0mS_GssD4UCizbhO805s-CcNAIqWd9IciQxwXBkQmdtXofjhKdaccaKbSWWC5jI6odqCWat6HHYk5HOYHDyG0jr4p3tl0LsaY1U4Rih70AEDTmcpX2L5y-pZpPbmBL5uIOoW-jIlqsDX5nMLghWTGSHoAyr0Eoner-wRWVuiXQgpC_8J1gG-r0YSzpB-TW9r3bqIyOBRHaHNDkXROOQAOFpDnj1E5YNLVkD_wgePE86fnoY1JjEq9guU-KxbjCzAQyb15AqAvkUTvhViAL_FCJDupRrUKB6lpB2KuImxsIAnP0ocrWWH2CfyLUO2BYLw0SLBLT2pZuleb0dchDxznQho1X3td343RAQ8DMK0BYP93CCoDzYpRV45kzoTCWrV3GHkm_BSGty_Ont5N0nyJfWJSmO6RDOpS9lLDpLzNUZUlBiCLxL0ZBZ0UuIYhrgfqegy7qi1bFI_uAh3X38a3pb3zol3Q4dBwYJj4yWKWwz56XlXnb4Howg9N1zNi34D4o285zCEIurMV6zj5LnWkShoXSmiWy0d8lR8qVCdQ2QV4uYYLAQTqnHhNJQhYvT9_L0b6BiSkn36a-2fSj6TiQoTRT_VZjfktE7tZh1WzSw0xoJFoE7WhoTD64uVUdnu_5328m5bcPdF5ZENPk-uyLjwzPHA0Eie75C3xA_7QoAd8xZNyJPqJi31d5o2p5Uq54pDWhGh3_U5gyDgZEJsZcBjemT"]]],null,null,"ar",1,1],null,null,[null,[["__secure_field__4fa1d0a7","__secure_field__4fa1d0a7",9,2026,null,"7526",null,"__s7e_data__61bb463a","Mr cnn",[["US",null,"IL",null,"Winfield",null,null,null,null,null,null,"60190",null,["0s036 Church Street","Mr cnn toun"]],null,null,null,"billingAddress",null,null,2001],"CAEQAxogEgJVUxoDVVNEMAhAAFABYPWnBGoCCgCgARSoARSwARQ=","0.buyertos/US/6/20/en,0.privacynotice/ZZ/5/9/ar","creditCardForm-1"]]]]',
        'kt': 'Rs2.0.8:billing_ui_v3::s11,2,26b5e19,1,140,a063ebe9,1,2b6,edd98bac,0,18,4863fd35,0,140,cb2d5c6f,0,2b6,6ad47c6c,2,e8,7bdb49f6,1,95,b6540200,0,140,eea820b6,0,236,1aa4331,0,"Linux armv81,f54683f2,0,"Google Inc.,af794515,0,"5.0 28Linux3b Android 103b K29 AppleWebKit2f537.36 28KHTML2c like Gecko29 Chrome2f137.0.0.0 Mobile Safari2f537.36,d81723d1,1,"ar2dAE,5cc3ab5f,0,"Mozilla2f5.0 28Linux3b Android 103b K29 AppleWebKit2f537.36 28KHTML2c like Gecko29 Chrome2f137.0.0.0 Mobile Safari2f537.36,24a66df6,0,-b4,"Thu Jan 01 1970 023a003a00 GMT2b0200 282a48424a2a 343142 234831482827 27443133454a29,770c67fc,0,6:a21,3,1987a82d79d,10,"cardnumber,"ccmonth,"ccyear,"cvc,"ccname,"COUNTRY,"ORGANIZATION,"RECIPIENT,"ADDRESS_LINE_1,"ADDRESS_LINE_2,"LOCALITY,"POSTAL_CODE,"PHONE_NUMBER,"embedderHostOrigin,"xsrf,"sri,84,2af:a40,"f,1987a82da4d,"n,0,0,"t,1987a82cdfb,0,0,0,0,1987a82ce04,1987a82ce04,1987a82ce04,1987a82ce04,1987a82ce04,0,1987a82ce14,1987a82d21a,1987a82d237,1987a82d23f,1987a82d7c6,1987a82d7c7,1987a82db1d,1987a82dc59,1987a82dc5a,1987a82dc95:a10:a31,3,"h,1,"p,6b,46,"m,4aa,15b0,8dd,17fe,f04,3c2,32c1'
    }

    try:
        # إضافة جلسة مع إعدادات أفضل للاتصال
        session = requests.Session()
        session.verify = False  # تعطيل التحقق من SSL (لأغراض الاختبار فقط)
        session.headers.update(headers)
        
        # إرسال الطلب مع إعدادات متقدمة
        response = session.post(
            'https://payments.google.com/efe/payments/u/2/instrument_manager_save_page',
            params=params,
            cookies=cookies,
            data=data,
            timeout=15,
            allow_redirects=True
        )
        
        # استخراج النص العربي فقط من الاستجابة
        arabic_content = extract_arabic_text(response.text)
        
        # إرجاع الاستجابة كـ JSON مع النص العربي فقط
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
