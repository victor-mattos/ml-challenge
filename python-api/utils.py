

import requests
import pandas as pd
from typing import List

def get_access_dict():

    from settings import APP_ID, SECRET_KEY, CODE_ID, URI_REDIRECT, STATE 

    # URL da API
    url = "https://api.mercadolibre.com/oauth/token"

    # Dados do corpo da requisição
    payload = {
        "grant_type": "authorization_code",
        "client_id": APP_ID,  # Substitua pelo seu APP_ID
        "client_secret": SECRET_KEY,  # Substitua pelo seu SECRET_KEY
        "code": CODE_ID,  # Código de autorização gerado
        "redirect_uri": URI_REDIRECT # Sua URI de redirecionamento
        }

    # Cabeçalhos da requisição
    headers = {
        "accept": "application/json",
        "content-type": "application/x-www-form-urlencoded"
    }

    # Enviar a requisição POST
    response = requests.post(url, data=payload, headers=headers)

    access_dict = response.json()

    return access_dict

def refresh_access_token(refresh_token):

    from settings import APP_ID, SECRET_KEY, CODE_ID, URI_REDIRECT
    # URL for the token endpoint
    url = "https://api.mercadolibre.com/oauth/token"

    # Payload for the refresh token request
    payload = {
        "grant_type": "refresh_token",
        "client_id": APP_ID,
        "client_secret": SECRET_KEY,
        "refresh_token": refresh_token
    }

    # Headers for the request
    headers = {
        "accept": "application/json",
        "content-type": "application/x-www-form-urlencoded"
    }

    # Send the POST request to refresh the token
    response = requests.post(url, data=payload, headers=headers)
    new_access_dict = response.json()

    # Add the expiration time to the new_access_dict
    # new_access_dict['expires_at'] = time.time() + new_access_dict['expires_in']
    return new_access_dict

###################################################################
###################################################################

def get_df_listed_items_by_name(item_name:str,total_itens:int=50,verbose:bool=False)->pd.DataFrame:


    from settings import AUTHORIZATION_DICT

    headers = {
        'Authorization': f'Bearer {AUTHORIZATION_DICT["access_token"]}',
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

        url_search = f"{base_url}?q={item_name}&limit={50}&offset={offset}"
        
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

###################################################################
###################################################################

def get_df_listed_items_by_item_list(item_list:List[str], total_itens:int=50)->pd.DataFrame:

    from settings import AUTHORIZATION_DICT

    headers = {
        'Authorization': f'Bearer {AUTHORIZATION_DICT["access_token"]}',
        'Content-Type': 'application/json'
    }

    df = pd.DataFrame()

    for item in item_list:

        df_aux = get_df_listed_items_by_name(item_name = item, total_itens = total_itens)

        df = pd.concat([df, df_aux])

    return df

###################################################################
###################################################################

def get_df_item_by_item_id(item_id: str, verbose:bool=False) -> pd.DataFrame:
    from settings import AUTHORIZATION_DICT


    headers = {
        'Authorization': f'Bearer {AUTHORIZATION_DICT["access_token"]}',
        'Content-Type': 'application/json'
    }

    # Base URL for the item details API
    base_url = f"https://api.mercadolibre.com/items/{item_id}"

    if verbose:
        print(f"    ### Getting info for item {item_id}")

    response = requests.get(url=base_url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to fetch data: {response.status_code} - {response.text}")
        return pd.DataFrame()  

    item = response.json()

    filtered_item = filter_dict_for_dataframe(item)

    df = pd.DataFrame([filtered_item])
    
    return df

###################################################################
###################################################################

def filter_dict_for_dataframe(item: dict) -> dict:

    filtered_item = {}
    for key, value in item.items():
        if not isinstance(value, (dict, list)):
            filtered_item[key] = value
    return filtered_item


###################################################################
###################################################################


def get_batch_df_items_by_item_ids(item_ids: List[str]) -> pd.DataFrame:
    from settings import AUTHORIZATION_DICT

    # Headers for the API request
    headers = {
        'Authorization': f'Bearer {AUTHORIZATION_DICT["access_token"]}',
        'Content-Type': 'application/json'
    }

    # Base URL for the batch items API
    base_url = "https://api.mercadolibre.com/items"

    # Split item_ids into chunks of 20 (MercadoLibre's limit for batch requests)
    chunk_size = 20
    all_items = []

    for i in range(0, len(item_ids), chunk_size):
        # Get a chunk of item_ids
        chunk = item_ids[i:i + chunk_size]
        ids_param = ",".join(chunk)

        # Make the batch API request
        response = requests.get(url=f"{base_url}?ids={ids_param}", headers=headers)
        
        # Check if the request was successful
        if response.status_code != 200:
            print(f"Failed to fetch data: {response.status_code} - {response.text}")
            continue

        # Parse the JSON response
        items_data = response.json()

        # Filter each item to remove nested structures
        for item in items_data:
            if "body" in item and isinstance(item["body"], dict):
                filtered_item = filter_dict_for_dataframe(item["body"])
                all_items.append(filtered_item)

    # Convert the filtered items into a DataFrame
    df = pd.DataFrame(all_items)
    return df