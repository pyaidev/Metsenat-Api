from django.db import models
from django.db.models import Sum
from django.core.exceptions import ValidationError
from apps.accounts.models import Account
from apps.donate.models import Donate

STATUS = (
    ('Yangi', 'Yangi'),
    ('Moderatsiyada', 'Moderatsiyada'),
    ('Tasdiqlangan', 'Tasdiqlangan'),
    ('Bekor qilingan', 'Bekor qilingan'),
)

PAYMENT = (
    ('Naqd', 'Naqd'),
    ('Pul o`tkazmasi', 'Pul o`tkazmasi'),
)


class SponsorWallet(models.Model):
    class Meta:
        verbose_name = "Sponsor"
        verbose_name_plural = "Sponsors"

    sponsor = models.ForeignKey(Account, on_delete=models.CASCADE, null=True,
                                limit_choices_to={'is_sponsor': True, 'is_active': True})
    sponsor_wallet = models.FloatField(default=0.0)
    spent_amount = models.FloatField(default=0.0)
    is_company = models.BooleanField(default=False)
    status = models.CharField(max_length=30, choices=STATUS, default='Yangi')
    company_name = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    pay_type = mo
    369dels.CharField(max_length=30, choices=PAYMENT, default=None, blank=True, null=True)
    date_created = models.DateField(auto_now_add=True)

    def clean(self):
        if self.pk:
            sponsor = SponsorWallet.objects.get(pk=self.pk)
            if (sponsor.status == "Tasdiqlangan" or sponsor.status == "Moderatsiyada") and self.status == "Yangi":
                raise ValidationError("Statusni dastlabki holatga qaytarib bo`lmaydi!")
        if self.is_company and self.company_name is None:
            raise ValidationError("Korxona nomi kiritilmadi")
        if self.is_company is False and self.company_name:
            raise ValidationError("Bu homiy yuridik shaxs emas! Korxona nomini kiritmang!")
        if (self.status == "Yangi" or self.status == "Moderatsiyada") and self.pay_type:
            raise ValidationError("Tasdiqlanmagan homiy uchun to`lov turini tanlab bo`lmaydi!")
        if self.status == "Tasdiqlangan" and self.pay_type is None:
            raise ValidationError("To`lov turi tanlanmadi!")
        sponsor_all_give = self.donates()
        new_amount = self.spent_amount
        if sponsor_all_give is None:
            sponsor_all_give = 0
        if sponsor_all_give > new_amount:
            name = "Xatolik. Bu homiyning hisobidan yangi kiritilgan mablag`dan ko`proq mablag` homiylikka yo`naltirib bo`lingan!"
            raise ValidationError(f"{name} {sponsor_all_give} sum")

    def __str__(self):
        return self.sponsor.full_name

    def spent_amounts(self):
        spent_amount = Donate.objects.filter(sponsor_id=self.id).aggregate(
            Sum('donate'))
        if spent_amount.get('donate__sum'):
            spent_amount = self.sponsor_wallet - spent_amount.get('donate__sum')
        else:
            return 0
        # print(spent_amount)
        return spent_amount

    def wallet_avg(self):
        spent_amount = Donate.objects.filter(sponsor_id=self.id).aggregate(Sum('donate'))
        return spent_amount.get('donate__sum')

    def donates(self):
        donate = Donate.objects.filter(student_id=self.id).aggregate(Sum('donate'))
        return donate.get('donate__sum')
