from django.contrib import admin
from profiles.models import (
    Language,
    LookingFor,
    PersonalInterest,
    ProfessionalInterest,
)

# Register your models here.
admin.site.register(Language)
admin.site.register(LookingFor)
admin.site.register(PersonalInterest)
admin.site.register(ProfessionalInterest)
