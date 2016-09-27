# -*- coding: utf-8 -*-


from django.db import models


class Slider(models.Model):

    title = models.CharField('Заголовок', max_length=128)
    url = models.CharField('Ссылка', max_length=256, blank=True, null=True,
                           help_text="Не забудьте указать начальную и конечную косые черты /")
    image = models.ImageField('Миниатюра', upload_to='upload_slider', blank=True, null=True)
    show = models.BooleanField('Показывать', default=True)
    position = models.IntegerField('Позиция', blank=True, null=True)

    def save(self, *args, **kwargs):
        model = self.__class__

        if self.position is None:
            # Append
            try:
                last = model.objects.order_by('-position')[0]
                self.position = last.position + 1
            except IndexError:
                # First row
                self.position = 0
        return super(Slider, self).save(*args, **kwargs)

    class Meta:
        ordering = ('position', )
        verbose_name = 'Картинку в слайдер'
        verbose_name_plural = 'Картинки в слайдере'
