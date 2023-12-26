const $ = window.$;
const BASEURL = 'ezyurl.xyz';
const testEnv = 'api/ezy_v1/short?url=';

$(document).ready(() => {


  function opacityStart() {
    $('.left-sidebar').css('opacity', '0.2');
    $('.right-sidebar').css('opacity', '0.2');
    $('footer').css('opacity', '0.2');
  };
  
  function opacityEnd() {
    $('.left-sidebar').css('opacity', '1');
    $('.right-sidebar').css('opacity', '1');
    $('footer').css('opacity', '1');
  };
  
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
    opacityStart();
    $('.cover-up').css('width', '80%');
  });

  $('.close-button').click(function () {
    opacityEnd();
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
    opacityStart();
    $('.name_form').slideDown();
  });
  $('#name_cancel').click(function () {
    opacityEnd();
    $('.name_form').slideUp();
  });
  /* end names edit */
  
  /* password edit */
  $('#edit_pass').click(function () {
    opacityStart();
    $('.password_form').slideDown();
  });
  $('#pass_cancel').click(function () {
    opacityEnd();
    $('.password_form').slideUp();
  });
  /* end password edit */
  
  /* authy setup */
  $('.authy_html_setup').click(function () {
    if ($('#authy_status').text() == 'disabled') {
      $('.authy_form').slideDown();
      opacityStart();
    }
  });
  $('#authy_cancel').click(function () {
    $('.authy_form').slideUp();
    opacityEnd();
  });
  /* end authy setup */
  
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
  
  /*DELETE USER FUNCTIONS */
  
  $('.delete_user').on('click', function(e) {
    e.preventDefault();
    const userId = $(this).data('user-id');
    if (confirm(`Confirm to delete your account and it's records`)) {
      $.ajax({
        url: `/profile/delete/${userId}`,
        method: 'POST',
        success: function(response) {
          window.location.replace(window.location.href);
        },
        error: function(xhr, status, error) {
          console.error(error);
        }
      });
    }
  });
  /*END DELETE USER */

  $('.authy_f').find('input').each(function() {
    $(this).attr('maxlength', 1);
    $(this).on('keyup', function(e) {
      var parent = $($(this).parent());

      if(e.keyCode === 8 || e.keyCode === 37) {
        var prev = parent.find('input#' + $(this).data('previous'));
      
        if(prev.length) {
          $(prev).select();
        }
        } else if((e.keyCode >= 48 && e.keyCode <= 57) || (e.keyCode >= 65 && e.keyCode <= 90) || (e.keyCode >= 96 && e.keyCode <= 105) || e.keyCode === 39) {
          var next = parent.find('input#' + $(this).data('next'));
      
          if(next.length) {
            $(next).select();
          } else {
            if(parent.data('autosubmit')) {
              parent.submit();
            }
          }
        }
    });
  });
  
  
  /* secret key copy */  
  const auS = $('#user_secret_key').data('name');
  const fN = $('#user_secret_key').text().trim().split(' ')[0];

  $(document).on('click', '.secret_key_copy', function() {
    const tempInput = $('<textarea>');
    $('body').append(tempInput);
    tempInput.val(fN).select();
    document.execCommand('copy');
    tempInput.remove();
    $(this).text('Copied!');
    setTimeout(() => {
      $(this).text('Click to copy');
    }, 1000);
  });
  /* End secret key copy */
  
  /* qr code for user 2fa*/

  $('#authy_qr_code').css({
    'background-image': `url('https://chart.googleapis.com/chart?chs=150x150&cht=qr&chl=${auS}')`,
    'background-repeat': 'no-repeat',
    'width': '100px',
    'height': '100px',
    'background-size': '100%',
  });
  /* end qr code for user 2fa*/

  
  addClassForMobile();
  $(window).resize(addClassForMobile);
  
  
  $('.main-content h1').click(function () {
    window.location.replace(window.location.href);
  });
  
});
