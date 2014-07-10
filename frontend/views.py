from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.http import StreamingHttpResponse
from ticketing.models import Event, BuyerType, EventBuyerMapping, PriceMatrix, Price, Transaction
from cart import Cart
from django.contrib.auth.decorators import login_required
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

        # go through the available prices and see what the user has requested
        for price in prices:
            if price.enabled:
                this_price = "%s-%s" % (price.category.id, price.buyer_type.id)

                if this_price in data:
                    # for each of these buyer_types lock a seat and add it to the cart
                    number_of_seats = int(data[this_price])
                    if number_of_seats > 0 and number_of_seats < 10:

                        locked_seats = event.lock_seats(transaction, 
                                                        price.buyer_type, 
                                                        price.price, 
                                                        number_of_seats)
                        if locked_seats:
                            logging.info('Locked %s seats', (len(locked_seats)))
                            # add sets to cart...
                            cart = Cart(request)
                            for seat in locked_seats:
                                logging.info('Adding seat to cart: %s' , (seat.id))
                                cart.add(seat, seat.price, 1)
                            context.update({'success': 'Seats added to shopping cart'})
                        else:
                            context.update({'error': 'Not enough seats available'})
                            logging.error('Failed to lock seats')

    html = render(request, 'buy.html', context)
    return StreamingHttpResponse(html)


def cart(request):
    cart = Cart(request)
    total = total_cart(cart)

    cart = sorted(cart, key=lambda mapping: [mapping.product.event.name,
                                             mapping.product.buyer_type.name])

    context = {'cart': cart,
               'total': total}

    html = render(request, 'cart.html', context)
    return StreamingHttpResponse(html)


def total_cart(cart):
    total = 0
    for item in cart:
        total += item.product.price
    return total


def empty_cart(request):
    cart = Cart(request)
    transaction = Transaction(user=request.user)
    transaction.save()

    for item in cart:
        item.product.unlock_seat(transaction)
        cart.remove(item.product)

    context = {'total': 0}

    html = render(request, 'cart.html', context)
    return StreamingHttpResponse(html)


@login_required
def purchase(request):
    context = {}
    html = render(request, 'cart.html', context)
    return StreamingHttpResponse(html)