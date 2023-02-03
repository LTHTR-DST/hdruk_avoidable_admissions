import requests
import requests_cache

class FHIRTermClient:
    def __init__(self, fhir_url, client_id=None, client_secret=None, token_url=None, cache_backend=None):
        self.fhir_url = fhir_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.cache_backend = cache_backend
        self.session = requests.Session()
        self.token_url = token_url

        if cache_backend is not None:
            print('setting up caching')
            self.session = requests_cache.CachedSession('demo_cache', backend=cache_backend)
        else:
            print('not setting up caching')
            self.session = requests.Session()
        if client_id is not None:
            print('setting up authorisation')
            bearer_token = self.get_access_token()
            self.session.headers.update({'Authorization': 'Bearer' + bearer_token})

    def get_access_token(self):
        response = requests.post(
            self.token_url,
            data={"grant_type": "client_credentials"},
            auth=(self.client_id, self.client_secret),
        )
        return response.json()["access_token"]


    def map_code(self, map_url, src_code, src_system, tgt_system):
        # map a code and return full response of all maps of all types
        jsonResponse = None
        response = self.session.get(self.fhir_url + '/ConceptMap/$translate', params={"code": src_code,"url": map_url,"system": src_system,"target": tgt_system})
        if response.status_code != 200:
            print(response.text)
            print(response.status_code)
        else:
            jsonResponse = response.json()
        return jsonResponse

    def map_code_simple_one2one(self, map_url, src_code, src_system, tgt_system):
        # convenience example only for use where you know the map will only give zero or one result and you don't care about the mapping relationship
        jsonResponse = self.map_code(map_url, src_code, src_system, tgt_system)
        map_result = jsonResponse['parameter'][0]['valueBoolean']
        if map_result is True:
            return jsonResponse['parameter'][1]['part'][1]['valueCoding']['code']
        else:
            return None
