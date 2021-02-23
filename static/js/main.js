$(document).ready(function () {
    $('.image-section').hide();
    $('.loader').hide();
    $('#result').hide();

    // Upload Preview
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                let dataURL = reader.result;
                $('#selected-image').attr("src", dataURL);
                base64Image = dataURL.replace(/^data:image\/(png|jpg|jpeg);base64,/, "");
                console.log(base64Image);
            }
            $("#result").text("");
            reader.readAsDataURL(input.files[0]);
        }
    }
    
    $("#imageUpload").change(function () {
        $('.image-section').show();
        $('#btn-predict').show();
        $('#result').text('');
        //$('#result').hide();
        readURL(this);
    });

    $("#btn-predict").click(function(){
        
        // Show loading animation
        $(this).hide();
        $('.loader').show();
            let message = {
            image: base64Image
        }
        console.log(message);
        $.post("http://127.0.0.1:5000/predict", JSON.stringify(message), function(response){
            $('.loader').hide();
            $('#result').fadeIn(600);
            $("#result").text(' Diagnosis status :  ' + response.prediction.result);
            console.log(response);
        });          
    });
});
