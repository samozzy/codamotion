import os 
# This is here as a 'just in case' and is not currently used
class PublicAzureStorage(AzureStorage):
    account_name = os.environ.get('AZURE_STORAGE_ACCOUNT_NAME')
    account_key = os.environ.get('AZURE_STORAGE_ACCOUNT_KEY')
    azure_container = os.environ.get('AZURE_STORAGE_CONTAINER')
    expiration_secs = None