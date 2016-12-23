
# Your Paddle public key.
public_key = '''-----BEGIN PUBLIC KEY-----
MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAvnnj0l6/aVaUrjTHo+LL
ZFjlkCuWEqCIaTk9zaft0reIpkeGyAmNiUgCMk3uJa++4BBao5QzfbyZ2BhaOFrh
DGccVEkUOOUvViD5nSAPMRbJCXF6d0JllXpuaYLfvqlwcxUdlMJb2XZrHcTUcvJz
bekzoLs04C1d3EC1Qcxn61gqLM4SqVTL1lAnZ9anj1KkEd8X0qfV/jTaufCFDYBC
6/PhsM35fLpBT6l7SbU7EGwqlSDO8UipFeeMb4FRps28vB4r6nQfaJVarJvXof8Z
nRmnq7Cd7vHqoxyH9Ra0NXOSEKwlMerSK6Qb7fQwHRE7agQEWegsufAUgrUmw3Ks
2MwJuQ763KBHBqhkNwONRRKWNF/k808l5QtsvuD/lS770KPY+fp/LU7qLt02Af07
lmd99ka15awlSfZ6fmmfzhy4j04fbeq9Z2yjqLZ2WZ43kHgQu/YKfwygiXRvG5b7
VvJ7Tx17XRHXpU+7gAKlIZEXrBeqxYg10Mp+fH/oBLjzCnOcdMKSyMOizLEGmFTR
gqnicWonXgbpH7beHJ2dUPZtJAnA1Q4Tsz6xTI9WkiwJ+SbwFalB4LF7FnTmp7Pq
cabmxogHMATVe2j8zf529J9B3MKCaHNCNh99zdiy2JlIgPlPbMTYq7lkrlt6Dn+l
X1skTX8d1Ba8MZywkk7O8f8CAwEAAQ==
-----END PUBLIC KEY-----'''

import collections
import base64

# Crypto can be found at https://pypi.python.org/pypi/pycrypto
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
import hashlib

# PHPSerialize can be found at https://pypi.python.org/pypi/phpserialize
import phpserialize

# Convert key from PEM to DER - Strip the first and last lines and newlines, and decode
public_key_encoded = public_key[26:-25].replace('\n', '')
public_key_der = base64.b64decode(public_key_encoded)


def verify(data):
    # input_data represents all of the POST fields sent with the request
    # Get the p_signature parameter & base64 decode it.
    input_data = {}
    for key in data:
        input_data[key] = data[key]
    signature = input_data['p_signature']

    # Remove the p_signature parameter
    del input_data['p_signature']

    # Ensure all the data fields are strings
    for field in input_data:
        input_data[field] = str(input_data[field])

    # Sort the data
    sorted_data = collections.OrderedDict(sorted(input_data.items()))

    # and serialize the fields
    serialized_data = phpserialize.dumps(sorted_data)

    # verify the data
    key = RSA.importKey(public_key_der)
    digest = SHA.new()
    digest.update(serialized_data)
    verifier = PKCS1_v1_5.new(key)
    signature = base64.b64decode(signature)
    if verifier.verify(digest, signature):
        return True
    else:
        return False
