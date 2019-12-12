$(document).ready(function() {
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      // Only send the token to relative URLs i.e. locally.
      xhr.setRequestHeader("X-CSRFToken", $("input[name=csrfmiddlewaretoken]").val());
    }
  });

  function mark_all_read() {
    var dropdown = $('#dropdown-notifications');
    dropdown.find('li.notification-unread').each(function() {
        $(this).removeClass('notification-unread');
        $(this).addClass('notification-read');
    });
    dropdown.find('i').removeClass('notification-icon');

    $.ajax({
      url: "/notifications/ajax/all/read/",
      method: "PUT",
      success: function(data) {
        console.log(data);
      }
    })
  }

  function mark_read() {
    var btn = $(this);
    btn.parent().closest('tr').removeClass('info');
    btn.attr('data-task', 'unread');
    btn.text('Mark Unread');
    btn.unbind('click');
    $.ajax({
      url: "/notifications/ajax/" + btn.attr('data-notification-id') + "/read/",
      method: "PUT",
      success: function(data) {
        if ( data.success ) {
          btn.on('click', mark_unread);
        }
      }
    });
  }

  function mark_unread() {
    var btn = $(this);
    btn.parent().closest('tr').addClass('info');
    btn.attr('data-task', 'read');
    btn.text('Mark Read');
    btn.unbind('click');
    $.ajax({
      url: "/notifications/ajax/" + btn.attr('data-notification-id') + "/unread/",
      method: "PUT",
      success: function(data) {
        if ( data.success ) {
          btn.on('click', mark_read);
        }
      }
    });
  }

  function mark_delete() {
    var btn = $(this);
    btn.parent().closest('tr').remove();
    $.ajax({
      url: "/notifications/ajax/" + btn.attr('data-notification-id') + "/archive/",
      method: "PUT",
      success: function(data) {
        if ( data.success ) {

        }
      }
    });
  }

  function request_approve(e) {
    e.preventDefault();
    var btn = $(this);
    var request_id = btn.attr('data-id');

    btn.parent().hide();

    var d = $('#dropdown-requests').find('.notification-icon');
    var c = Number(d.attr('data-count')) - 1;
    d.attr('data-count', c);

    if ( c === 0 ) {
      d.removeClass('notification-icon');
    }

    $.ajax({
        url: '/requests/ajax/' + request_id + '/approve/',
        method: 'post',
        success: function (data) {

        }
    });
  }

  function request_decline(e) {
    e.preventDefault();
    var btn = $(this);
    var request_id = btn.attr('data-id');

    btn.parent().hide();

    var d = $('#dropdown-requests').find('.notification-icon');
    var c = Number(d.attr('data-count')) - 1;
    d.attr('data-count', c);

    if ( c === 0 ) {
      d.removeClass('notification-icon');
    }

    $.ajax({
        url: '/requests/ajax/' + request_id + '/decline/',
        method: 'post',
        success: function (data) {

        }
    });
  }

  $('.notification-box button[data-task=read]').on('click', mark_read);

  $('.notification-box button[data-task=unread]').on('click', mark_unread);

  $('.notification-box button[data-task=delete]').on('click', mark_delete);

  $('#dropdown-notifications').find('.dropdown-toolbar-actions a').on('click', mark_all_read);

  $('#dropdown-requests').find('button[data-task=approve]').on('click', request_approve);
  $('#dropdown-requests').find('button[data-task=decline]').on('click', request_decline);
});