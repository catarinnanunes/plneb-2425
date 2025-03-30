function delete_conceito(designation){ 
    $.ajax("/conceitos/"+ designation, {
        type:"DELETE",
        success: function(data) {
            console.log(data)
            if (data["success"]){
                window.location.href = data["redirect_url"]
            }

        },
        error: function(error) {
            console.log(error)
        }
    })
}

$(document).ready( function () {
    $('#tabela_conceitos').DataTable();
} );