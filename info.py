from datetime import date
# AUTH0_CALLBACK_URL = 'https://bugtracker109-stage.herokuapp.com/callback'
# AUTH0_CLIENT_ID = '2Qo9NMZBSqfdIvmx5Oeh2v0AGTKL61bB'
# AUTH0_CLIENT_SECRET = 'YoMyvqDqWOP9IAWSv1HwQ_vjnK5wK_tJFDhRd0X39vkOy_Vfq7O78G84BWduc7nJ'
# AUTH0_DOMAIN = 'dev-9oonecyt.us.auth0.com'
# AUTH0_AUDIENCE = 'bugTracker'

AUTH0_CALLBACK_URL = 'http://127.0.0.1:5000/callback'
DATABASE_URL = 'postgresql://postgres:postgres@localhost:5432/trackbug'
AUTH0_CLIENT_ID = '9G8lEykzSilhzkP8Ww402w4OzGi846pO'
AUTH0_CLIENT_SECRET = 'GDGaLeZ-6PHxmaaqX4Wl4xLRVAf2_hLWQjmF8j5xyDLmoUxNZeBGVr3b-6PBfHIf'
AUTH0_DOMAIN = 'dev-9oonecyt.us.auth0.com'
AUTH0_AUDIENCE = 'bugTracker'

AUTH0_BASE_URL = 'https://' + AUTH0_DOMAIN
AUTH0_ALGORITHM = ['RS256']
PRIORITY = ['High','Low','Medium']
STATUS = ['open','closed','in-progress']
DATE = date.today().strftime("%d/%m/%Y")

