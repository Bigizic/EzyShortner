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
  $('.left-items-lx').addClass('hover-effect');
  
  /* mobile menu button */
  $('.menu-button').click(function () {
    $('.cover-up').css('width', '80%');
  });

  $('.close-button').click(function () {
    $('.cover-up').css('width', '0');
  });
  /* end mobile menu button */
  
    /* Function to add a class for mobile*/
  function addClassForMobile() {
    const leftItemLix = $('.left-items-lx');
    if ($(window).width() <= 991) {
      leftItemLix.addClass('mobile-class');
    } else {
      leftItemLix.removeClass('mobile-class');
    }
  }
  /* end class for mobile*/
  
  /* names edit */
  $('#edit_name').click(function () {
    $('.name_form').slideDown();
  });
  $('#name_cancel').click(function () {
    $('.name_form').slideUp();
  });
  /* end names edit */
  
  /* password edit */
  $('#edit_pass').click(function () {
    $('.password_form').slideDown();
  });
  $('#pass_cancel').click(function () {
    $('.password_form').slideUp();
  });
  /* end password edit */
  
  /* status code success or email has been used */
  const statusElement = $('#status_code, #status_code_2');
    if (statusElement.length) {
      setTimeout(function () {
        statusElement.fadeOut();
      }, 5000);
    }
  /* end */


  /* password toogle for old password*/
  const passwordInput = $('#o_pass');
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
  
  /* password toogle for new password */
  const passwordInpu = [$('#n_pass'), $('#nn_pass')];
  const eyeIco = [$('.toggle-password-n i')];

  passwordInpu.forEach(function(e) {
    e.attr('minlength', 8);      
    e.on('input', function () {          
        eyeIco.forEach(function(icon) {
            icon.addClass('bi-eye-slash-fill');
        });
        const newPassword = $('#n_pass').val();
        const confirmNewPassword = $('#nn_pass').val();
        
        if (newPassword === confirmNewPassword) {
            $('#n_status').hide();
        } else {
            $('#n_status').show().css('display', 'block');
        }
    });
  });      

  eyeIco.forEach(function(icon) {
    icon.click(function () {
        passwordInpu.forEach(function(input) {
            if (input.attr('type') === 'password') {
                input.attr('type', 'text');
                icon.removeClass('bi-eye-slash-fill').addClass('bi-eye-fill');
            } else {
                input.attr('type', 'password');
                icon.removeClass('bi-eye-fill').addClass('bi-eye-slash-fill');
            }
        });
    });
  });
  /* end */
  
  /* PASSWORD MUST MATCH WARNING */
  $('#pass_form').on('submit', function(event) {
  const newPassword = $('#n_pass').val();
  const confirmNewPassword = $('#nn_pass').val();
  
  if (newPassword !== confirmNewPassword) {
    event.preventDefault();
    $('#n_status').html('');
    $('#n_status').html('Password must match');
    $('#n_status').show();
  }
  });
  /* END */

  
  addClassForMobile();
  $(window).resize(addClassForMobile);
  
  
  $('.main-content h1').click(function () {
    window.location.replace(window.location.href);
  });
  
});
