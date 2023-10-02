from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Users(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    birthday = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=11,
    )
    def __str__(self):
        return self.user.username
class file(models.Model):
    f_id=models.AutoField(primary_key = True)
    u_id=models.ForeignKey(Users,db_column='u_id', on_delete=models.CASCADE, null=True, blank=True)
    f_name=models.CharField(max_length=100)
    p_id=models.ForeignKey("file", db_column='p_id',on_delete=models.CASCADE, null=True, default=None ,blank=True)

class link_list(models.Model):
    l_id=models.AutoField(primary_key = True)
    u_id=models.ForeignKey(Users,db_column='u_id', on_delete=models.CASCADE)
    link=models.CharField(max_length=500)
    name=models.CharField(max_length=100)
    remark=models.CharField(max_length=100,default='none')
    p_id = models.ForeignKey(file, db_column='p_id',on_delete=models.CASCADE)

class mc(models.Model):
    u_id=models.ForeignKey(Users,db_column='u_id', on_delete=models.CASCADE)
    isf = models.BooleanField()
    isc = models.BooleanField()
    fid = models.IntegerField()