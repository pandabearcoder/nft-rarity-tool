from django.db import models


class Project(models.Model):
    contract_address = models.CharField(max_length=100)
    contract_abi = models.TextField()
    name = models.CharField(max_length=50)

    @property
    def nft_count(self):
        return self.nfts.count()

    def __str__(self):
        return self.name


class NFT(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='nfts',
    )
    nft_id = models.PositiveIntegerField()
    image_url = models.TextField()
    rarity_score = models.FloatField(null=True, default=None)
    rank = models.PositiveIntegerField(null=True)

    def __str__(self):
        return '{}: {}'.format(self.project.name, self.nft_id)


class Attribute(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='attributes'
    )
    name = models.CharField(max_length=50)
    value = models.CharField(max_length=100)

    def __str__(self):
        return '{}: {}'.format(self.name, self.value)


class Trait(models.Model):
    nft = models.ForeignKey(
        NFT,
        on_delete=models.CASCADE,
        related_name='nft_attributes',
    )
    attribute = models.ForeignKey(
        Attribute,
        on_delete=models.CASCADE,
        related_name='traits',
    )
    rarity_score = models.FloatField(null=True, default=None)
