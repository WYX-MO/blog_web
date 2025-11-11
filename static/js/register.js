$(function () {
    // 绑定验证码按钮事件
    function bond_captcha_event() {
        $('#button-get-captcha').click(function (event) {
            const $this = $(this);
            const email = $('input[name="email"]').val().trim();

            // 前端邮箱验证
            if (!email) {
                showError('emailError', '请输入邮箱');
                return;
            }
            if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
                showError('emailError', '请输入有效的邮箱格式');
                return;
            }
            clearError('emailError'); // 清除邮箱错误提示

            // 防止重复点击
            $this.off('click');
            $this.text('发送中...');

            // 发送验证码请求
            $.ajax({
                url: '/auth/send_email?email=' + email,
                method: "GET",
                dataType: 'json', // 明确指定JSON格式
                success: function (result) {
                    if (result.code === 200) {
                        alert('验证码发送成功，请注意查收');
                        startCountdown($this); // 开始倒计时
                    } else if (result.code === 400) {
                        alert('发送失败：' + result.msg);
                        $this.text('获取验证码');
                        bond_captcha_event(); // 重新绑定事件
                    } else if (result.code === 500) {
                        alert('服务器错误：' + result.msg);
                        $this.text('获取验证码');
                        bond_captcha_event();
                    }
                },
                error: function (xhr) {
                    alert('请求失败，请稍后再试');
                    $this.text('获取验证码');
                    bond_captcha_event();
                }
            });
        });
    }

    // 验证码倒计时
    function startCountdown($btn) {
        let countdown = 60;
        const timer = setInterval(function () {
            if (countdown <= 0) {
                $btn.text('获取验证码');
                clearInterval(timer);
                bond_captcha_event(); // 重新绑定点击事件
            } else {
                $btn.text(countdown + '秒后可重发');
                countdown--;
            }
        }, 1000);
    }

    // 显示错误提示
    function showError(elementId, message) {
        const $element = $('#' + elementId);
        $element.text(message);
        // 给对应输入框添加红色边框
        if (elementId === 'usernameError') {
            $('#exampleInputUsername1').addClass('is-invalid');
        } else if (elementId === 'emailError') {
            $('#exampleInputEmail1').addClass('is-invalid');
        } else if (elementId === 'captchaError') {
            $('input[name="captcha"]').addClass('is-invalid');
        } else if (elementId === 'passwordError') {
            $('#exampleInputPassword1').addClass('is-invalid');
        }
    }

    // 清除错误提示
    function clearError(elementId) {
        const $element = $('#' + elementId);
        $element.text('');
        // 移除输入框红色边框
        if (elementId === 'usernameError') {
            $('#exampleInputUsername1').removeClass('is-invalid');
        } else if (elementId === 'emailError') {
            $('#exampleInputEmail1').removeClass('is-invalid');
        } else if (elementId === 'captchaError') {
            $('input[name="captcha"]').removeClass('is-invalid');
        } else if (elementId === 'passwordError') {
            $('#exampleInputPassword1').removeClass('is-invalid');
        }
    }

    // 注册表单提交处理
    $('#registerForm').submit(function (e) {
        e.preventDefault(); // 阻止默认提交，用AJAX处理
        const formData = $(this).serialize();

        // 清除所有错误提示
        $('.error-msg').text('');
        $('.form-control').removeClass('is-invalid');

        $.ajax({
            url: $(this).attr('action'),
            method: 'POST',
            data: formData,
            dataType: 'json',
            success: function (result) {
                if (result.code === 200) {
                    alert('注册成功，即将跳转到登录页');

                } else {
                    // 显示字段错误
                    const errors = result.errors || {};
                    if (errors.username) showError('usernameError', errors.username[0]);
                    if (errors.email) showError('emailError', errors.email[0]);
                    if (errors.captcha) showError('captchaError', errors.captcha[0]);
                    if (errors.password) showError('passwordError', errors.password[0]);
                }
            },
            error: function () {
                alert('服务器错误，请稍后再试');
            }
        });
    });

    // 初始化验证码事件绑定
    bond_captcha_event();
});