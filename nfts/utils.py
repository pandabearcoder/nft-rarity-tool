import requests
from web3.main import Web3

from django.conf import settings

from .models import Project, NFT, Attribute, Trait


def fetch_nft_uri(contract, token_id):
    uri = contract.functions.tokenURI(token_id).call()
    return uri


def fetch_nft_data(uri):
    """
        uri: ipfs url. eg. ipfs://QmeSjSinHpPnmXmspMjwiXyN6zS4E9zccariGR3jxcaWtq/7575
    """
    base_url = 'https://ipfs.io/ipfs/{}'
    nft_uri = uri.split('://')[1]

    ipfs_api = base_url.format(nft_uri)
    response = requests.get(ipfs_api)
    data = response.json()
    return data


def bulk_fetch_nfts(project_id):
    project = Project.objects.get(pk=project_id)

    w3 = Web3(Web3.HTTPProvider(settings.INFURA_ENDPOINT))
    contract = w3.eth.contract(
        address=project.contract_address,
        abi=project.contract_abi
    )

    for i in range(0, 10):
        uri = fetch_nft_uri(contract, i)
        data = fetch_nft_data(uri)
        nft = NFT.objects.create(
            project=project,
            nft_id=i,
            image_url=data['image'].split('://')[1],
        )
        for attribute in data['attributes']:
            attribute, _ = Attribute.objects.get_or_create(
                project=project,
                name=attribute['trait_type'],
                value=attribute['value'],
            )
            Trait.objects.create(
                nft=nft,
                attribute=attribute,
            )
