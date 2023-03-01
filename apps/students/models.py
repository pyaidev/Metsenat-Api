from django.db import models
from django.db.models import Sum
from django.core.exceptions import ValidationError
from apps.accounts.models import Account
from apps.donate.models import Donate
from apps.sponsors.models import SponsorWallet
from apps.university.models import DEGREE, University


class StudentWallet(models.Model):
    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"

    student = models.ForeignKey(Account, on_delete=models.CASCADE, null=True,
                                limit_choices_to={'is_student': True, 'is_active': True})

    degree = models.IntegerField(choices=DEGREE, default=0)
    otm = models.ForeignKey(University, on_delete=models.CASCADE, null=True)
    contract_amount = models.FloatField(default=0.0)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def clean(self):
        student_all_get = self.donates()
        if student_all_get is None:
            student_all_get = 0
        new_amount = self.contract_amount
        if student_all_get is None:
            sponsor_all_give = 0
        if student_all_get > new_amount:
            name = "Xatolik. Bu talaba yangi kiritilgan mablag`dan oshiqcha sum hisobiga o`tkazilgan"
            raise ValidationError(f"{name} {student_all_get} sum")

    def __str__(self):
        return self.student.full_name

    def donates(self):
        donate = Donate.objects.filter(student_id=self.id).aggregate(Sum('donate'))
        return donate.get('donate__sum')
