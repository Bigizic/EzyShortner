const $ = window.$;
const BASEURL = 'ezyurl.xyz';
const testEnv = 'api/ezy_v1/short?url=';

$(document).ready(() => {

  /* start loading view */
  $('.loader').show();
  setTimeout(function() {
    $('.loader-container').fadeOut();
    $('body').css('visibility', 'visible');
  }, 1000);
  /* end loading view */

  $('.left-items-lix').addClass('hover-effect');

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

  $('#user_input').on('input', function () {
    if ($('#user_output').val()) {
      $('#user_output').val('');
    }
  });

  /* copy button */
  $('.copy_').click(function () {
    const urlField = $('#user_output').select();
    document.execCommand('copy');
    urlField.blur();
  });
  /* end copy button */

  /* qr image animation */
  $('.qr_code').click(function () {
    $('#qr_container').slideDown();
  });
  $('#cancelButton').click(function () {
    $('#qr_container').slideUp();
  });
  /* end qr image animation */

  /* output or alias prefered characters */
  $('#user_output').on('input', function() {
    $(this).val($(this).val().replace(/[^a-zA-Z0-9-_+=&]/g, ''));
  });
  /* end prefered characters */

  /* This sets the alias button */
  let isAliasActive = false;
  
  $('.alias').on('click', function () {
    if ($('#user_output').val()) {
      $('#user_output').val('');
    }
    
    const currentWidth = parseInt($('#user_output').css('width'));
    const lPadd = parseInt($('#user_output').css('padding-left'));
    const rPadd = parseInt($('#user_output').css('padding-right'));
    const newWidth = currentWidth - (lPadd + rPadd);
    if (!isAliasActive) {
      $('#user_output').css('width', newWidth);
      $('#user_output').attr('autofocus', 'autofocus');
      $('#user_output').removeAttr('readonly');
      $('#user_output').attr('placeholder', 'Enter an alias e.g JohnDoe');
      $('.label_user_output').css('color', 'aliceblue');
      $('.label_user_output').css('font-size', 'medium');
      $('.label_user_output').html(BASEURL + '/');
      $('#user_output').on('input', function () {
        const userInput = $(this).val();
        $('.label_user_output').text(`${BASEURL}/` + userInput);
      });
      isAliasActive = true;
    } else {
      const formerWidth = currentWidth + (lPadd + rPadd);
      $('#user_output').val('');
      $('#user_output').css('width', formerWidth);
      $('#user_output').attr('readonly', 'readonly');
      $('#user_output').attr('placeholder', '');
      $('.label_user_output').css('color', '');
      $('.label_user_output').css('font-size', '');
      $('.label_user_output').html('');
      $('#user_output').off('input');

      isAliasActive = false;
    }
  });
  /* end alias button */
  
});
