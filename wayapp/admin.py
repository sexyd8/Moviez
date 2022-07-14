from django.contrib import admin
from . models import *

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'image','videofile')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','category','name','image','videofile','price','description','foreign','latest','local','wood','gold','diamond')
    list_editable = ['foreign','latest','local','wood','gold','diamond']

class CarouselAdmin(admin.ModelAdmin):
    list_display = ('image','comment')


class PaymentAdmin(admin.ModelAdmin):
    list_display=('id','user','title','amount','paid','first_name','last_name','phone')


class MemberAdmin(admin.ModelAdmin):
    list_display=('id','title','dfee')
    

class MembershipAdmin(admin.ModelAdmin):
    list_display=('id','profile','first_name','last_name','membership','phone','fee','pay_code',)
  

class ProfileAdmin(admin.ModelAdmin):
    list_display=('id','title','dfee','user','first_name','last_name','phone','email')




admin.site.register(Category,CategoryAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Carousel,CarouselAdmin)
admin.site.register(Payment,PaymentAdmin)
admin.site.register(Member,MemberAdmin)
admin.site.register(Membership,MembershipAdmin)
admin.site.register(Profile,ProfileAdmin)
