from tfl.client import Client
from tfl.api_token import ApiToken
import config

app_id = config.app_id
app_key = config.app_key
stationID = config.stationID

token = ApiToken(app_id, app_key)

client = Client(token)
print (client.get_lines(line_id="victoria")[0])