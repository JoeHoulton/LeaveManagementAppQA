from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

class LEAVE_EVENTS(models.Model):
    title = models.CharField(max_length=40)
    snippet = models.CharField(max_length=150, blank=True)
    body = models.TextField(max_length=400, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField(blank=True)
    end_date = models.DateField(blank=True)
    start_time = models.CharField(max_length=40)
    end_time = models.CharField(max_length=40)
    status = models.CharField(max_length=40)
    creator_id = models.ForeignKey(User, blank=True, null=True)
    remind = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Leave Events"


class LEAVE_EVENTSAdmin(admin.ModelAdmin):
    list_display = ["start_date", "start_time", "end_date", "end_time", "title", "status", "snippet","creator_id","created_at"]
    list_filter = ["creator_id"]

class ORGANISATIONS(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    organisation_name = models.CharField(max_length=150)

    class Meta:
        verbose_name_plural = "Organisations"

    def __str__(self):
        return "(%s) %s" % (self.organisation_name, self.created_at)

class ORGANISATIONSAdmin(admin.ModelAdmin):
    list_display = ["created_at", "updated_at", "organisation_name"]
    list_filter = ["organisation_name"]

class ADDRESSES(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True)
    address_name = models.CharField(max_length=150)
    house_name = models.CharField(max_length=40)
    address_1 = models.CharField(max_length=40, blank=True)
    address_2 = models.CharField(max_length=40, blank=True)
    city = models.CharField(max_length=40)
    county = models.CharField(max_length=40)
    postcode = models.CharField(max_length=40)
    user_id = models.ForeignKey(User, blank=True, null=True)

    def __str__(self):
        return "(%s) %s" % (self.address_name, self.user_id)

    class Meta:
        verbose_name_plural = "Addresses"

class ADDRESSESAdmin(admin.ModelAdmin):
    list_display = ["created_at", "updated_at", "address_name", "house_name", "address_1", "address_2", "city", "county", "postcode", "user_id"]
    list_filter = ["user_id"]

class TEAMS(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    team_name = models.CharField(max_length=80)
    organisation_name = models.ForeignKey(ORGANISATIONS, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Teams"

    def __str__(self):
        return "(%s) %s" % (self.team_name, self.created_at)

class TEAMSAdmin(admin.ModelAdmin):
    list_display = ["created_at", "updated_at", "team_name", "organisation_name"]
    list_filter = ["team_name"]

admin.site.register(LEAVE_EVENTS, LEAVE_EVENTSAdmin)
admin.site.register(ORGANISATIONS, ORGANISATIONSAdmin)
admin.site.register(ADDRESSES, ADDRESSESAdmin)
admin.site.register(TEAMS, TEAMSAdmin)
