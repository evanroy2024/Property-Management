from django.shortcuts import render ,redirect
from .models import FAQ
# Create your views here.
def faq(request):
    faqs = FAQ.objects.all()
    return render(request, 'contentpage/faq.html', {'faqs': faqs})



# views.py
from django.shortcuts import render
from .models import UserMessage

def send_message_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        need_type = request.POST.get('need_type')
        message = request.POST.get('message')

        if name and email and need_type and message:
            UserMessage.objects.create(
                name=name,
                email=email,
                need_type=need_type,
                message=message
            )
            return redirect('mainapp:home')  # Redirect to the FAQ page after sending the message

    return render(request, 'contentpage/send_message.html')
