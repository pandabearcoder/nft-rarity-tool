from django.contrib import admin

from .models import (
    Project,
    NFT,
    Attribute,
    Trait,
)


admin.site.register(Project)
admin.site.register(NFT)
admin.site.register(Attribute)
admin.site.register(Trait)
