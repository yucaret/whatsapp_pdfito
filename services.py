import requests
import urllib.request
import sett
import json
import time
import os
import shutil
import pandas as pd

def obtener_Mensaje_whatsapp(message):
    media_id = ''
    
    if 'type' not in message :
        text = 'mensaje no reconocido'
        return text

    typeMessage = message['type']
    if typeMessage == 'text':
        text = message['text']['body']
    elif typeMessage == 'button':
        text = message['button']['text']
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'list_reply':
        text = message['interactive']['list_reply']['title']
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'button_reply':
        text = message['interactive']['button_reply']['title']
    elif typeMessage == 'document':
        media_id = message[typeMessage]['id']
        text = message[typeMessage].get('filename','')
    else:
        text = 'mensaje no procesado'

    return text,  media_id

def enviar_Mensaje_whatsapp(data):
    try:
        whatsapp_token = sett.whatsapp_token
        whatsapp_url = sett.whatsapp_url
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer ' + whatsapp_token}
        print("se envia ", data)
        response = requests.post(whatsapp_url, 
                                 headers=headers, 
                                 data=data)
        
        if response.status_code == 200:
            return 'mensaje enviado', 200
        else:
            return 'error al enviar mensaje', response.status_code
    except Exception as e:
        return e,403
    
def text_Message(number,text):
    data = json.dumps(
            {
                "messaging_product": "whatsapp",    
                "recipient_type": "individual",
                "to": number,
                "type": "text",
                "text": {
                    "body": text
                }
            }
    )
    return data

def buttonReply_Message(number, options, body, footer, sedd,messageId):
    buttons = []
    for i, option in enumerate(options):
        buttons.append(
            {
                "type": "reply",
                "reply": {
                    "id": sedd + "_btn_" + str(i+1),
                    "title": option
                }
            }
        )

    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "buttons": buttons
                }
            }
        }
    )
    return data

def listReply_Message(number, options, body, footer, sedd,messageId):
    rows = []
    for i, option in enumerate(options):
        rows.append(
            {
                "id": sedd + "_row_" + str(i+1),
                "title": option,
                "description": ""
            }
        )

    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "button": "Ver Opciones",
                    "sections": [
                        {
                            "title": "Secciones",
                            "rows": rows
                        }
                    ]
                }
            }
        }
    )
    return data

def document_Message(number, url, caption, filename):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "document",
            "document": {
                "link": url,
                "caption": caption,
                "filename": filename
            }
        }
    )
    return data

def sticker_Message(number, sticker_id):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "sticker",
            "sticker": {
                "id": sticker_id
            }
        }
    )
    return data

def video_Message(number, video_file_path):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "video",
            "video": {
                "file": os.open(video_file_path, "rb")
            }
        }
    )
    return data

def quickreply_Message(number, quickreplyId):
    
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "quick_reply",
            "quick_reply": {  # Nombre correcto de la clave
                "id": quickreplyId
            }
        }
    )
    return data

def get_media_id(media_name , media_type):
    media_id = ""
    if media_type == "sticker":
        media_id = sett.stickers.get(media_name, None)
    #elif media_type == "image":
    #    media_id = sett.images.get(media_name, None)
    #elif media_type == "video":
    #    media_id = sett.videos.get(media_name, None)
    #elif media_type == "audio":
    #    media_id = sett.audio.get(media_name, None)
    return media_id

def replyReaction_Message(number, messageId, emoji):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "reaction",
            "reaction": {
                "message_id": messageId,
                "emoji": emoji
            }
        }
    )
    return data

def replyText_Message(number, messageId, text):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "context": { "message_id": messageId },
            "type": "text",
            "text": {
                "body": text
            }
        }
    )
    return data

def markRead_Message(messageId):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id":  messageId
        }
    )
    return data

def validar_parametros_como_numero(suministro, anho, mes):
    try:
        suministro = int(suministro)
        anho = int(anho)
        mes = int(mes)

        if (mes >= 1 and mes <= 12):
            return False, 'mes incorrecto', None, None, None
    except ValueError:
        return False, 'no numericos', None, None, None
    
    return True, 'ok', suministro, anho, mes

def validar_y_separar(texto):
    valores = texto.split(',')
    
    # Verificar si hay exactamente tres valores
    if len(valores) != 3:
        return None, 'no son 3 valores', False

    # Intentar convertir los valores a números
    suministro = valores[0].strip()
    anho = valores[1].strip()
    mes = valores[2].strip()

    flag_valid_param, mensaje_valid_param, suministro, anho, mes = validar_parametros_como_numero(suministro, anho, mes)

    if (flag_valid_param):
        return True, mensaje_valid_param, [suministro, anho, mes]
    else:
        return False, mensaje_valid_param, None

