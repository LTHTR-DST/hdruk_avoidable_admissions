# TODO: Document this module

import requests
import requests_cache
from pandas import json_normalize
from requests.exceptions import HTTPError


class FHIRTermClient:
    """Client to interact with a FHIR Terminology Server.

    See the following resources for more information.

    - API Docs: <https://ontoserver.csiro.au/docs/5.1/api-fhir.html>
    - <https://github.com/NHSDigital/TerminologyServer>
    - <https://ontology.nhs.uk/>

    Author: <https://github.com/dfleming9>
    """

    def __init__(
        self,
        fhir_url="https://ontology.nhs.uk/staging/fhir",
        client_id=None,
        client_secret=None,
        token_url=None,
        cache_backend="memory",
    ):
        self.fhir_url = fhir_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.cache_backend = cache_backend
        self.session = requests.Session()
        self.token_url = token_url

        if cache_backend is not None:
            print("setting up caching")
            self.session = requests_cache.CachedSession(
                "demo_cache", backend=cache_backend
            )
        else:
            print("not setting up caching")
            self.session = requests.Session()

        if client_id is not None:
            print("setting up authorisation")
            bearer_token = self._get_access_token()
            self.session.headers.update({"Authorization": "Bearer " + bearer_token})

    def _get_access_token(self) -> str:
        try:
            response = requests.post(
                self.token_url,
                data={"grant_type": "client_credentials"},
                auth=(self.client_id, self.client_secret),
            )
            return response.json()["access_token"]
        except Exception as exc:

            raise HTTPError("Authentication failed.", *exc.args)

    def map_code(self, map_url, src_code, src_system, tgt_system):
        # map a code and return full response of all maps of all types
        jsonResponse = None
        response = self.session.get(
            self.fhir_url + "/ConceptMap/$translate",
            params={
                "code": src_code,
                "url": map_url,
                "system": src_system,
                "target": tgt_system,
            },
        )
        if response.status_code != 200:
            print(response.text)
            print(response.status_code)
        else:
            jsonResponse = response.json()
        return jsonResponse

    def map_code_simple_one2one(self, map_url, src_code, src_system, tgt_system):
        # convenience example only for use where you know the map will only give
        # zero or one result and you don't care about the mapping relationship
        jsonResponse = self.map_code(map_url, src_code, src_system, tgt_system)
        print(jsonResponse)
        map_result = jsonResponse["parameter"][0]["valueBoolean"]
        if map_result is True:
            return jsonResponse["parameter"][1]["part"][1]["valueCoding"]["code"]
        else:
            return None

    def expand_valueset(self, vs_url: str) -> dict:

        jsonResponse = None
        response = self.session.get(
            self.fhir_url + "/ValueSet/$expand",
            params={"url": vs_url, "property": "category"},
        )
        if response.status_code != 200:
            raise HTTPError(
                f"Error retrieving valueset. HTTP Status: {response.status_code}; {response.text}"
            )
        else:
            jsonResponse = response.json()
            print("Expansion contains: " + str(jsonResponse["expansion"]["total"]))

        return jsonResponse

    def expand_valueset_to_list(self, vs_url: str) -> list:
        """Retrieve members of a valueset as a complete JSON response.

        For refsets, `vs_url` should be {{base_url}}?fhir_vs=refset/[sctid]

        e.g. http://snomed.info/sct?fhir_vs=refset/999003051000000109

        See https://ontoserver.csiro.au/docs/5.1/api-fhir.html and
        https://ontoserver.csiro.au/docs/5.1/api-fhir.html#Value_Set
        for more details on constructing `vs_url`.

        Args:
            vs_url (str): e.g. http://snomed.info/sct?fhir_vs=refset/[sctid]

        Returns:
            list: List of members of valueset
        """

        response = self.expand_valueset(vs_url)
        df_json_concepts = json_normalize(response["expansion"]["contains"])

        return df_json_concepts["code"].tolist()

    def validate_code(self, vs_url, code, system):
        # validate
        jsonResponse = None
        response = self.session.get(
            self.fhir_url + "/ValueSet/$validate-code",
            params={"url": vs_url, "code": code, "system": system},
        )
        if response.status_code != 200:
            print(response.text)
            print(response.status_code)
        else:

            jsonResponse = response.json()
            validation_result = jsonResponse["parameter"][0]["valueBoolean"]
            # print(validation_result)
        return validation_result
