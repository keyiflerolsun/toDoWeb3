// Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

$(function () {
    $('#gorev_ekle_buton').on('click', function (event) {
        let yeni_gorev_text = $('#yeni_gorev_text').val();

        if (!yeni_gorev_text) {
            return
        }

        $('#eklendi_tik').hide();
        $("#bekleyin_spin").show()
        $('#yeni_gorev_text').val("")

        $.ajax({
            data: {yeni_gorev_text},
            type: 'POST',
            url: '/gorev_olustur',
            complete: function(response) {
                if (response.status != 200) {
                    $('#sol_cikti_alani').html(`<div class="alert alert-warning text-center"><h5 class="alert-head">Bir Hata Oluştu!</h5></div>`)
                }
            }
        })
        .done(function (data) {
            console.log(data);
            // $('#sol_cikti_alani').html(`
            // <div class="alert alert-success">
            //     <h4 class="alert-head text-center">Başarılı!</h4>

            //     ${data.detay}
            //     </br></br>
            //     <em>Görevi Eklendi...</em>
            // </div>
            // `.trim())
            $('#bekleyin_spin').hide();
            $('#eklendi_tik').show();
            $('#gorev_tablo').append(`
                <tr>
                    <!-- <th scope="row">${data.tarih}</th> -->
                    <th scope="row"><span data-toggle="tooltip" data-placement="top" title="${data.tarih}"><i class="fa fa-calendar" aria-hidden="true"></i> ${data.tarih.split(' ')[1]}</span></th>
                    <td>${data.olay}</td>
                    <td>${data.detay}</td>
                    <td><a href="${data.bsc_scan}" class="alert-link" target=_blank>***${data.tx_hash.substr(-5)}</a></td>
                </tr>
            `);
            $('#yapilacaklar_listesi').append(`
                <li class="list-group-item border-0 d-flex align-items-center ps-0">
                    <div class="btn-group btn-group-toggle" data-toggle="buttons">
                        <label id="gorev_buton" class="btn btn-dark">
                            <input type="checkbox"><i class="fa fa-close text-danger" aria-hidden="true"></i>
                        </label>
                    </div>
                    <div id="gorev_text" data-id="${data.event_args.gorev_id}" class="ml-3">${data.detay}</div>
                </li>
            `);

        })

        event.preventDefault();
    })
});