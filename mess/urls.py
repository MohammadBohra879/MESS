from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'equipment', EquipmentViewSet)
router.register(r'user', UserViewSet)
router.register(r'request', RequestViewSet)
router.register(r'rating', RatingViewSet)

urlpatterns = [
    path('router/', include(router.urls)),

    path('donor/<int:donor_id>/equipment/',
         EquipmentByDonorViewSet.as_view({'get': 'list'})),

    path('equipment/available/',
         AvailableEquipmentViewSet.as_view({'get': 'list'})),

    path('equipment/in-use/',
         InUseEquipmentViewSet.as_view({'get': 'list'})),

    path('user/<int:user_id>/requests/',
         UserRequestViewSet.as_view({'get': 'list'})),

    path('equipment/<int:equipment_id>/ratings/',
         EquipmentRatingViewSet.as_view({'get': 'list'})),

    path('equipment/<int:equipment_id>/average-rating/',
         EquipmentAverageRatingViewSet.as_view({'get': 'list'})),

    path('equipment/available/count/',
         AvailableEquipmentCountViewSet.as_view({'get': 'list'})),

    path('users/count/',
         UserCountViewSet.as_view({'get': 'list'})),

     # path('admin/equipment/rating/',
     #      EquipmentByRatingViewSet.as_view({'get': 'list'})),

     path('equipment-list/', equipment_list, name='equipment-list'),
     path('equipment-detail/', equipment_detail, name='equipment-detail'),
     path('equipment-detail-before-login/<int:id>/', equipment_view_detail_before_login, name='equipment-detail-before-login'),
     path('equipment_view_detail/<int:id>/', equipment_view_detail, name='equipment-view-detail'),
     path('raise-request/<int:id>/', raise_request_view, name='raise-request'),
     path('', home_view, name='index'),
     path('login/', login_view, name='login'),
     path('homepage/', dashboard_view, name='homepage'),
     path('logout/', logout_view, name='logout'),
     path('add-equip/', add_equip, name='add-equip'),
     path('profile/', profile_view, name='profile'),
     path('my_equip/', my_equip, name='my-equip'),
     path('delete-equipment/<int:id>/', delete_equipment, name='delete-equipment'),
     path('my_req/', my_req, name='my-req'),
     path('remove-request/<int:id>/', remove_request, name='remove-request'),
     path('submit-feedback/<int:id>/', submit_feedback, name='submit-feedback'),
     path('received_req/', received_req, name='received-req'),
     path('approve-request/<int:id>/', approve_request, name='approve-request'),
     path('reject-request/<int:id>/', reject_request, name='reject-request'),
     path('about_us/', about_us, name='about-us'),
     path('about_us_logged_in/', about_us_logged_in, name='about-us-logged-in'),
]
