from django.db import models


class Province(models.Model):
    provinceId = models.AutoField(primary_key=True, verbose_name='省份id')
    provinceName = models.CharField(max_length=20, default='', verbose_name='省份名称')

    class Meta:
        db_table = 't_Province'
        verbose_name = '省份信息'
        verbose_name_plural = verbose_name

    def getJsonObj(self):
        province = {
            'provinceId': self.provinceId,
            'provinceName': self.provinceName,
        }
        return province

