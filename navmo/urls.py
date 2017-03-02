"""navmo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from register.views_register import faqs,overview,registration,home,login_check,logout_page,start,contactus,send_message
from register.views_register import logout_and_register,message,syllabus,exam_centers,results,admin_results1
from otp.views import verify_mobile
from payment.views import payment,payment_faliure,payment_success
from forgot_password.views import forgot_password
from admit_card.views import admit_card1,admit_card_offline,admit_card_offline3
from admit_card.views import final_admit_card
from admit_card.views import admit_card1,admit_card_offline,admit_card_offline3,send_email,release_admit_card
from photo_gallery.views import photo_gallery
from register.views_register import admin_certificate,admin_final_result_levelwise,admin_final_result_groupwise,upgrade_marks_data
from register.views_register import upload_final_result, national_result_levelwise
from register.views_results import national_all_rank_levelwise
from register.views_results import national_all_rank_groupwise
from register.views_results import spr_report,generate_marks
from register.views_results import send_email,register_raj
from register.views_results import data_panel_login,data_panel_logout, data_panel_home,send_spr_panel
from register.views_results import admin_results,scheduler,mysql_status,dump_db,graphs,download_spr_for_user,download_spr_panel,mail_spr_for_id


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',start),
    url(r'^accounts/login/$', login_check),
    url(r'^login/$', login_check),
    url(r'^register810/$',registration ),
    url(r'^home/$',home ),
    url(r'^logout/$',logout_page ),
    url(r'^logout_and_register/$',logout_and_register),
    url(r'^payment/$',payment ),
    url(r'^verify_mobile/$',verify_mobile ),
    url(r'^payment_faliure/$',payment_faliure),
    url(r'^payment_success/$',payment_success),
    url(r'^contactus/$',contactus),
    url(r'^overview/$',overview),
    url(r'^faqs/$',faqs),
    url(r'^message/$',message),
    url(r'^forgot_password/$',forgot_password),
    url(r'^syllabus/$',syllabus),
    url(r'^exam_centers/$',exam_centers),
    url(r'^admit_card/$',admit_card1),
    url(r'^admit_card_offline/$',admit_card_offline),
    url(r'^results/$',results),
    url(r'^admin_results/$',admin_results),
    url(r'^admin_results1/$',admin_results1),
    url(r'^admin_certificate/$',admin_certificate),

    # url(r'^send_message/$',send_message),
    url(r'^admit_card_offline3/$',admit_card_offline3),
    url(r'^final_admit_card/$',final_admit_card), 
    # url(r'^send_email/$',send_email),
    url(r'^release_admit_card/$',release_admit_card),
    url(r'^photo_gallery/$',photo_gallery), 

    url(r'^admin_final_result_levelwise/$',admin_final_result_levelwise),
    url(r'^admin_final_result_groupwise/$',admin_final_result_groupwise),
    url(r'^upgrade_marks_data/$',upgrade_marks_data),
    #url(r'^upload_final_result/$',upload_final_result),
    url(r'^national_result_levelwise/$',national_result_levelwise),
    url(r'^national_all_rank_levelwise/$',national_all_rank_levelwise),
    url(r'^national_all_rank_groupwise/$',national_all_rank_groupwise),
    url(r'^spr_report/$',spr_report),
    url(r'^generate_marks/$',generate_marks),
    #url(r'^convert_to_pdf/$',convert_to_pdf),
    url(r'^send_email/$',send_email),
    # url(r'^register_raj/$',register_raj),
    url(r'^data_panel/$',data_panel_login),
    url(r'^data_panel_logout/$',data_panel_logout),
    url(r'^data_panel_home/$',data_panel_home),
    url(r'^scheduler/$',scheduler),
    url(r'^mysql_status/$',mysql_status),
    url(r'^send_spr_panel/$',send_spr_panel),
    url(r'^dump_db/$',dump_db),
    url(r'^graphs/$',graphs),
    url(r'^download_spr_user/$',download_spr_for_user),
    url(r'^download_spr_panel/$',download_spr_panel),
    url(r'^get_spr/$',mail_spr_for_id),

]
from django.conf import settings
from django.conf.urls.static import static
urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)