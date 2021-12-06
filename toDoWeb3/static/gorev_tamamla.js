// Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

$(function () {
    $(document).on('click', '#gorev_buton', function (event) {
        let _i_class    = $(this).find("i").attr("class")
        let _gorev_text = $(this).parent().parent().find("#gorev_text")
        let gorev_id    = _gorev_text.data("id")
        let gerisi      = $(this).parent()

        if (!_i_class.endsWith("success")) {
            $(this).replaceWith(`
                <label id="gorev_buton" class="btn btn-dark active" style="display: none;">
                    <input type="checkbox" checked><i class="fa fa-check text-success" aria-hidden="true"></i>
                </label>
            `.trim())
            $(_gorev_text).replaceWith(`<div id="gorev_text" class="ml-3"><i id="gorev_spin" class="fa fa-spinner fa-spin fa-lg fa-fw mb-3 mr-3" aria-hidden="true"></i> <s>${_gorev_text.text()}</s></div>`)
        } else {
            $(this).replaceWith(`
                <label id="gorev_buton" class="btn btn-dark" style="display: none;">
                    <input type="checkbox"><i class="fa fa-close text-danger" aria-hidden="true"></i>
                </label>
            `.trim())
            $(_gorev_text).replaceWith(`<div id="gorev_text" class="ml-3"><i id="gorev_spin" class="fa fa-spinner fa-spin fa-lg fa-fw mb-3 mr-3" aria-hidden="true"></i> ${_gorev_text.text()}</div>`)
        }

        $.ajax({
            data: {gorev_id},
            type: 'POST',
            url: '/gorev_tamamla',
            complete: function (response) {
                if (response.status != 200) {
                    $('#sol_cikti_alani').html(`<div class="alert alert-warning text-center"><h5 class="alert-head">Bir Hata Oluştu!</h5></div>`)
                }
            }
        }).done(function (data) {
            console.log(data);
            $('#gorev_tablo').append(`
                <tr>
                    <!-- <th scope="row">${data.tarih}</th> -->
                    <th scope="row"><span data-toggle="tooltip" data-placement="top" title="${data.tarih}"><i class="fa fa-calendar" aria-hidden="true"></i> ${data.tarih.split(' ')[1]}</span></th>
                    <td>${data.olay}</td>
                    <td>${data.detay}</td>
                    <td><a href="${data.bsc_scan}" class="alert-link" target=_blank>***${data.tx_hash.substr(-5)}</a></td>
                </tr>
            `);
            gerisi.children().show();
            $('#gorev_spin').remove();
        })

        event.preventDefault();
    })
});