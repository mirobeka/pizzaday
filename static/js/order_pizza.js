function initialize_order_forms(){
  $('.ui.order.form')
    .form(
        {},
        {
          onSuccess: function(){
            var form_data = {
              size: $("input[type=submit][clicked=true]").val(),
              pizza: $(this).form("get field", "pizza").val(),
              extra: $(this).form("get field", "extra").val(),
            }
            console.log(form_data)
            $.ajax({
              type: "POST",
              url: window.location,
              data: form_data,
              success: on_form_submitted
            })
          }
        }
      )
}

$(document).ready(function(){
  $('.ui.accordion').accordion();
  //$('.ui.button').raptorize();
  initialize_order_forms();

  // to determine what
  $(".ui.order.form input[type=submit]").click(function() {
    console.log("sadf")
    $("input[type=submit]", $(this).parents(".ui.order.form")).removeAttr("clicked");
    $(this).attr("clicked", "true");
    $(this).parents(".ui.order.form").form("validate form")
  });
});
