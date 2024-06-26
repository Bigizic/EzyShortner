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

  /* status code success or email has been used */
  const statusElement = $('#status_code');
    if (statusElement.length) {
      setTimeout(function () {
        statusElement.fadeOut();
      }, 5000);
    }
  /* end */
  
  /* next button functions */
  $('.next_button').click(function () {
    if ($('#typing-animation').text() === "Create an account in seconds!") {
      const emailInput = $('#email_or_username');
      const passInput = $('#pass');
      if (emailInput.val() && passInput.val().length >= 8) {
        $('.first_form').hide().css('transform', 'scale(1)');
        $('.second_form').show().css('transform', 'scale(1.1)');
        typeText(0, "Almost there...", 100);
      } else {
        if (!emailInput.val()) {
          emailInput.css('border', '1px solid red');
        }
        if (!passInput.val()) {
          passInput.css('border', '1px solid red');
        }
        if (passInput.val().length < 8) {
          $('.password-warning').html("password length must be 8");
        }
      }
    }
  });
  $('.nnext_button').click(function () {
    $('#typing-animation').css('display', 'none');
    $('.second_form').hide().css('transform', 'scale(1)');
    $('.third_form').show().css('transform', 'scale(1.1)');
  });
  /* next button end */
  
  /* back button functions */
  $('.back_button').click(function () {
    if ($('#typing-animation').text() === "Almost there...") {
      $('.second_form').hide().css('transform', 'scale(1)');
      $('.first_form').show().css('transform', 'scale(1.1)');
      typeText(0, "Create an account in seconds!", 100);
    }
  });
  /* back button end */
  
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
  

  typeText(0, 'Create an account in seconds!', 100);
});
