from django.db.models.signals import pre_init
import django.dispatch

def  f1(sender,signal,sql):

    with open("logs/sql.log","a",encoding="utf-8") as f:
        f.write("%s 耗时%s\n"%(sql.get("sql"),sql.get("time")))

# pre_init.connect(f1)

cmdb_log=django.dispatch.Signal(providing_args=['sql'])

cmdb_log.connect(f1)