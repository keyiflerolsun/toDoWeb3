// Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

$(function () {
    $('#cuzdan_ekle_buton').on('click', function (event) {
        let private_key = $('#private_key').val();
        let cuzdan_adi  = $('#cuzdan_adi').val();

        if (!private_key || !cuzdan_adi) {
            $('#sol_cikti_alani').html(`
                <div class="alert alert-warning">
                    <h4 class="alert-head text-center">Başarısız!</h4>
                    İstenen Bilgileri Eksiksiz Girin..
                </div>
            `.trim())
            return
        }

        $.ajax({
            data: {private_key, cuzdan_adi},
            type: 'POST',
            url: '/cuzdan_ekle',
            complete: function(response) {
                if (response.status === 400) {
                    $('#sol_cikti_alani').html(`<div class="alert alert-warning text-center"><h5 class="alert-head">Bir Hata Oluştu!</h5></div>`)
                }
            }
        })
        .done(function (data) {
            console.log(data);
            $('#sol_panel').html(`
            <div class="alert alert-success">
                <h4 class="alert-head text-center">Bekleyin, Yönlendiriliyor..</h4>

                Cüzdan Hex : <code>${data.cuzdan_hex}</code>
                <br>
                Cüzdan Adı  : <code>${cuzdan_adi}</code>
            </div>
            `.trim())
            setTimeout(function(){ window.location = "/"; }, 0);
        })

        event.preventDefault();
    })
});