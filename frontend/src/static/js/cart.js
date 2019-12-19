$(document).ready(function() {
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      // Only send the token to relative URLs i.e. locally.
      xhr.setRequestHeader("X-CSRFToken", $("input[name=csrfmiddlewaretoken]").val());
    }
  });

  function updateCart() {
    var rows = $('table.cart tbody tr')
    if ( rows.length === 0 ) {
      $('table.cart tbody')
          .html('<tr><td colspan="5"><span style="font-style: italic;">Your cart is empty.</span></td></tr>');
      $('table.cart tfoot').remove();
    $('#cart_count').removeClass('notification-icon')
    } else {
      var total = 0.0;
      $('td.price').each(function() {
        total += Number($(this).text());
      });
      $('#total_price').text(total);
    $('#cart_count').attr('data-count', rows.length);
    }
  }

  $('table.cart tbody button').on('click', function() {
    var btn = $(this);
    btn.parent().closest('tr').remove();
    var item = btn.attr('data-id');
    $.ajax({
      url: '/cart/ajax/?item='+item,
      method: 'delete',
      success: function(data) {
        console.log(data);
        updateCart();
      }
    })
  });

  $('form[name=checkout]').on('submit', function(evt) {
    evt.preventDefault();
    $('form[name=checkout] button[type=submit]').attr('disabled', 'disabled');

    $.ajax({
      url: '/checkout/',
      method: 'post',
      success: function(data) {
        if ( data.success ) {
          window.location.href = '/dashboard/transactions/'
        }
      }
    })

  });
});