import requests
import json
import string
import hashlib

def get_encrypted_message(url):

    response = requests.get(url)

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None
    
def decrypt_message(encrypted_message, numero_casas):
    alphabet = list(string.ascii_lowercase)
    encrypted_list = list(encrypted_message)
    decrypted_list = []

    for c in encrypted_list:
        if c.isalpha():
            for a in alphabet:
                if c == a:
                    if (ord(c) - numero_casas) < ord('a'):
                        i = numero_casas - 1
                        temp = ord(c)
                        while temp > ord('a'):
                            temp -= 1
                            i -= 1
                        decrypted_list.append(chr(ord('z') - i))
                    else:
                        decrypted_list.append(chr(ord(c) - numero_casas))
        else:
            decrypted_list.append(c)
    
    decrypted_message = ''.join(decrypted_list)
    return decrypted_message

api_token = "508efda55a19dbe2630d67d522fbd195604ba71a"
api_url_get = "https://api.codenation.dev/v1/challenge/dev-ps/generate-data?token={0}".format(api_token)

encrypted_message = get_encrypted_message(api_url_get)

if encrypted_message is not None:
    with open('answer.json', 'w') as answer:
        json.dump(encrypted_message, answer)
    numero_casas = encrypted_message['numero_casas']
    cifrado = encrypted_message['cifrado'].lower()
    decifrado = decrypt_message(cifrado, numero_casas)
    encrypted_message['decifrado'] = decifrado
    resumo = hashlib.sha1(encrypted_message['decifrado'].encode('utf-8')).hexdigest()
    encrypted_message['resumo_criptografico'] = resumo
    with open('answer.json', 'w') as answer:
        json.dump(encrypted_message, answer)
        
    api_url_post = "https://api.codenation.dev/v1/challenge/dev-ps/submit-solution?token={0}".format(api_token)
    file = {'answer': open('answer.json', 'rb')}
    response = requests.post(api_url_post, files=file)
    response.text
else:
    print('Solicitação inválida')