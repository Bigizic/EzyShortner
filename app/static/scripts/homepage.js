const $ = window.$;
const BASEURL = "localhost";
// const BASEURL = "ezyurl.io/";

$(document).ready(() => {
  $('#user_input').keypress(function (e) {
    if (e.which === 13 && $('#user_input').val().length > 3) {
      $('#url_form').submit();
    }
    if (e.which === 13) {
      if ($('#user_input').val().length < 2) {
        $('#user_input').focus();
        $('#user_input').blur();
      }
    }
  });

  $('.copy_').click(function () {
    const urlField = $('#user_output').select();
    document.execCommand('copy');
    urlField.blur();
  });

  $('.qr_code').click(function () {
    $('#qr_container').slideDown();
  });
  $('#cancelButton').click(function () {
    $('#qr_container').slideUp();
  });
  $('header h1').click(function () {
    window.location.replace(window.location.href);
  });

  $('.menu-button').click(function () {
    $('.cover-up').css('width', '100%');
    
  });
  
  $('.close-button').click(function () {
    $('.cover-up').css('width', '0');
  });

  /* This sets the alias button */
  $('.alias').one('click', function () {
    if ($('#user_output').val()) {
      $('#user_output').val('');
    }
    const currentWidth = parseInt($('#user_output').css('width'));
    const lPadd = parseInt($('#user_output').css('padding-left'));
    const rPadd = parseInt($('#user_output').css('padding-right'));
    const newWidth =  currentWidth - (lPadd + rPadd);
    $('#user_output').css('width', newWidth);
    $('#user_output').attr('autofocus', 'autofocus');
    $('#user_output').removeAttr('readonly');
    $('#user_output').attr('placeholder', 'Enter an alias e.g JohnDoe');
    $('.label_user_output').css('color', 'aliceblue');
    $('.label_user_output').html('www.ezyurl.tech/');
    $('#user_output').on('input', function () {
      var userInput = $(this).val();
      $('.label_user_output').text(`${BASEURL}/` + userInput);
    });
  });
  /* end alias button */
})

