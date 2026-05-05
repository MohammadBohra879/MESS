from urllib import request

from rest_framework import viewsets, mixins
from django.shortcuts import get_object_or_404, redirect, render
from datetime import date
from django.db.models import Avg, Count, Q
from rest_framework.response import Response
from django.core.paginator import Paginator
from geopy.geocoders import Nominatim
import math
from .models import User, Equipment, Request, Rating
from .serializers import UserSerializer, EquipmentSerializer, RequestSerializer, RatingSerializer
from geopy.geocoders import Nominatim

# -------------------------
# Equipment CRUD
# -------------------------
class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.select_related('donor').all()
    serializer_class = EquipmentSerializer


# -------------------------
# View Equipment by Donor
# -------------------------
class EquipmentByDonorViewSet(mixins.ListModelMixin,
                              viewsets.GenericViewSet):
    serializer_class = EquipmentSerializer

    def get_queryset(self):
        donor_id = self.kwargs.get('donor_id')
        donor = get_object_or_404(User, user_id=donor_id)
        return donor.equipment.select_related('donor').all()


# -------------------------
# Available Equipment
# -------------------------
class AvailableEquipmentViewSet(mixins.ListModelMixin,
                                viewsets.GenericViewSet):
    serializer_class = EquipmentSerializer

    def get_queryset(self):
        return Equipment.objects.filter(available_status='available')


