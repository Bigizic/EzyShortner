const $ = window.$;

$(document).ready(() => {
  $('#user_input').keypress(function (e) {
    if (e.which === 13) {
      $('#url_form').submit();
  function updateVisibility () {
    if ($('#user_output').val()) {
      $('.share').css('visibility', 'visible');
    }
  }

  $('.enter').click(function () {
    updateVisibility();
  });

  $('#user_input').keypress(function (e) {
    if (e.which === 13) {
      updateVisibility();
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
    alert('URL copied to clipboard: ');
  });
});
