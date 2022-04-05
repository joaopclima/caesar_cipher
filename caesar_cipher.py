import requests, json, sys, hashlib

def get_json(url):
    try:
        return requests.get(url = url).json()
    except:
        print("Oooops! Problems trying to get the JSON from the server.\n{}".format(sys.exc_info()[0]))
        return 1
    
def save_json_to_file(json_returned, file_path):
    try:
        with open(file_path, "w") as outfile:  
            json.dump(json_returned, outfile, indent=1)
        outfile.close()
    except:
        print("Oooops! Problems while trying to save the JSON file.\n{}".format(sys.exc_info()[0]))
        return 1
    return 0

def read_file(file_path):
    try:
        with open(file_path) as json_file:  
            loaded_json = json.load(json_file)      
        json_file.close()
    except:
        print("Oooops! Problems while trying to load the JSON file.\n{}".format(sys.exc_info()[0]))
        return 1
    return loaded_json

def update_json(loaded_json, field, text):
    try:    
        loaded_json[field] = text
        save_json_to_file(loaded_json, file_path)
    except:
        print("Oooops! Problems trying to update update the JSON.\n{}".format(sys.exc_info()[0]))
        return 1
    return 0

def decypher_message(overhead, message, letters_mapping):
    decyphered_message = ""
    try:
        for letter in message:
            if(letter in letters_mapping):
                decyphered_position = (letters_mapping.index(letter) - overhead)%26
                decyphered_message += letters_mapping[decyphered_position]
            elif(letter == " "):
                decyphered_message += " "
            else:
                decyphered_message += format(letter)
    except:
        print("Oooops! Problems while trying to generate the Decyphered message.\n{}".format(sys.exc_info()[0]))
        return 1
    return decyphered_message

def generate_sha1(decyphered_message):
    try:
        result_sha1 = hashlib.sha1(decyphered_message.encode()) 
    except:
        print("Oooops! Problems while trying to generate the SHA1 hash.\n{}".format(sys.exc_info()[0]))
        return 1
    return result_sha1.hexdigest()

def send_result_to_codenation(url_post, file_path):
    try:
        files = {"answer": open(file_path, "rb")}
        request_return = requests.post(url = url_post, files = files)
        if(request_return.status_code == 200):
            print("Answer successfully sent!\n{}".format(request_return._content))
        else:
            print(requests.Request('POST', url_post, files=files).prepare().body.decode('utf8'))
    except:
        print("Oooops! Problems while trying to send the file to codenation.\n{}".format(sys.exc_info()[0]))
        return 1
    return 0
    
if __name__ == "__main__":
    url_get = "https://api.codenation.dev/v1/challenge/dev-ps/generate-data?token=12818de9bd8ad7cba554de3c9e391a3363311a6f"
    url_post = "https://api.codenation.dev/v1/challenge/dev-ps/submit-solution?token=12818de9bd8ad7cba554de3c9e391a3363311a6f"
    file_path = "answer.json"
    letters_mapping = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    json_returned = get_json(url_get)
    save_json_to_file(json_returned, file_path)
    decyphered_message = decypher_message(json_returned["numero_casas"], json_returned["cifrado"], letters_mapping)
    loaded_json = read_file(file_path)
    update_json(loaded_json, "decifrado", decyphered_message)
    sha1_message = generate_sha1(decyphered_message)
    loaded_json = read_file(file_path)
    update_json(loaded_json, "resumo_criptografico", sha1_message)
    send_result_to_codenation(url_post, file_path)