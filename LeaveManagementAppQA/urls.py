from django.conf.urls.defaults import patterns, include, url

from django.contrib.auth import views as auth_views

from django.contrib import admin
admin.autodiscover()

from django.conf import settings

from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'LeaveManagementAppQA.views.index'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^account/leavedetails/','LeaveManagementAppQA.accounts.views.get_leave_information_ajax'),
    url(r'^account/addresses/','LeaveManagementAppQA.accounts.views.get_addresses_ajax'),
    url(r'^account/login/','LeaveManagementAppQA.accounts.views.login'),
    url(r'^account/auth/', 'LeaveManagementAppQA.accounts.views.auth_view'),
    url(r'^account/logout/','LeaveManagementAppQA.accounts.views.logout'),
    url(r'^account/loggedin/', 'LeaveManagementAppQA.accounts.views.loggedin'),
    url(r'^account/invalid/','LeaveManagementAppQA.accounts.views.invalid_login'),
    url(r'^account/profile/','LeaveManagementAppQA.accounts.views.index'),
    url(r'^change-password/', auth_views.password_change),
    url(r'^password_change/done/', auth_views.password_change_done),
    url(r'^password_reset/$', auth_views.password_reset),
    url(r'^password_reset/done/$', auth_views.password_reset_done),
    url(r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.password_reset_confirm),
    url(r'^reset/done/$', auth_views.password_reset_complete),
    url(r'^calendar/getevents/', 'LeaveManagementAppQA.cal.views.get_cal_events'),
    url(r'^calendar/','LeaveManagementAppQA.cal.views.calendar_view'),
    url(r'^calendar/language/(?P<language>[a-z\-]+)/','LeaveManagementAppQA.cal.views.language'),
    url(r'^main/','LeaveManagementAppQA.cal.views.main'),
    url(r'^main/(\d+)/', 'LeaveManagementAppQA.cal.views.main'),
    url(r'^dashboard/getbradfordfactor/', 'LeaveManagementAppQA.dashboard.views.get_bradford_factor'),
    url(r'^dashboard/getrequeststoapprove/', 'LeaveManagementAppQA.dashboard.views.get_team_leave_requests'),
    url(r'^dashboard/getpersonalevents/', 'LeaveManagementAppQA.dashboard.views.get_personal_leave_requests_ajax'),
    url(r'^dashboard/submitrequest/', 'LeaveManagementAppQA.dashboard.views.leave_request_submit'),
    url(r'^dashboard/', 'LeaveManagementAppQA.dashboard.views.dashboard'),
    url(r'^datepicker/', 'LeaveManagementAppQA.cal.views.date_picker_testing'),
    url(r'^event/approvedlocal/', 'LeaveManagementAppQA.requestapproval.views.approve_leave_local'),
    url(r'^event/approved/', 'LeaveManagementAppQA.requestapproval.views.approve_leave'),
    url(r'^event/cancelled/', 'LeaveManagementAppQA.requestapproval.views.cancel_leave'),
    url(r'^event/auth/', 'LeaveManagementAppQA.cal.views.event_add_auth'),
    url(r'^event/success/', 'LeaveManagementAppQA.cal.views.event_add_successful'),
    url(r'^userrequests/getuserrequests/', 'LeaveManagementAppQA.requestapproval.views.get_personal_leave_requests_ajax'),
    url(r'^userrequests', 'LeaveManagementAppQA.requestapproval.views.get_personal_requests'),
    url(r'^leaverequests/getallteamleaverequests/', 'LeaveManagementAppQA.requestapproval.views.get_all_team_leave_requests'),
    url(r'^leaverequests/getleaverequests/', 'LeaveManagementAppQA.requestapproval.views.get_team_leave_requests'),
    url(r'^leaverequests', 'LeaveManagementAppQA.requestapproval.views.leave_requests'),
    url(r'^teamrequests/', 'LeaveManagementAppQA.requestapproval.views.get_team_requests'),
)

handler404 = "LeaveManagementAppQA.views.handler404"


