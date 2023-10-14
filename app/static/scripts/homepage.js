const $ = window.$;

$(document).ready(() => {
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
    alert('URL copied to clipboard: ');
  });
});
