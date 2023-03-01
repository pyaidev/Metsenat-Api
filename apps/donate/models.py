from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Sum

class Donate(models.Model):
    sponsor = models.ForeignKey('sponsors.SponsorWallet', on_delete=models.CASCADE, null=True,
                                related_name="sponsor_donate")
    student = models.ForeignKey('students.StudentWallet', on_delete=models.CASCADE, null=True,
                                related_name="student_wallet")
    donate = models.FloatField(default=0.0, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.pk:
            object = StudentSponsor.objects.get(pk=self.pk)
            if object.sponsor != self.sponsor:
                raise ValidationError("Homiyni o`zgartirish mumkin emas!")
            if object.student != self.student:
                raise ValidationError("Talabani o`zgartirish mumkin emas!")
            student_all_get = object.student.studentsponsor_set.all().aggregate(Sum('amount')).get('amount__sum')
            sponsor_all_give = object.sponsor.studentsponsor_set.all().aggregate(Sum('amount')).get('amount__sum')
            new_amount = self.donate
            last_amount = object.donate
            print(1, last_amount)
            print(2, new_amount)
            if student_all_get is None:
                student_all_get = 0
            if sponsor_all_give is None:
                sponsor_all_give = 0

            errorr: str = ""
            if self.sponsor.status != "Tasdiqlangan":
                errorr += "Tasdqilanmagan homiy hisobidan mablag` ajratilmaydi"
                raise ValidationError(errorr)
            if student_all_get - last_amount + new_amount > object.student.amount_contract:
                errorr += "Miqdor talaba kontrak miqdoridan ko`p, "
            if object.sponsor.amount_pay < sponsor_all_give - last_amount + new_amount:
                errorr += "homiyning mablag`i bu o`tkazmaga yetmaydi!"
            if errorr != "":
                raise ValidationError(errorr)
        else:
            student_all_get = self.donates()
            sponsor_all_give = self.donates()
            new_amount = self.donate
            if student_all_get is None:
                student_all_get = 0
            if sponsor_all_give is None:
                sponsor_all_give = 0

            errorr: str = ""
            if self.sponsor.status != "Tasdiqlangan":
                errorr += "Tasdqilanmagan homiy hisobidan mablag` ajratilmaydi"
                raise ValidationError(errorr)
            if student_all_get + new_amount > self.student.contract_amount:
                errorr += "Miqdor talaba kontrak miqdoridan ko`p, "
            if self.sponsor.spent_amount < sponsor_all_give + new_amount:
                errorr += "homiyning mablag`i bu o`tkazmaga yetmaydi!"
            if errorr != "":
                raise ValidationError(errorr)
    def donates(self):
        donate = Donate.objects.filter(student_id=self.id).aggregate(Sum('donate'))
        return donate.get('donate__sum')


    def __int__(self):
        return self.donate
