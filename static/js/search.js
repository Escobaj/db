let search_overlay = $("#search")
let search_input = $("#input-search")

search_input.on('change paste keyup', (e) => {
    $.get("/search/" + search_input.val(), (data, status) => {
        search_overlay.html('')
        for (let i = 0; i < data.length; i += 1) {
            search_overlay.append(`
                <div class="search-item">
                    <a class="row" href="/${data[i].type}/${data[i].id}">
                        <div class="col-lg-4">
                            <img src="${data[i].picture || 'https://x1.xingassets.com/assets/frontend_minified/img/users/nobody_m.original.jpg'}" class="search-picture">
                        </div>
                        <div class="col-lg-8">
                            <p>
                                ${data[i].name}
                            </p>
                        </div>
                    </a>
                </div>`
            )
        }
    });
})

search_overlay.width(search_input.outerWidth())
search_overlay.css({
    top: search_input.position().top + 45,
    left: search_input.position().left
})

search_input.focus(() => {
    search_overlay.show();
})

search_input.focusout((e) => {
    setTimeout(() => {
        search_overlay.hide();
    }, 2000)
})