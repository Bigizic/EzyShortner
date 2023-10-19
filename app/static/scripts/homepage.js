const $ = window.$;

$(document).ready(() => {
  $('#user_input').keypress(function (e) {
    if (e.which === 13) {
      $("#url_form").submit();
    }
  });

  $('.copy_').click(function () {
    const urlField = $('#user_output').select();
    document.execCommand('copy');
    urlField.blur();
  });
});
