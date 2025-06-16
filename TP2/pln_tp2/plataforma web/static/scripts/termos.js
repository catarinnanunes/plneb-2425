
function delete_termo(designation){
    $.ajax("/termos/"+ designation, {
        type: "DELETE",
        success: function(data) {
            console.log(data)
            if (data["success"]){
                alert(data.message);
                window.location.href = data["redirect_url"]
            } 
        },
        error: function(error){
            console.log(error)
        }
    })
}
    
// para as tabelas funcionarem
// é executado quando a página é carregada
$(document).ready( function () {
    $('#tabela_termos').DataTable({
        "search": {
            "regex": true  // pesquisa com expressões regulares
        }
    });
} );
