from django.db import models


class ScenicType(models.Model):
    typeId = models.AutoField(primary_key=True, verbose_name='类型id')
    typeName = models.CharField(max_length=20, default='', verbose_name='类别名称')

    class Meta:
        db_table = 't_ScenicType'
        verbose_name = '景区类型信息'
        verbose_name_plural = verbose_name

    def getJsonObj(self):
        scenicType = {
            'typeId': self.typeId,
            'typeName': self.typeName,
        }
        return scenicType

