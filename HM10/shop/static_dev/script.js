function add_or_remove_favorite(url ,element, data, csrf_token) {
    $.ajax({
        url: url,
        type: "POST",
        dataType: "json",
        data: JSON.stringify({data: data,}),
        headers: {
                    "X-Requested-With": "XMLHttpRequest",
                    "X-CSRFToken": csrf_token,
                  },
        success: (data) => {
            if (data.action == 'remove') {
                console.log(data);
                element.siblings('#favorite_action').attr('value', 'add');
                element.attr('value', 'Add to favorite');
            };

            if (data.action == 'add') {
                console.log(data);
                element.siblings('#favorite_action').attr('value', 'remove');
                element.attr('value', 'Remove from favorite')
            };

        },
        error: (error) => {
            console.log(error);
        }
  });
 }