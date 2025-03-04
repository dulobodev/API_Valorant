import requests
import base64

class Authorization:
    def __init__(self, lockfile_path, name, tagline):
        self.lockfile_path = lockfile_path
        self.name = name
        self.tagline = tagline
        self.access_token = None
        self.token = None
        self.puuid = None
        self._read_lockfile()
        self._get_tokens()

    # a porta, senha, e outras informacoes necessarias para resgatar os tokens, estao em um file do jogo, essa funcao ira ler o arquivo, pegar a porta e senha
    def _read_lockfile(self): 
        try:
            with open(self.lockfile_path, 'r') as f:
                content = f.read().strip()
            lockfile_parts = content.split(":")
            self.port = lockfile_parts[2]
            self.password = lockfile_parts[3]
        except Exception as e:
            print(f"Erro ao ler o lockfile: {e}")
            self.port = None
            self.password = None

    # funcao para resgatar tokens necessarios, utilizando a senha descriptografada e a porta passada no arquivo
    def _get_tokens(self):
        if not self.port or not self.password: # caso nao tenha a porta e senha, nao funcionara o codigo
            return
        
        auth_value = f"riot:{self.password}"
        encoded_auth_value = base64.b64encode(auth_value.encode()).decode() # descriptografia da senha para funcionar o request
        url = f"https://127.0.0.1:{self.port}/entitlements/v1/token"
        headers = {"Authorization": f"Basic {encoded_auth_value}"}

        
        '''o token de acesso e uma senha de muitos caracteres e numeros, como sao passados em formato de dicionarios, 
        lemos a parte do dicionario onde estao os dois tokens e armazenamos nas duas variaveis.
        '''
        try:
            response = requests.get(url, headers=headers, verify=False)
            if response.status_code == 200:
                conteudo_json = response.json()
                self.access_token = conteudo_json["accessToken"] 
                self.token = conteudo_json["token"]
            else:
                print(f"Erro na requisição: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Erro ao tentar se conectar: {e}")

    # essa funcao pega um id especial da riot que cada usuario tem, ele e utilizado nas requisicoes, estamos armazenando o puuid em self.puuid
    def get_puuid(self):
        auth_value = f"riot:{self.password}"
        encoded_auth_value = base64.b64encode(auth_value.encode()).decode()
        url = f"https://127.0.0.1:{self.port}/player-account/aliases/v1/lookup?gameName={self.name}&tagLine={self.tagline}"
        headers = {"Authorization": f"Basic {encoded_auth_value}"}

        try:
            response = requests.get(url, headers=headers, verify=False)
            if response.status_code == 200:
                filter_puuid =  response.json()
                self.puuid = filter_puuid[0]['puuid']
            else:
                print(f"Erro na requisição: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Erro ao tentar se conectar: {e}")
    
    