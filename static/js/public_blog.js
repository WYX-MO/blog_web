window.onload = function () {
    // 检查依赖是否加载
    if (typeof window.wangEditor === 'undefined' || typeof $ === 'undefined') {
        console.error('请先加载 wangEditor 和 jQuery');
        return;
    }

    const { createEditor, createToolbar } = window.wangEditor;

    // 编辑器配置
    const editorConfig = {
        placeholder: '请输入内容...',
        onChange(editor) {
            const html = editor.getHtml();
            console.log('编辑器内容更新:', html);
        },
    };

    // 初始化编辑器
    const editor = createEditor({
        selector: '#editor-container',
        html: '<p><br></p>',
        config: editorConfig,
        mode: 'default',
    });

    // 初始化工具栏
    const toolbar = createToolbar({
        editor,
        selector: '#toolbar-container',
        config: {},
        mode: 'default',
    });

    // 辅助函数：判断编辑器内容是否为空（去除HTML标签后）
    function isContentEmpty(html) {
        return html.replace(/<[^>]+>/g, '').trim() === '';
    }

    // 发布按钮点击事件
    $('#submit-btn').click(function (event) {
        event.preventDefault(); // 阻止默认行为（若按钮是submit类型）

        // 获取表单数据
        const title = $('input[name=title]').val().trim();
        const category = $('select[name=category]').val();
        const content = editor.getHtml();
        const csrfToken = $('input[name=csrfmiddlewaretoken]').val();

        // 表单验证
        if (!title) {
            alert('请输入标题');
            return;
        }
        if (!category) {
            alert('请选择分类');
            return;
        }
        if (isContentEmpty(content)) {
            alert('请输入内容');
            return;
        }

        // 处理提交状态
        const $btn = $(this);
        $btn.text('发布中...').prop('disabled', true);

        // 发送AJAX请求
        $.ajax({
            url: '/blog/public/',
            type: 'POST',
            data: {
                title: title,
                content: content,
                category: category,
                csrfmiddlewaretoken: csrfToken,
            },
            success: function (data) {
                if (data.status === 'success') {
                    alert('发布成功');
                    window.location.href = '/blog/'; // 跳转到博客列表页
                } else {
                    alert('发布失败：' + (data.message || '未知错误'));
                }
            },
            error: function (xhr) {
                alert('发布失败：' + (xhr.responseJSON?.message || '网络错误'));
            },
            complete: function () {
                // 恢复按钮状态
                $btn.text('发布').prop('disabled', false);
            },
        });
    });
};