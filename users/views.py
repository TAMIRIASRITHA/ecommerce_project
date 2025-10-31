from django.shortcuts import render, redirect
from users.forms import RegistrationForm, UpdateProfileForm
from django.contrib.auth import authenticate, login, logout
from users.models import OTP, CustomUser
from django.utils import timezone
from orders.models import Order
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import threading


# ✅ EMAIL SENDING (NON-BLOCKING THREAD)
def send_otp_email(recipient_email, otp_code):

    def _send():
        subject = "Your OTP Code — My Ecom Site"
        from_email = settings.DEFAULT_FROM_EMAIL or settings.EMAIL_HOST_USER

        context = {
            'otp': otp_code,
            'site_name': 'My Ecom Site',
            'expiry_minutes': 3,
        }

        html_content = render_to_string('emails/otp_email.html', context)

        try:
            msg = EmailMessage(subject, html_content, from_email, [recipient_email])
            msg.content_subtype = "html"
            msg.send(fail_silently=True)
        except Exception:
            pass  # Prevent server crash

    # ✅ Run email sending in background
    threading.Thread(target=_send).start()


# ✅ REGISTRATION VIEW
def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.email
            user.set_password(form.cleaned_data['password1'])
            user.is_active = False
            user.save()

            # ✅ Generate OTP
            otp_code = OTP.generate_otp()
            otp_expiry = timezone.now() + timedelta(minutes=3)
            OTP.objects.create(user=user, code=otp_code, expires_at=otp_expiry)

            request.session['email'] = user.email

            # ✅ Send OTP without blocking request
            send_otp_email(user.email, otp_code)

            return redirect('users:verify_otp')
    else:
        form = RegistrationForm()

    return render(request, 'users/register.html', {'form': form})


# ✅ HOME VIEW
def home_view(request):
    if not request.user.is_authenticated:
        return redirect('users:login')
    return render(request, 'users/home.html', {'user': request.user})


# ✅ VERIFY OTP
def verify_otp_view(request):
    email = request.session.get('email')
    if not email:
        return redirect('users:register')

    user = CustomUser.objects.filter(email=email).first()
    if not user:
        return redirect('users:register')

    if request.method == 'POST':
        code = request.POST.get('otp')
        otp_obj = OTP.objects.filter(user=user, code=code).order_by('-created_at').first()

        if not otp_obj:
            return render(request, 'users/verify_otp.html', {'message': 'Invalid OTP'})

        if otp_obj.is_expired():
            return render(request, 'users/verify_otp.html', {'message': 'OTP is expired'})

        # ✅ Activate User
        user.is_active = True
        user.save()
        return redirect('users:login')

    return render(request, 'users/verify_otp.html')


# ✅ LOGIN
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user:
            login(request, user)
            return redirect('users:home_view')

        return render(request, 'users/login.html', {
            'message': 'Invalid email or password'
        })

    return render(request, 'users/login.html')


# ✅ LOGOUT
def logout_view(request):
    logout(request)
    return redirect('users:login')


# ✅ PROFILE
@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('users:profile')
    else:
        form = UpdateProfileForm(instance=request.user)

    orders = Order.objects.filter(user=request.user)

    return render(request, 'users/profile.html', {
        'form': form,
        'orders': orders,
    })
