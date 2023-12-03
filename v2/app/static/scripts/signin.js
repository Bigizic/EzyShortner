$(document).ready(() => {
  /* start loading view */
  $('.loader').show();
  setTimeout(function() {
    $('.loader-container').fadeOut();
    $('body').css('visibility', 'visible');
  }, 1000);
  /* end loading view */

  /* create an account animation */
  function typeText(index, text, delay) {
    if (index < text.length) {
      $('#typing-animation').text(text.substring(0, index + 1));
      setTimeout(function() {
        typeText(index + 1, text, delay);
      }, delay);
    }
  }
  /* end */

  /* being removing animation text */
  function clearText(index, text, delay) {
    if (index <= text.length) {
      $('#typing-animation').text(text.substring(0, text.length - index));
      setTimeout(function() {
        clearText(index + 1, text, delay);
      }, delay);
    }
  }
  /* end */

  /* status code success or email has been used */
  const statusElement = $('#status_code');
    if (statusElement.length) {
      setTimeout(function () {
        statusElement.fadeOut();
      }, 5000);
    }
  /* end */

  /* password toogle */
  const passwordInput = $('#pass');
  const eyeIcon = $('.toggle-password i');
  
  passwordInput.attr('minlength', 8);
  passwordInput.on('input', function () {
    eyeIcon.addClass('bi-eye-slash-fill');
  });
  
  eyeIcon.click(function () {
    if (passwordInput.attr('type') === 'password') {
      passwordInput.attr('type', 'text');
      eyeIcon.removeClass('bi-eye-slash-fill').addClass('bi-eye-fill');
    } else {
      passwordInput.attr('type', 'password');
      eyeIcon.removeClass('bi-eye-fill').addClass('bi-eye-slash-fill');
    }
  });
  /* end */
  
  /* next button hover */
  $('.next_button').hover(
    function () {
      $('.next_button i').css('color', '#131418');
    },
    function () {
      $('.next_button i').css('color', '#fff');
    });
  /* end */
    
  typeText(0, "Hi there, Welcome back...", 100);
});