def get_url_recibo(suministro, anho, mes):
    url_busqueda = sett.busqueda_url
    link_enel_consulta = url_busqueda + str(suministro) +'&company=0&dtmId=consult'

    response = urllib.request.urlopen(link_enel_consulta)

    data = json.loads(response.read())

    if (len(data) > 6):
        data = data['invoiceList']

        for i in data:
            i_mes = i['issueDate'][3:5]
            i_anho = i['issueDate'][6:]

            if((('0000' + anho)[0:4] == i_anho) and (('00' + mes)[0:2] == i_mes)):

                pdflink = i['pdfLink']

                if (len(pdflink) > 100):
                    return True, 'recibo esta en la web', pdflink
                else:
                    return False, 'suministro existe, recibo no tiene link', ''

        return False, 'suministro existe, recibo no esta en la web', ''
    else:
        return False, 'suministro no existe', ''
    
def administrar_envio_recibo(number, suministro, anho, mes):
    flag_url, respuesta_url, document_url = get_url_recibo(suministro, anho, mes)

    print("administrar_envio_recibo: get_url_recibo --> flag_url = " + str(flag_url) + ", respuesta_url = " + str(respuesta_url) + ", document_url =" + str(document_url))

    mensaje_envio_recibo = ''

    if(flag_url):
        mensaje_envio_recibo = document_Message(number, document_url, "Listo!!!", "recibo_" + str(suministro) + "_" + str(anho) + "_" + str(mes) + ".pdf")
    else:
        texto_ = 'suministro = ' + suministro + ', año =' + anho + ', mes =' + mes + '; presenta el error "' + respuesta_url + '"'
                
        mensaje_envio_recibo = text_Message(number, texto_)
    
    print("administrar_envio_recibo: correcto")

    return mensaje_envio_recibo

def obtener_media_info(media_id):
    url_info = f'https://graph.facebook.com/v17.0/{media_id}?phone_number_id={sett.whatsapp_phone_number_id}'
    headers = {'Authorization': 'Bearer ' + sett.whatsapp_token}

    try:
        response = requests.get(url_info, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f'obtener_media_info: http error {e} ')
        return None
    except Exception as e:
        print(f'obtener_media_info: Otros error {e}')
        return None
    
    print('obtener_media_info: correcto')
    return response.json()

def es_media_type_permitida(mime_type):
    return mime_type in sett.media_types

def borrar_media_directorio(directory):
    if not os.path.exists(directory):
        #directorio no existe
        return
    
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'borrar_media_directorio: Error al borrar {file_path} razon {e}')

def descargar(media_url, file_path):
    headers = {'Authorization': 'Bearer ' + sett.whatsapp_token}
    try:
        response = requests.get(media_url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f'descargar: http error {e} ')
        return False
    except Exception as e:
        print(f'descargar: Otros error {e}')
        return False
    
    with open(file_path, 'wb') as f:
        f.write(response.content)

    return True

def administrar_descarga(media_id, number, filename_number):
    # 1. obtenemos la metadata del archivo que subio el usuario
    media_info = obtener_media_info(media_id)

    if media_info is None:
        return False, 'error al obtener metadata', '', ''
    
    # 2. conseguimos la url de esa metadata y el tipo doc
    media_url = media_info.get('url')
    mime_type = media_info.get('mime_type')
    
    # 3. validamos si es un tipo de doc permitido
    if not es_media_type_permitida(mime_type):
        return False, f'tipo de archivo no permitido {mime_type}', '', ''
    
    # 4. configuramos el directorio donde se guardara el archivo
    ext = sett.media_types[mime_type]
    directory = f'media/{number}/{ext}'
    
    borrar_media_directorio(directory)

    os.makedirs(directory, exist_ok=True)
    filename = filename_number
    file_path = os.path.join(directory, filename + '.' + ext)

    # 5. descargamos el archivo
    if descargar(media_url, file_path):
        return True, 'archivo descargado, continuamos a procesar la información', file_path, ext
    else:
        return False, 'error al descargar archivo', '', ''

