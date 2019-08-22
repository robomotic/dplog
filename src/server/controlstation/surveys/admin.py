from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import QuestionVirtual,ResponseVirtual,ClientVirtual
from .models import Question,Response,Client

admin.site.register(QuestionVirtual)
admin.site.register(ResponseVirtual)
admin.site.register(ClientVirtual)

admin.site.register(Question)
admin.site.register(Response)
admin.site.register(Client)
