import jsonref
from jsonref import JsonRef
import json
import requests
import pprint
import requests_mock
import os

BRANCH = os.environ.get("BRANCH", '1__0__0')



release_package_url = 'https://raw.githubusercontent.com/open-contracting/standard/{}/standard/schema/release-package-schema.json'.format(BRANCH)
release_package_schema = requests.get(release_package_url).json()

record_package_url = 'https://raw.githubusercontent.com/open-contracting/standard/{}/standard/schema/record-package-schema.json'.format(BRANCH)
record_package_schema = requests.get(record_package_url).json()

release_url = 'https://raw.githubusercontent.com/open-contracting/standard/{}/standard/schema/release-schema.json'.format(BRANCH)
release_schema = requests.get(release_url).json()

versioned_release_url = 'https://raw.githubusercontent.com/open-contracting/standard/{}/standard/schema/versioned-release-validation-schema.json'.format(BRANCH)
versioned_release_schema = requests.get(versioned_release_url).json()


ref_release_url = record_package_schema['definitions']['record']['properties']['compiledRelease']['$ref']
ref_versioned_release_url = record_package_schema['definitions']['record']['properties']['versionedRelease']['$ref']



@requests_mock.Mocker()
def test_function(m):
    m.get('http://test.com', text='resp')
    return requests.get('http://test.com').text


class JsonRefEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, jsonref.JsonRef):
           return dict(obj)
        return json.JSONEncoder.default(self, obj)




def changeprops(object, mix_types=False):
    if isinstance(object, dict):
        object.pop('patternProperties', None)
        for key, value in list(object.items()):
            if key == 'type' and mix_types:
                if 'string' in object['type']:
                    object['type'] = ['string', 'integer']
                if 'integer' in object['type']:
                    object['type'] = ['string', 'integer']

            changeprops(value, mix_types)

deref_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'derefed-schemas') 

with requests_mock.Mocker() as m:
    m.get(ref_release_url, json=release_schema)
    m.get(ref_versioned_release_url, json=versioned_release_schema)
    unref_record_package_schema = JsonRef.replace_refs(record_package_schema)
    unref_release_package_schema = JsonRef.replace_refs(release_package_schema)

    with open(os.path.join(deref_directory, 'deref-{}-record-package-schema.json'.format(BRANCH)), "w+") as deref_record_package:
        deref_record_package.write(json.dumps(unref_record_package_schema, cls=JsonRefEncoder, indent=2))

    with open(os.path.join(deref_directory, 'deref-{}-release-package-schema.json'.format(BRANCH)), "w+") as deref_release_package:
        deref_release_package.write(json.dumps(unref_release_package_schema, cls=JsonRefEncoder, indent=2))

    with open(os.path.join(deref_directory, 'deref-{}-100-record-package-schema.json'.format(BRANCH)), "w+") as deref_record_package:
        changeprops(unref_record_package_schema)
        unref_record_package_schema['properties']['records']['minItems'] = 100
        unref_record_package_schema['properties']['records']['type'] = 'array'
        deref_record_package.write(json.dumps(unref_record_package_schema, cls=JsonRefEncoder, indent=2))

    with open(os.path.join(deref_directory, 'deref-{}-100-release-package-schema.json'.format(BRANCH)), "w+") as deref_release_package:
        unref_release_package_schema['properties']['releases']['minItems'] = 100
        unref_release_package_schema['properties']['releases']['type'] = 'array'
        deref_release_package.write(json.dumps(unref_release_package_schema, cls=JsonRefEncoder, indent=2))

    with open(os.path.join(deref_directory, 'deref-{}-bad-record-package-schema.json'.format(BRANCH)), "w+") as deref_record_package:
        changeprops(unref_record_package_schema, mix_types=True)
        deref_record_package.write(json.dumps(unref_record_package_schema, cls=JsonRefEncoder, indent=2))

    with open(os.path.join(deref_directory, 'deref-{}-bad-release-package-schema.json'.format(BRANCH)), "w+") as deref_release_package:
        changeprops(unref_release_package_schema, mix_types=True)
        deref_release_package.write(json.dumps(unref_release_package_schema, cls=JsonRefEncoder, indent=2))

