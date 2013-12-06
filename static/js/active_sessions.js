$(document).ready(function(){
  $("#email_modal").modal("setting", {
    onApprove: function(){
      console.log("submitting form");
      $('#modal_form').form("submit");
    }
  });

  $("#modal_form").form({},
  {
    onSuccess: function(){
      var form_data = {
        user_email: get_field_value("user_email"),
        session_name: get_field_value("session_name")
      }
      $.ajax({
        type: "POST",
        url: ".",
        data: form_data,
        success: on_form_submitted
      })
    }
  })
})

function on_form_submitted(response){
  window.location.assign(response)
}

function get_field_value(field_id){
  return $('.ui.form').form('get field', field_id).val()
}

function join(session_name){
  // add hidden field
  $("#modal_header").text("Want to join " + session_name + " ?");
  $("#session_name").val(session_name);
  $("#email_modal").modal("show");
}

