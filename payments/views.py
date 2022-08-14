from django.shortcuts import redirect, render
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from users.models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

@login_required(login_url='/users/login/')
def home(request):
    user=User.objects.get(username=request.user)
    profile=Profile.objects.get(user=user)
    return render(request, "payments/index.html", context={"profile":profile})

@csrf_exempt
def add_money(request):
    currency = 'INR'
    amountrs=request.POST.get('amount')
    if amountrs is not None:
        amount=int(amountrs)*100
        # Create a Razorpay Order
        razorpay_order = razorpay_client.order.create(dict(amount=amount, currency=currency, payment_capture='0'))
        # order id of newly created order.
        razorpay_order_id = razorpay_order['id']
        callback_url = '/payments/paymenthandler/'
        # we need to pass these details to frontend.
        context = {}
        context['razorpay_order_id'] = razorpay_order_id
        context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
        context['razorpay_amount'] = amount
        context['currency'] = currency
        context['callback_url'] = callback_url
        context['amrs'] = amountrs
    
        return render(request, 'payments/add.html', context=context)
    return redirect('/payments/')

@csrf_exempt
def paymenthandler(request):
    # only accept POST request.
    if request.method == "POST":
        try:
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            amount = request.POST.get('razorpay_amount', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is None:
                try:
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
                    user=User.objects.get(username=request.user)
                    profile=Profile.objects.get(user=user)
                    old_amount=profile.wallet_bal
                    Profile.add_money(amount, profile, old_amount)
                    # render success page on successful caputre of payment
                    return render(request, 'payments/paymentsuccess.html')
                except:
 
                    # if there is an error while capturing payment.
                    return render(request, 'paymentfail.html')
            else:
 
                # if signature verification fails.
                return render(request, 'paymentfail.html')
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()
