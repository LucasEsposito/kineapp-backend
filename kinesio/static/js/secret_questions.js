answer_input = $('#answer');
answer_button = $('#answer_button');

answer_input.on("change keyup paste", function(){
    answer_input.popover('hide');
    answer_button.popover('hide');
    answer_input.removeClass('animated bounce')
})

function check_answer(){
    if (answer_input.val() == "") {
        answer_input.addClass('animated bounce');
        answer_input.popover('show');

    } else {
        let question_id = $('#questionSelector').val();
        let google_token=sessionStorage.google_token;
        $.ajax({
            type: 'POST',
            url: 'api/v1/login/',
            data: {
                'secret_question_id': question_id,
                'google_token': google_token,
                'answer': answer_input.val()
            },
            success: function(response) {
                sessionStorage.setItem('token', response.token);
                console.log('Log In Successfuly Summited ' + response.token);
                $('#modalGeneric').modal('hide');
                location.reload()
            },
            error: function(response){
                answer_input.addClass('animated bounce');
                console.log(response);
                let popover= answer_button.popover(
                    {content: response.responseJSON.message}
                );
                answer_button.popover('show')
            },
        });

        return false;
    }
}