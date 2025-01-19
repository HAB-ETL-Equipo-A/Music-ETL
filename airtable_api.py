import requests

class AirtableAPI:

    def __init__(self, app_id, access_token):

        self.app_id = app_id
        self._access_token = access_token

        self._headers = {
            "Authorization" : f"Bearer {self._access_token}",
            "Content-Type"  : "application/json"
        }

    def _get_response(self, url, headers, params):
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
    
        return response.json()

    def get_table_data(self, table_name, max_iter=50):
        
        table_endpoint = f"https://api.airtable.com/v0/{self.app_id}/{table_name}"
        
        records = []
        params = None

        for i in range(max_iter):
            data = self._get_response(table_endpoint, self._headers, params)
            records.extend(data['records'])
            
            if 'offset' in data:
                params = {'offset': data['offset']}
            else:
                break
                
        return [record['fields'] for record in records]
    