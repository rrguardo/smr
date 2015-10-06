/*
$(function() {
    var submit_form = function(e) {
      $.getJSON($SCRIPT_ROOT + '/_add_numbers', {
        a: $('input[name="a"]').val(),
        b: $('input[name="b"]').val()
      }, function(data) {
        $('#result').text(data.result);
        $('input[name=a]').focus().select();
      });
      return false;
    };
 
    $('a#calculate').bind('click', submit_form);

    $('input[type=text]').bind('keydown', function(e) {
      if (e.keyCode == 13) {
        submit_form(e);
      }
    });

    $('input[name=a]').focus();
});
*/
