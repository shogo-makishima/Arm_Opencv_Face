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
    alert("Stay and not spam on buttons.")
    $.ajax({
        url: "/_send_settings/",
        type: "POST",
        data: { 
            type: 'json',
            cascade: $('select[name$="cascadeSelector"]').children("option:selected").val(),
            port: $('select[name$="portSelector"]').children("option:selected").val(),
            scaleFactor: $('input[name$="scaleFactor"]').val(),
            minNeighbors: $('input[name$="minNeighbors"]').val(),
            area: $('input[name$="area"]').val(),
            key: $('input[name$="keyAccess"]').val(),
        },
        success: function(result) {
            if (result.response == 900){
                alert("Access denied! Uncorrect password! ")
            } else {
                alert("Successfull!")
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
}


function SetOptionsPorts(){
    $.ajax({
        url: "/_get_ports/",
        type: "POST",
        data: { type: 'json' },
        success: function(result) {
            $('select[name$="portSelector"]').find('option').remove().end()
            for (var i = 0; i < result.ports.length; i++) {
                $('select[name$="portSelector"]').append(`<option value="${result.ports[i]}"> ${result.ports[i]} </option>`);
            }
        }
    });
}
