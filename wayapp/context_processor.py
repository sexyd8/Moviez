from .models import  *

    
def dropdown(request):
    categories = Category.objects.all()

    context = {
        'categories':categories
    }

    return context
    


def member(request):
    member = Member.objects.all()

    context = {
        'member':member
    }

    return context



# def upgrade(request):
#     upgrade = Member.objects.exclude(title='Wood')

#     context = {
#         'upgrade':upgrade
#     }

#     return context


# def downgrade(request):
#     downgrade = Member.objects.exclude(title='Diamond')

#     context = {
#         'downgrade':downgrade
#     }

#     return context
