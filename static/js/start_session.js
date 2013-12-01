function get_field_value(field_id){
  return $('.ui.form').form('get field', field_id).val()
}

function on_form_submitted(response){
  window.location.assign(response)
}

function initialize_session_form(){
  $('#session_form')
    .form({
        email: {
          identifier: "email",
          rules: [{
            type: "empty",
            prompt: "Please enter your email"
          }],
        },
        deadline: {
          identifier: "deadline",
          rules: [{
            type: "empty",
            prompt: "Please enter ending time"
          }],
        },
        lunch_time: {
          identifier: "lunch_time",
          rules: [{
            type: "empty",
            prompt: "Please enter approx lunch time"
          }],
        },
      },
      {
        onSuccess: function(){
          var form_data = {
            email: get_field_value("email"),
            deadline: get_field_value("deadline"),
            approx_lunch: get_field_value("lunch_time"),
            restaurant: get_field_value("pizza_place"),
            recipients: get_field_value("recipients"),
          }
          $.ajax({
            type: "POST",
            url: "/startsession/",
            data: form_data,
            success: on_form_submitted
          })
        }
      }
    )
}

$(document).ready(function(){
  initialize_session_form();
  $(".ui.selection.dropdown").dropdown();
})
