import json
from jose import jwt
from urllib.request import urlopen

token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImctT2g2c3FGZ21DcERMc0NJN21IZyJ9.eyJpc3MiOiJodHRwczovL2Rldi05b29uZWN5dC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWZiZjMwMDgxYTc1NTAwMDc2MDQ2MDk2IiwiYXVkIjoiYnVnVHJhY2tlciIsImlhdCI6MTYwNjM2NjEyNywiZXhwIjoxNjA2MzczMzI3LCJhenAiOiIyUW85Tk1aQlNxZmRJdm14NU9laDJ2MEFHVEtMNjFiQiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOltdfQ.bVlAN0G7XorHHvtqLS9nh2M8uNRjOQQN_4lzgWw-0LDm3znYy7CsF7QYPzMoj2dg7E_nesbpKbHfCI_dUOjREmMDnRN3Jqg-GN2IhtM2jfW8rFbu8dT3wzgrJ6BmLtdZfstGbL3H_GoH3-WoQZ7Cvk59WgwXv5N46n8aHGTYDWgKOj89kPorRYtQde91CBu9sON0jCSzuv0231WS5H7JWb96FrYX2HVfOFYx_2qtbDvGOiHl-TJimJT06NHGRCsL074UcOorBmMyKwT61tCJiY1iZlOaj_FNGl26l3rH2bUyJocDdb4cGwxO8E8Ko4Y9C4Gbt-EQBSZgFF9dl-XvnA'

ALGORITHMS=['RS256']
API_AUDIENCE = 'bugTracker'
AUTH0_DOMAIN = 'dev-9oonecyt.us.auth0.com'


jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
jwks = json.loads(jsonurl.read())
unverified_header = jwt.get_unverified_header(token)
rsa_key = {}

for key in jwks['keys']:
    if key['kid'] == unverified_header['kid']:
        rsa_key = {
            'kty': key['kty'],
            'kid': key['kid'],
            'use': key['use'],
            'n': key['n'],
            'e': key['e']
        }


payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

print(payload)