# -------------------------
# In Use Equipment
# -------------------------
class InUseEquipmentViewSet(mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    serializer_class = EquipmentSerializer

    def get_queryset(self):
        return Equipment.objects.filter(available_status='In_use')


# -------------------------
# Equipment Ratings
# -------------------------
class EquipmentRatingViewSet(mixins.ListModelMixin,
                             viewsets.GenericViewSet):
    serializer_class = RatingSerializer

    def get_queryset(self):
        equipment_id = self.kwargs.get('equipment_id')
        return Rating.objects.filter(product_id=equipment_id)


# -------------------------
# Average Rating
# -------------------------
class EquipmentAverageRatingViewSet(mixins.ListModelMixin,
                                    viewsets.GenericViewSet):

    def list(self, request, equipment_id=None):
        avg = Rating.objects.filter(
            product_id=equipment_id
        ).aggregate(Avg('score'))

        return Response({'average_rating': avg['score__avg']})


# -------------------------
# Count Available Equipment
# -------------------------
class AvailableEquipmentCountViewSet(mixins.ListModelMixin,
                                     viewsets.GenericViewSet):

    def list(self, request):
        total = Equipment.objects.filter(
            available_status='available'
        ).count()

        return Response({'total_available_equipment': total})

# -------------------------
# USER CRUD
# -------------------------
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# -------------------------
# Count Total Users
# -------------------------
class UserCountViewSet(mixins.ListModelMixin,
                       viewsets.GenericViewSet):

    def list(self, request):
        total = User.objects.count()
        return Response({'total_users': total})


# -------------------------
# User Requests
# -------------------------
class UserRequestViewSet(mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    serializer_class = RequestSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return Request.objects.filter(requester_id=user_id)


# -------------------------
# Request CRUD
# -------------------------
class RequestViewSet(viewsets.ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer


# -------------------------
# Rating CRUD
# -------------------------
class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer


# -------------------------
# Admin: Equipment by Rating 
# -------------------------
# class EquipmentByRatingViewSet(mixins.ListModelMixin,
#                                viewsets.GenericViewSet):

#     serializer_class = EquipmentSerializer

#     def get_queryset(self):
#         return Equipment.objects.annotate(
#             avg_rating=Avg('rating__score')
#         ).order_by('avg_rating')


#login page
# -------------------------
# HOME PAGE
# -------------------------
def home_view(request):
    user_count = User.objects.count()
    equipment_count = Equipment.objects.count()
    sharing_count = Request.objects.count()
    equipments = Equipment.objects.select_related('donor').all().order_by('-create_date')[:4]  # Show only 4 items on the homepage
    return render(request, 'pre_sign/Index.html', {
        'equipment': equipments,
        'user_count': user_count,
        'equipment_count': equipment_count,
        'sharing_count': sharing_count
    }
    )


# -------------------------
# LOGIN VIEW
# -------------------------
def login_view(request):
    error = None

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        lat = float(request.POST.get('lat') or 0)
        long = float(request.POST.get('long') or 0)

        if not email or not password:
            error = "Please enter email and password"
            return render(request, 'pre_sign/sign_in.html', {'error': error})

        try:
            user = User.objects.get(email=email)

            if user.password == password:
                # Update location
                user.lat = lat or 0
                user.long = long or 0
                user.update_date = date.today()
                user.save()

                request.session['user_id'] = user.user_id
                request.session['user_name'] = user.name
                request.session['user_email'] = user.email
                request.session['user_contact_no'] = user.contact_no
                request.session['user_lat'] = user.lat
                request.session['user_long'] = user.long

                return redirect('homepage')

            else:
                error = "Invalid Password"

        except User.DoesNotExist:
            # Create new user
            new_user = User.objects.create(
                name="New User",
                email=email,
                password=password,
                contact_no=0,
                lat=lat or 0,
                long=long or 0,
                create_date=date.today()
            )

            request.session['user_id'] = new_user.user_id
            request.session['user_name'] = new_user.name

            return redirect('homepage')

    return render(request, 'pre_sign/sign_in.html', {'error': error})

# -------------------------
# DASHBOARD
# -------------------------
def dashboard_view(request):
    user_count = User.objects.count()
    equipment_count = Equipment.objects.count()
    sharing_count = Request.objects.count()
    user_name = request.session.get('user_name', 'User')
    equipments = Equipment.objects.select_related('donor').all().order_by('-create_date')[:4]  # Show only 4 items on the homepage
    return render(request, 'sign_in/homepage.html', {
        'username': user_name,
        'user_count': user_count,
        'equipment_count': equipment_count,
        'sharing_count': sharing_count,
        'equipment': equipments
    })


# -------------------------
# LOGOUT
# -------------------------
def logout_view(request):
    request.session.flush()
    return redirect('index')



#items page after login
def equipment_list(request):
    query = request.GET.get('q', '')
    equipments = Equipment.objects.select_related('donor').all().order_by('-create_date')

    if query:
        # 🔥 normalize input (remove spaces + lowercase)
        search = query.replace(" ", "").lower()

        equipments = equipments.filter(
            Q(equipment_name__icontains=query) |   # normal search
            Q(equipment_name__icontains=search)    # merged search
        )

    #  PAGINATION (8 items)
    paginator = Paginator(equipments, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    geolocator = Nominatim(user_agent="geoapi")

    equipment_data = []

    for e in page_obj:   #  IMPORTANT CHANGE (not all, only page items)
        lat = e.donor.lat
        lon = e.donor.long

        try:
            location = geolocator.reverse(f"{lat}, {lon}")
            area = location.address if location else "Unknown Location"
        except:
            area = "Location not found"

        data = {
            'id': e.equipment_id,
            'name': e.equipment_name,
            'area': area,
            'available_status': e.available_status,
            'img': e.equipment_img,
        }

        equipment_data.append(data)

    return render(request, 'sign_in/items.html', {
        'equipment': equipment_data,
        'page_obj': page_obj,   #  send this
        'username': request.session.get('user_name')
    })

#equipment detail page before login
def equipment_detail(request):
    query = request.GET.get('q', '')
    equipments = Equipment.objects.select_related('donor').all().order_by('-create_date')

    if query:
        # 🔥 normalize input (remove spaces + lowercase)
        search = query.replace(" ", "").lower()

        equipments = equipments.filter(
            Q(equipment_name__icontains=query) |   # normal search
            Q(equipment_name__icontains=search)    # merged search
        ) 
    #  PAGINATION (8 items)
    paginator = Paginator(equipments, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    geolocator = Nominatim(user_agent="geoapi")

    equipment_data = []

    for e in page_obj:  
        lat = e.donor.lat
        lon = e.donor.long

        try:
            location = geolocator.reverse(f"{lat}, {lon}")
            area = location.address if location else "Unknown Location"
        except:
            area = "Location not found"

        data = {
            'id': e.equipment_id,
            'name': e.equipment_name,
            'area': area,
            'available_status': e.available_status,
            'img': e.equipment_img,
        }

        equipment_data.append(data)
    return render(request, 'pre_sign/items.html', {
        'equipment': equipment_data,
        'page_obj': page_obj,
        "username": request.session.get('user_name')
    }
    )

def equipment_view_detail_before_login(request, id):
    equip = get_object_or_404(Equipment, equipment_id=id)

    geolocator = Nominatim(user_agent="geoapi")

    try:
        location = geolocator.reverse(f"{equip.donor.lat}, {equip.donor.long}")
        area = location.address if location else "Unknown Location"
    except:
        area = "Location not found"

    rating_data = Rating.objects.filter(product=equip).aggregate(
    avg=Avg('score'),
    count=Count('rating_id')
)

    if rating_data['count'] >= 10:
        avg_rating = round(rating_data['avg'], 1)
    else:
        avg_rating = 5.0

    return render(request, 'pre_sign/equip_detail.html', {
        'equip': equip,
        'area': area,
        'avg_rating': avg_rating
    })

def equipment_view_detail(request, id):
    equip = get_object_or_404(Equipment, equipment_id=id)

    geolocator = Nominatim(user_agent="geoapi")

    try:
        location = geolocator.reverse(f"{equip.donor.lat}, {equip.donor.long}")
        area = location.address if location else "Unknown Location"
    except:
        area = "Location not found"

    # distance
    user_id = request.session.get('user_id')
    user = User.objects.get(user_id=user_id)

    distance = round(math.sqrt(
        (user.lat - equip.donor.lat)**2 +
        (user.long - equip.donor.long)**2
    ) * 111, 2)

    # rating
    rating_data = Rating.objects.filter(product=equip).aggregate(
    avg=Avg('score'),
    count=Count('rating_id')
)

    if rating_data['count'] >= 10:
        avg_rating = round(rating_data['avg'], 1)
    else:
        avg_rating = 5.0

    return render(request, 'sign_in/equip_detail.html', {
        'username': request.session.get('user_name'),
        'equip': equip,
        'area': area,
        'distance': distance,
        'avg_rating': avg_rating
    })

def raise_request_view(request, id):
    equip = get_object_or_404(Equipment, equipment_id=id)

    if request.method == 'POST':
        user_id = request.session.get('user_id')
        user = User.objects.get(user_id=user_id)

        priority = request.POST.get('priority')

        Request.objects.create(
            equipment=equip,
            requester=user,
            donor=equip.donor,
            status="Pending",
            priority=priority,
            req_date=date.today() 
        )

        return redirect('my-req')

    return render(request, 'sign_in/raise_req.html', {
        'equip': equip
    })

#about us before login
def about_us(request):
    return render(request, 'pre_sign/about_us.html')

#about us after login
def about_us_logged_in(request):
    return render(request, 'sign_in/about_us.html', {
        'username': request.session.get('user_name')
    })

def add_equip(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        img = request.FILES.get('img')

        lat = request.POST.get('lat')
        long = request.POST.get('long')

        user_id = request.session.get('user_id')
        donor = get_object_or_404(User, user_id=user_id)

        # UPDATE DONOR LOCATION
        if lat and long:
            donor.lat = float(lat)
            donor.long = float(long)
            donor.update_date = date.today()
            donor.save()

        # CREATE EQUIPMENT WITH SAME LOCATION
        Equipment.objects.create(
            equipment_name=name,
            available_status='Available',
            equipment_img=img,
            donor=donor,
            create_date=date.today()
        )

        return redirect('my-equip')

    return render(request, 'sign_in/add_equip.html', {
        'username': request.session.get('user_name')
    })


def profile_view(request):
    user_id = request.session.get('user_id')
    user = get_object_or_404(User, user_id=user_id)

    if request.method == 'POST':
        user.name = request.POST.get('name')
        user.email = request.POST.get('email')
        user.contact_no = request.POST.get('contact_no')

        # location update
        user.lat = float(request.POST.get('lat') or 0)
        user.long = float(request.POST.get('long') or 0)

        user.save()
        request.session['user_name'] = user.name
        request.session['user_email'] = user.email
        request.session['user_contact_no'] = user.contact_no
        request.session['user_lat'] = user.lat
        request.session['user_long'] = user.long
        return redirect('homepage')

    return render(request, 'sign_in/profile.html', {
        'username': user.name,
        'email': user.email,
        'contact_number': user.contact_no
    })

def my_equip(request):
    user_id = request.session.get('user_id')
    query = request.GET.get('q', '')
    # equipments = Equipment.objects.select_related('donor').all().order_by('-create_date')
    equipments = Equipment.objects.select_related('donor').filter(donor_id=user_id)
    if query:
        # 🔥 normalize input (remove spaces + lowercase)
        search = query.replace(" ", "").lower()

        equipments = equipments.filter(
            Q(equipment_name__icontains=query) |   # normal search
            Q(equipment_name__icontains=search)    # merged search
        )
   

    return render(request, 'sign_in/my_equip.html', {
        'equipment': equipments,
        'username': request.session.get('user_name')
    })

def delete_equipment(request, id):
    user_id = request.session.get('user_id')

    equip = get_object_or_404(Equipment, equipment_id=id, donor_id=user_id)
    equip.delete()

    return redirect('my-equip')

def my_req(request):
    user_id = request.session.get('user_id')
    requester = get_object_or_404(User, user_id=user_id)
    query = request.GET.get('q', '')
    requests = requester.requests_made.select_related('donor', 'equipment')

    if query:
            search = query.replace(" ", "").lower()

            requests = requests.filter(
                Q(equipment__equipment_name__icontains=query) |
                Q(equipment__equipment_name__icontains=search)
            )

    geolocator = Nominatim(user_agent="geoapi")

    request_data = []

    for req in requests:
        lat = req.donor.lat
        long = req.donor.long

        try:
            location = geolocator.reverse(f"{lat}, {long}")
            area = location.address if location else "Unknown Location"
        except:
            area = "Location not found"

        request_data.append({
            'req': req,
            'area': area
        })

    return render(request, 'sign_in/my_req.html', {
        'requests': request_data,
        'username': request.session.get('user_name'),
        'star_ratings': [1, 2, 3, 4, 5],  # for star rating
        'req_id': request.session.get('req_id')
    })

def remove_request(request, id): # only for pending, requester can cancel
    req = get_object_or_404(Request, req_id=id)
    user_id = request.session.get('user_id')
    # Only allow if pending
    if req.requester.user_id == user_id and req.status in ["Pending", "Rejected"]:
        req.delete()

    return redirect('my-req')

def submit_feedback(request, id):
    if request.method == 'POST':
        req = get_object_or_404(Request, req_id=id)

        rating = request.POST.get('rating')
        feedback = request.POST.get('feedback')

        Rating.objects.create(
            product=req.equipment,   
            reporter=req.requester,
            score=int(rating),
            feedback=feedback,
            rating_date=date.today()
        )

        req.equipment.available_status = "Available"
        req.equipment.update_date = date.today()
        req.equipment.save()

        req.status = "Completed"
        req.update_date = date.today()
        req.save()

        return redirect('my-req')




def received_req(request):
    user_id = request.session.get('user_id')
    donor = get_object_or_404(User, user_id=user_id)
    query = request.GET.get('q', '')
    requests = Request.objects.filter(donor=donor, status='Pending').select_related('requester', 'equipment')

    if query:
        search = query.replace(" ", "").lower()

        requests = requests.filter(
            Q(equipment__equipment_name__icontains=query) |
            Q(equipment__equipment_name__icontains=search)
        )

    return render(request, 'sign_in/received_req.html', {
        'requests': requests,
        'username': request.session.get('user_name')
    })

def approve_request(request, id):
    req = get_object_or_404(Request, req_id=id)
    req.status = "Approved"
    req.update_date = date.today()
    req.equipment.available_status = "In_use"
    req.equipment.save()
    req.save()
    return redirect('received-req')


def reject_request(request, id):
    req = get_object_or_404(Request, req_id=id)
    req.status = "Rejected"
    req.update_date = date.today()
    req.equipment.available_status = "Available"
    req.equipment.save()
    req.save()
    return redirect('received-req')