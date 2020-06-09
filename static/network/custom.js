$(document).ready(function () {
    // like/unlike utility
    $(".like").click(function () {
        let id = $(this).data('id');
        let text = parseInt($(this).text().replace(" ", ""));

        fetch(`/likeunlike/${id}`)
            .then(res => res.json())
            .then((res) => {
                let {status, message} = res;

                if (status === false) {
                    alert(message);
                }

                if (status === "like") {
                    $(this).text(" " + (text + 1));
                } else if (status === "unlike") {
                    $(this).text(" " + (text - 1));
                }
            })
            .catch(err => {
                alert(err);
            })
    });

    // edit utility that selects post by id. 
    $('.edit').click(function () {
        let id = $(this).data('id');
        $(`#post${id}`).toggleClass('hidden');
    });

    //update post that selects the edited post an submits.
    $('.update-post').click(function () {
        let id = $(this).data('id');
        let content = $(`#edit-content${id}`).val();
        let data = new FormData();
        data.append('content', content);
        data.append('csrfmiddlewaretoken', $("input[name=csrfmiddlewaretoken]").val());

        // using fetch api (promise)
        fetch(`/edit-post/${id}`, {
            method: 'POST',
            body: data,
        })
            .then((response) => response.json())
            .then((data) => {
                $(`#post-content${id}`).text(content);
                $(`#post${id}`).addClass('hidden');
                // $('.edit-post-div').addClass('hidden');
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    })
});