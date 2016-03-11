var path = require('path')
var jsf = require('json-schema-faker');
var fs = require('fs');

var BRANCH = process.env.ENV_VARIABLE || '1__0__0'

var record_schema = require(path.join(__dirname, '..', 'derefed-schemas', 'deref-' + BRANCH + '-100-record-package-schema.json'))
var record_generated = jsf(record_schema)
console.log('record_generated')
fs.writeFileSync(path.join(__dirname, '..', BRANCH + '_generated_record.json'), JSON.stringify(record_generated, undefined, 2))
console.log('record_writen')

var release_schema = require(path.join(__dirname, '..', 'derefed-schemas', 'deref-' + BRANCH + '-100-release-package-schema.json'))
var release_generated = jsf(release_schema)
console.log('release_generated')
fs.writeFileSync(path.join(__dirname, '..', BRANCH + '_generated_release.json'), JSON.stringify(release_generated, undefined, 2))
console.log('release_writen')

var bad_record_schema = require(path.join(__dirname, '..', 'derefed-schemas', 'deref-' + BRANCH + '-bad-record-package-schema.json'))
var bad_record_generated = jsf(bad_record_schema)
console.log('bad_record_generated')
fs.writeFileSync(path.join(__dirname, '..', BRANCH + '_bad_generated_record.json'), JSON.stringify(bad_record_generated, undefined, 2))
console.log('bad_record_writen')

var bad_release_schema = require(path.join(__dirname, '..', 'derefed-schemas', 'deref-' + BRANCH + '-bad-release-package-schema.json'))
var bad_release_generated = jsf(bad_release_schema)
console.log('bad_release_generated')
fs.writeFileSync(path.join(__dirname, '..', BRANCH + '_bad_generated_release.json'), JSON.stringify(bad_release_generated, undefined, 2))
console.log('bad_release_writen')

