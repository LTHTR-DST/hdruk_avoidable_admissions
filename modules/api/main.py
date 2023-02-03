# This is a sample Python script.
import secrets, yaml, time
from FHIRTerminologyUtilites import FHIRTermClient

if __name__ == '__main__':
    print('Setting up some example FHIRTermClients with different settings')
    mapper_not_caching = FHIRTermClient(fhir_url='https://poc.dc4h.link/authoring/fhir')
    mapper_with_caching = FHIRTermClient(fhir_url='https://poc.dc4h.link/authoring/fhir', cache_backend='memory')
    #mapper_with_auth = FHIRTermClient(fhir_url='https://ontology.nhs.uk/staging/fhir', client_id=secrets.client_id, client_secret=secrets.client_secret, token_url='https://ontology.nhs.uk/authorisation/auth/realms/nhs-digital-terminology/protocol/openid-connect/token')
    #mapper_with_cache_and_auth = FHIRTermClient(fhir_url='https://ontology.nhs.uk/staging/fhir', cache_backend='memory', client_id=secrets.client_id, client_secret=secrets.client_secret, token_url='https://ontology.nhs.uk/authorisation/auth/realms/nhs-digital-terminology/protocol/openid-connect/token')

    print('Perform some example maps')

    print('mapper_not_caching')
    print(mapper_not_caching.map_code_simple_one2one('http://aec-ecds-icd10-experimental/cm', '37796009', 'http://snomed.info/sct', 'http://hl7.org/fhir/sid/icd-10-uk'))
    print('mapper_with_caching')
    print(mapper_with_caching.map_code_simple_one2one('http://aec-ecds-icd10-experimental/cm', '37796009', 'http://snomed.info/sct', 'http://hl7.org/fhir/sid/icd-10-uk'))
    #print('mapper_with_auth')
    #print(mapper_with_auth.map_code_simple_one2one('http://snomed.info/sct?fhir_cm=900000000000527005', '134811001', 'http://snomed.info/sct','http://snomed.info/sct'))
    #print('mapper_with_cache_and_auth')
    #print(mapper_with_cache_and_auth.map_code_simple_one2one('http://snomed.info/sct?fhir_cm=900000000000527005', '134811001', 'http://snomed.info/sct','http://snomed.info/sct'))

    print('load in some sample codes for mapping from ExampleCodes.yaml')
    with open('ExampleCodes.yaml', 'r') as file:
        map_source_codes = yaml.safe_load(file)


    print('Perform a set of mapping without using caching...')
    map_counter_uncached = 0
    start = time.time()
    for x in range(0,100):
        for src in map_source_codes['map_source_codes']:
            mapper_not_caching.map_code_simple_one2one('http://aec-ecds-icd10-experimental/cm', src['code'], src['system'], 'http://hl7.org/fhir/sid/icd-10-uk')
            map_counter_uncached += 1
    end = time.time()
    print()

    non_cached_elapsed = end - start

    print('Perform same set of mapping using caching')
    map_counter_cached = 0
    start = time.time()
    for x in range(0,100):
        for src in map_source_codes['map_source_codes']:
            mapper_with_caching.map_code_simple_one2one('http://aec-ecds-icd10-experimental/cm', src['code'], src['system'], 'http://hl7.org/fhir/sid/icd-10-uk')
            map_counter_cached += 1
    end = time.time()
    with_cache_elapsed = end - start
    print()

    print('Compare results ...')
    print('Single Threaded without caching: ' + str(map_counter_uncached) + ' in ' + str(non_cached_elapsed) + ' sec, at rate: ' + str(map_counter_uncached/non_cached_elapsed) + ' per sec')
    print('Single Threaded with caching: ' + str(map_counter_cached) + ' in ' + str(with_cache_elapsed) + ' sec, at rate: ' + str(map_counter_cached/with_cache_elapsed) + ' per sec')
