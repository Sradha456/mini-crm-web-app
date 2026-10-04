from django.shortcuts import render, redirect
from .models import Contact , Deal
from .forms import ContactForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required



# Contact List + Search
@login_required
def contact_list(request):
    search = request.GET.get('search', '')

    if search:
        contacts = Contact.objects.filter(
            user=request.user,
            name__icontains=search)
    else:
        contacts = Contact.objects.filter(
            user=request.user
    )

    return render(
        request,
        'contacts/contact_list.html',
        {
            'contacts': contacts,
            'search': search
        }
    )


# Add Contact
@login_required
def contact_create(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()
            return redirect('contact_list')
    else:
        form = ContactForm()

    return render(request, 'contacts/contact_form.html', {
        'form': form
    })


# Edit Contact
@login_required
def contact_edit(request, id):
    contact = Contact.objects.get(id=id, user=request.user)

    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)

        if form.is_valid():
            form.save()
            return redirect('contact_list')
    else:
        form = ContactForm(instance=contact)

    return render(request, 'contacts/contact_form.html', {
        'form': form
    })


# Delete Contact
@login_required
def contact_delete(request, id):
    contact = Contact.objects.get(id=id, user=request.user)

    if request.method == 'POST':
        contact.delete()
        return redirect('contact_list')

    return render(request, 'contacts/contact_confirm_delete.html', {
        'contact': contact
    })

@login_required
def deal_list(request):
    deals = Deal.objects.filter(user=request.user)

    return render(
        request,
        'contacts/deal_list.html',
        {'deals': deals}
    )


# Signup
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'contacts/signup.html', {
        'form': form
    })

@login_required
@login_required
def deal_create(request):
    contacts = Contact.objects.filter(user=request.user)

    if request.method == "POST":
        title = request.POST.get("title")
        contact_id = request.POST.get("contact")
        stage = request.POST.get("stage")

        contact = Contact.objects.get(
            id=contact_id,
            user=request.user
        )

        Deal.objects.create(
            user=request.user,
            title=title,
            contact=contact,
            stage=stage
        )

        return redirect('deal_list')

    return render(request, 'contacts/deal_form.html', {
        'contacts': contacts
    })

@login_required
def deal_edit(request, id):
    deal = Deal.objects.get(id=id, user=request.user)
    contacts = Contact.objects.filter(user=request.user)

    if request.method == "POST":
        deal.title = request.POST.get("title")
        deal.contact_id = request.POST.get("contact")
        deal.stage = request.POST.get("stage")
        deal.save()

        return redirect('deal_list')

    return render(request, 'contacts/deal_form.html', {
        'deal': deal,
        'contacts': contacts
    })


@login_required
def deal_delete(request, id):
    deal = Deal.objects.get(id=id, user=request.user)

    if request.method == "POST":
        deal.delete()
        return redirect('deal_list')

    return render(request, 'contacts/deal_confirm_delete.html', {
        'deal': deal
    })

@login_required
def update_deal_stage(request, id, stage):
    deal = Deal.objects.get(id=id, user=request.user)

    if stage in ['New', 'Contacted', 'Qualified', 'Won', 'Lost']:
        deal.stage = stage
        deal.save()

    return redirect('deal_list')

@login_required
def ai_email(request, id):
    deal = Deal.objects.get(id=id, user=request.user)

    email = ""

    if request.method == "POST":
        contact_name = deal.contact.name
        notes = deal.contact.notes
        stage = deal.stage

        email = f"""Subject: Follow-up regarding {deal.title}
Hi {contact_name},
I hope you are doing well.
I wanted to follow up regarding {deal.title}.
Based on our previous discussion, I understand that:
{notes}
The current stage of our discussion is {stage}.
Please let me know if you have any questions or if you would like to discuss this further.
Looking forward to hearing from you.
Best regards,
Sales Team
"""

    return render(request, 'contacts/ai_email.html', {
        'deal': deal,
        'email': email
    })