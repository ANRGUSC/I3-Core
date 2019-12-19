from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from .models import Transaction, ItemCount


class TransactionsView(LoginRequiredMixin, View):
    """
        If the user is staff, will render a page of all transactions, and item counts of the transactions. Otherwise will display transactions and item counts where the user is either buyer or seller.
        
        (LoginRequiredMixin, View)
        
        :model:`billing.Transaction`
        
        **Context**
        
        :model:`billing.Transaction`, :model:`billing.ItemCount`
        
        ``transactions``: A list of all Transaction objects.
        
        ``item_counts``: A list of all ItemCount objects.
        
        **Template**
        
        :template:`dashboard/transactions.html`
        
        """
    def get(self, request, *args, **kwargs):
        """ Takes http request and renders page depending on whether user is staff
            """
        if request.user.is_staff:
            pass
            transactions = Transaction.objects.all().order_by("-timestamp")
            item_counts = ItemCount.objects.all()

            context = {
                'transactions': transactions,
                'item_counts': item_counts
            }

            return render(request, 'dashboard/transactions.html', context=context)
        else:
            purchases = Transaction.objects.filter(buyer=request.user).order_by("-timestamp")
            sales = Transaction.objects.filter(seller=request.user).order_by("-timestamp")
            item_counts = ItemCount.objects.filter(buyer=request.user).order_by("-last_recv_timestamp")

            context = {
                'purchases': purchases,
                'sales': sales,
                'item_counts': item_counts
            }

            return render(request, 'dashboard/transactions.html', context=context)