def administrar_chatbot(text, number, messageId, name, media_id, timestamp):
    pie_pagina = "Team Vive Lunahuana!!!"
    text = text.lower() #mensaje que envio el usuario
    list = []
    print("mensaje del usuario: ",text)

    markRead = markRead_Message(messageId)
    list.append(markRead)
    
    time.sleep(3)

    if "hola" in text:
        footer = pie_pagina

        # reaccion al mensaje
        #replyReaction = replyReaction_Message(number, messageId, "🫡")
        replyReaction = replyReaction_Message(number, messageId, ":)")
        enviar_Mensaje_whatsapp(replyReaction)
        time.sleep(2)
        
        # mensaje de inicio
        texto_ = '¡Hola! Soy Pdfito, quieres descargar el recibo de forma digital?'
        textMessage = text_Message(number, texto_)
        enviar_Mensaje_whatsapp(textMessage)
        
        time.sleep(2)
        
        # lista de opciones
        body = 'Hay 2 formas de realizar este pedido:'

        footer = pie_pagina

        options = ["Por nro. suministro", "Por archivos csv"]

        replyButtonData = buttonReply_Message(number, options, body, footer, "sed1", messageId)

        enviar_Mensaje_whatsapp(replyButtonData)

    elif "Por nro. suministro" in text:
        # mensaje
        texto_ = 'Para poder procesar esta información necesito que me envies los siguientes datos en este orden:\n\n' \
                 'suministro, año, mes\n\n' \
                 'Por ejemplo si quieres el recibo del suministro "123456 del mes de agosto del 2023" debes de enviarnos solo esta información:\n\n'\
                 '123456, 2023, 8'
        
        textMessage = text_Message(number, texto_)
        enviar_Mensaje_whatsapp(textMessage)

    elif "Por archivos csv" in text:
        # mensaje
        texto_ = 'Para poder procesar esta información necesito que subas el archivo csv el cual debe de tener el siguiente formato de cabeceras:\n\n' \
                 'suministro, anho, mes\n\n' \
                 'En ese mismo orden.'

        textMessage = text_Message(number, texto_)
        enviar_Mensaje_whatsapp(textMessage)

    # 2. si sube un archivo pdf
    # 2.1 procedemos a descargar el archivo localmente
    # 2.2 preguntamos que desea consultar
    elif media_id != '':
        print("administrar_chatbot: media_id = " + str(media_id))

        flag_descarga, mensaje_descarga, filepath_descarga, ext = administrar_descarga(media_id, number, str(number))
        textMessage = text_Message(number, mensaje_descarga)
        enviar_Mensaje_whatsapp(textMessage)
        time.sleep(2)

        if(flag_descarga):
            if ext in ['csv', 'txt']:
                df_lista = pd.read_csv(filepath_descarga)
            else:
                df_lista = pd.read_excel(filepath_descarga)

            for i, j in df_lista.iterrows():

                p_suministro = j['suministro']
                p_anho = j['anho']
                p_mes = j['mes']

                flag_valid_param, mensaje_valid_param, suministro, anho, mes = validar_parametros_como_numero(p_suministro, p_anho, p_mes)

                if flag_valid_param:

                    textMessage = administrar_envio_recibo(number, suministro, anho, mes)

                else:
                    texto_ = 'suministro = ' + p_suministro + ', año =' + p_anho + ', mes =' + p_mes + '; presenta el error "' + mensaje_valid_param + '"'
            
                    textMessage = text_Message(number, texto_)
                
                enviar_Mensaje_whatsapp(textMessage)

                time.sleep(3)

    elif "gracias" in text:
        textMessage = text_Message(number,"Excelente! no dudes en escribirme. ¡Hasta luego! 😊")
        enviar_Mensaje_whatsapp(textMessage)
    else :
        flag_val_y_sep, respuesta, lista  = validar_y_separar(text)

        print("administrar_chatbot: validar_y_separar: flag_validar_y_separar = " + str(flag_val_y_sep) + ", respuesta = " + str(respuesta) + ", lista = " + str(lista)  )

        if(flag_val_y_sep):
            texto_ = 'Excelente, dame unos segundos y lo proceso.'            
            
            textMessage = text_Message(number, texto_)
            
            enviar_Mensaje_whatsapp(textMessage)
            
            time.sleep(3)

            suministro = lista[0]
            anho = lista[1]
            mes = lista[2]

            textMessage = administrar_envio_recibo(number, suministro, anho, mes)
                     
            enviar_Mensaje_whatsapp(textMessage)

        else:
            if (respuesta == 'no son 3 valores') :
                texto_ = 'Hola, debes de ingresar tres valores numericos que corresponde a:\n\n' \
                        'suministro, año, mes\n\n' \
                        'Por ejemplo si quieres el recibo del suministro "123456" del mes de agosto del 2023 debes de enviarnos solo esta información:\n\n'\
                        '123456, 2023, 8\n\n'\
                        'Vuelve a enviar todos los valores nuevamente por favor.'
                
                textMessage = text_Message(number, texto_)

                enviar_Mensaje_whatsapp(textMessage)

            if (respuesta == 'mes incorrecto') :
                texto_ = 'Los valores agregados estan casi correctos, recuerda que los meses estan en el rango de 1 al 12.\n\n' \
                        'Por ejemplo si quieres el recibo del suministro "123456" del mes de agosto del 2023 debes de enviarnos solo esta información:\n\n'\
                        '123456, 2023, 8\n\n'\
                        'Vuelve a enviar todos los valores nuevamente por favor.'
                
                textMessage = text_Message(number, texto_)

                enviar_Mensaje_whatsapp(textMessage)

            if (respuesta == 'no numericos') :
                body = '¡Hola!, no te entendí tu pregunta, mi función es solo para decargar recibos en forma digital.\n\n'\
                        'Hay 2 formas de realizar este pedido:'

                footer = pie_pagina

                options = ["Por nro. suministro", "Por archivos csv"]

                replyButtonData = buttonReply_Message(number, options, body, footer, "sed1", messageId)

                enviar_Mensaje_whatsapp(replyButtonData)
            
    time.sleep(3)

    for item in list:
        enviar_Mensaje_whatsapp(item)

#al parecer para mexico, whatsapp agrega 521 como prefijo en lugar de 52,
# este codigo soluciona ese inconveniente.
def replace_start(s):
    if s.startswith("521"):
        return "52" + s[3:]
    else:
        return s