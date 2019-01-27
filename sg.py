from django.db.models.signals import pre_init
import django.dispatch

def  f1(sender,signal,top,size):
    print("xxoo_callback")
    print(sender,signal)

# pre_init.connect(f1)

yinuo=django.dispatch.Signal(providing_args=['top','size'])

yinuo.connect(f1)