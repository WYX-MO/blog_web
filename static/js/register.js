$(function () {
    function bond_captcha_event() {
        $('#button-get-captcha').click(function (event) {
            let $this = $(this);
            let email = $('input[name="email"]').val();
            if (!email) {
                alert('请输入邮箱');
                return;
            }
            $this.off('click');
            $this.text('发送中...');
            $.ajax({
                url: '/auth/send_email?email=' + email,
                method: "GET",
                success: function (result) {
                    if (result.code === 200) {
                        alert('验证码发送成功');
                    } else if (result.code === 400) {
                        alert('验证码发送失败');
                        console.log(console.error);
                        $this.text('获取验证码');
                    } else if (result.code === 500) {
                        alert('服务器错误');
                        console.log(console.error);
                        $this.text('获取验证码');
                        bond_captcha_event();
                    }
                    
                }
            });

            let countdown = 5;
            let timer = setInterval(function () {
                if (countdown <= 0) {
                    $this.text('获取验证码');
                    clearInterval(timer);
                    bond_captcha_event();
                } else {
                    $this.text(countdown + '秒后可重发');
                    countdown--;
                }

            }, 1000);
        });
    }

    bond_captcha_event();

});