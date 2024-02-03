from tfl.client import Client
from tfl.api_token import ApiToken

token = ApiToken(app_id, app_key)

client = Client(token)
print (client.get_line_meta_modes())
print (client.get_lines(mode="bus")[0])
print (client.get_lines(line_id="victoria")[0])