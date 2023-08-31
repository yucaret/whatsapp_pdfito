import os

#token = os.getenv("TOKEN_PERSONAL")
token = 'bigdateros'

#whatsapp_token = os.getenv("TOKEN_WAPP")
whatsapp_token = 'EAAPNsmzVTZB4BOZCJMHZC4bfa8e5UsBjByexIakNp1WXIUVxPiJ0eyK50JhNjFm78qZCztS40WCDOxKK6ZBqOaeHxSGZBCoAnQVYtyc2WL4wsnxdUzZCVRUZAbavccWP36V2NUZCTPu4E3A8ZAXKA79SV4ZA15fAdRZCJdt9cMGCeQ6k5XS2U1jQZC64PrY0uNFz3RMk6woUVmCb04cfpiTmZAHEXP5TNX2sbNaT39NlUZD'

#whatsapp_url = os.getenv("WAPP_URL")
whatsapp_url = 'https://graph.facebook.com/v17.0/108681648964959/messages'

#whatsapp_phone_number_id = os.getenv("WAPP_PHONE_NUMBER_ID")
whatsapp_phone_number_id = '108681648964959'

#openai_api_key = os.getenv("TOKEN_OPENAI_CHATGPT")
openai_api_key = 'APNsmzVTZB4BOZCJMHZC4bfa8e5UsBjByexIak'

#celular_gerente = os.getenv("CELULAR_GERENTE")
celular_gerente = '51949702168'

media_types = {
    #'audio/aac': 'aac',
    #'audio/mp4': 'mp4',
    #'audio/mpeg': 'mp3',
    #'audio/amr': 'amr',
    #'audio/ogg': 'ogg',
    'text/plain': 'txt',
    'text/csv': 'csv',
    #'application/pdf': 'pdf',
    #'application/vnd.ms-powerpoint': 'ppt',
    #'application/msword': 'doc',
    'application/vnd.ms-excel': 'xls',
    #'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'docx',
    #'application/vnd.openxmlformats-officedocument.presentationml.presentation': 'pptx',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': 'xlsx'#,
    #'image/jpeg': 'jpeg',
    #'image/png': 'png',
    #'video/mp4': 'mp4',
    #'video/3gp': '3gp',
    #'image/webp': 'webp',
}

stickers = {
    "poyo_feliz": 984778742532668,
    "perro_traje": 1009219236749949,
    "perro_triste": 982264672785815,
    "pedro_pascal_love": 801721017874258,
    "pelfet": 3127736384038169,
    "anotado": 24039533498978939,
    "gato_festejando": 1736736493414401,
    "okis": 268811655677102,
    "cachetada": 275511571531644,
    "gato_juzgando": 107235069063072,
    "chicorita": 3431648470417135,
    "gato_triste": 210492141865964,
    "gato_cansado": 1021308728970759
}

busqueda_url = "https://www.enel.pe/es/personas/consulta-ultimo-recibo-deluz.mdwedgeohl.getHistoricalInvoices.html?supplyCode="