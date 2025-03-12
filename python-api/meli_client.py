import requests
import pandas as pd
import time
from typing import List

class MeliAPI_Client:
    def __init__(self):


        from settings import APP_ID, SECRET_KEY, CODE_ID, URI_REDIRECT, AUTHORIZATION_DICT

        self.APP_ID = APP_ID
        self.SECRET_KEY = SECRET_KEY
        self.CODE_ID = CODE_ID
        self.URI_REDIRECT = URI_REDIRECT
        self.refresh_token = AUTHORIZATION_DICT['refresh_token']
        self.access_dict = self._refresh_access_token()

    def _get_access_dict(self):

        url = "https://api.mercadolibre.com/oauth/token"
        payload = {
            "grant_type": "authorization_code",
            "client_id": self.APP_ID,
            "client_secret": self.SECRET_KEY,
            "code": self.CODE_ID,
            "redirect_uri": self.URI_REDIRECT
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/x-www-form-urlencoded"
        }
        response = requests.post(url, data=payload, headers=headers)
        access_dict = response.json()
        access_dict['expires_at'] = time.time() + access_dict['expires_in']
        return access_dict

    def _refresh_access_token(self):

        url = "https://api.mercadolibre.com/oauth/token"
        payload = {
            "grant_type": "refresh_token",
            "client_id": self.APP_ID,
            "client_secret": self.SECRET_KEY,
            "refresh_token": self.refresh_token
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/x-www-form-urlencoded"
        }
        response = requests.post(url, data=payload, headers=headers)
        new_access_dict = response.json()
        new_access_dict['expires_at'] = time.time() + new_access_dict['expires_in']
        return new_access_dict

    def _get_valid_access_token(self):

        if time.time() >= self.access_dict['expires_at']:
            print("Access token expired. Refreshing token...")
            self.access_dict = self._refresh_access_token()
            print("Token refreshed successfully.")
        return self.access_dict['access_token']

    def get_df_listed_items_by_name(self, item_name: str, total_itens: int = 50, verbose: bool = False) -> pd.DataFrame:

        headers = {
            'Authorization': f'Bearer {self._get_valid_access_token()}',
            'Content-Type': 'application/json'
        }
        base_url = "https://api.mercadolibre.com/sites/MLA/search"
        limit = 50
        offset = 0
        all_items = []

        if verbose:
            print(f"### Searching for {item_name} in Mercado Livre")

        while offset < total_itens:
            if verbose:
                print(f"    ### Getting items from range {offset} to {offset + limit}")

            url_search = f"{base_url}?q={item_name}&limit={limit}&offset={offset}"
            res = requests.get(url=url_search, headers=headers)
            response_dict = res.json()
            items = response_dict.get("results", [])
            all_items.extend(items)
            offset += limit

            if len(items) < limit:
                break

        df = pd.DataFrame(all_items)
        if len(df) > total_itens:
            df = df.head(total_itens)

        if verbose:
            print(f"    ### Total of {len(df)} items found")

        return df

    def get_df_listed_items_by_item_list(self, item_list: List[str], total_itens: int = 50) -> pd.DataFrame:

        df = pd.DataFrame()
        for item in item_list:
            df_aux = self.get_df_listed_items_by_name(item_name=item, total_itens=total_itens)
            df = pd.concat([df, df_aux])
        return df

    def get_df_item_by_item_id(self, item_id: str, verbose: bool = False) -> pd.DataFrame:

        headers = {
            'Authorization': f'Bearer {self._get_valid_access_token()}',
            'Content-Type': 'application/json'
        }
        base_url = f"https://api.mercadolibre.com/items/{item_id}"

        if verbose:
            print(f"    ### Getting info for item {item_id}")

        response = requests.get(url=base_url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch data: {response.status_code} - {response.text}")
            return pd.DataFrame()

        item = response.json()
        filtered_item = self._filter_dict_for_dataframe(item)
        df = pd.DataFrame([filtered_item])
        return df

    def get_batch_df_items_by_item_ids(self, item_ids: List[str]) -> pd.DataFrame:

        headers = {
            'Authorization': f'Bearer {self._get_valid_access_token()}',
            'Content-Type': 'application/json'
        }
        base_url = "https://api.mercadolibre.com/items"
        chunk_size = 20
        all_items = []

        for i in range(0, len(item_ids), chunk_size):
            chunk = item_ids[i:i + chunk_size]
            ids_param = ",".join(chunk)
            response = requests.get(url=f"{base_url}?ids={ids_param}", headers=headers)
            if response.status_code != 200:
                print(f"Failed to fetch data: {response.status_code} - {response.text}")
                continue

            items_data = response.json()
            for item in items_data:
                if "body" in item and isinstance(item["body"], dict):
                    filtered_item = self._filter_dict_for_dataframe(item["body"])
                    all_items.append(filtered_item)

        df = pd.DataFrame(all_items)
        return df

    def _filter_dict_for_dataframe(self, item: dict) -> dict:
  
        filtered_item = {}
        for key, value in item.items():
            if not isinstance(value, (dict, list)):
                filtered_item[key] = value
        return filtered_item