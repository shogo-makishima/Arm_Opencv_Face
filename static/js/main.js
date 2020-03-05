function UpdateImage(){
    $.ajax({
        url: "/_get_image/",
        type: "POST",
        data: { type: 'json' },
        success: function(result) {
            console.log(result);
            $("#image_canvas").attr("src", "data:image/jpg;charset=utf-8;base64,"+result.image)
        }
    });
}

function SendSettings(){
    $.ajax({
        url: "/_send_settings/",
        type: "POST",
        data: { 
            type: 'json',
            cascade: $('select[name$="cascadeSelector"]').children("option:selected").val(),
            scaleFactor: $('input[name$="scaleFactor"]').val(),
            minNeighbors: $('input[name$="minNeighbors"]').val(),
            area: $('input[name$="area"]').val(),
            key: $('input[name$="keyAccess"]').val(),
        },
        success: function(result) {
            if (result.response == 900){
                alert("Access denied! Uncorrect password! ")
            } else {
                alert("Please, don't spam on button's.")
            }
        }
    });
}

function SetOptionsCascade(){
    $.ajax({
        url: "/_get_cascades/",
        type: "POST",
        data: { type: 'json' },
        success: function(result) {
            $('select[name$="cascadeSelector"]').find('option').remove().end()
            for (var i = 0; i < result.cascades.length; i++) {
                console.log(i);
                $('select[name$="cascadeSelector"]').append(`<option value="${result.cascades[i]}"> ${result.cascades[i]} </option>`);
            }
        }
    });
    /*
    optionText = 'Premium'; 
    optionValue = 'premium'; 
    
    $('select[name$="cascadeSelector"]').find('option').remove().end()
    $('select[name$="cascadeSelector"]').append(`<option value="${optionValue}"> ${optionText} </option>`);
    */
}
