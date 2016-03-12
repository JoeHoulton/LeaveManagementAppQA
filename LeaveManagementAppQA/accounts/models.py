from django.contrib.auth.models import User
from django.db import models
from django.contrib import admin
from decimal import Decimal

from LeaveManagementAppQA.cal.models import ORGANISATIONS
from LeaveManagementAppQA.cal.models import TEAMS

class Employee(models.Model):
    user = models.OneToOneField(User)
    manager = models.ForeignKey(User, related_name='User' ,blank=True, null=True)
    organisation = models.ForeignKey(ORGANISATIONS, blank=True, null=True)
    leave_entitlement = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal(25.0))
    leave_remaining = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal(25.0))
    team_name = models.ForeignKey(TEAMS, related_name='User', blank=True, null=True)

    def get_leave_entitlement(self):
        return str(self.leave_entitlement)

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ["user", "manager", "organisation", "leave_entitlement", "leave_remaining", "team_name"]
    list_filter = ["manager"]

admin.site.register(Employee, EmployeeAdmin)