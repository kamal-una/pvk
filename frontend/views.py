from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.http import StreamingHttpResponse
from ticketing.models import Event, BuyerType, EventBuyerMapping, PriceMatrix, Price, Transaction
import logging


def schedule(request):
    events = Event.objects.order_by('date')
    context = {'events': events}

    html = render(request, 'schedule.html', context)
    return StreamingHttpResponse(html)


def buy(request, event):
    event = get_object_or_404(Event, pk=event)
    prices = event.get_prices()

    context = {'event': event,
               'prices': prices}

    if request.method == 'POST':
        data = request.POST

        #make a new transaction
        transaction = Transaction(user=request.user)
        transaction.save()
        redirect_to_cart = False

        # go through the available prices and see what the user has requested
        for price in prices:
            if price.enabled:
                this_price = "%s-%s" % (price.category.id, price.buyer_type.id)

                if this_price in data:
                    # for each of these buyer_types lock a seat and add it to the cart
                    number_of_seats = int(data[this_price])
                    if number_of_seats > 0 and number_of_seats < 10:

                        lock_seats = event.lock_seats(transaction, 
                                                      price.buyer_type, 
                                                      price.price, 
                                                      number_of_seats)
                        if lock_seats:
                            logging.info('Locked %s seats', (number_of_seats))
                            redirect_to_cart = True
                        else:
                            context.update({'error': 'Not enough seats available'})
                            logging.error('Failed to lock seats')

        # only redirect to the cart if we have added some seats
        if redirect_to_cart:
            pass
            #return redirect('cart')

    html = render(request, 'buy.html', context)
    return StreamingHttpResponse(html)