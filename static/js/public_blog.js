window.onload = function () {

    console.log('按钮元素：', $('#submit-btn')[0]);
    console.log('匹配到的元素数量：', $('#submit-btn').length);

    const { createEditor, createToolbar } = window.wangEditor

    const editorConfig = {
        placeholder: 'Type here...',
        onChange(editor) {
            const html = editor.getHtml()
            console.log('editor content', html)
            // 也可以同步到 <textarea>
        },
    }

    const editor = createEditor({
        selector: '#editor-container',
        html: '<p><br></p>',
        config: editorConfig,
        mode: 'default', // or 'simple'
    })

    const toolbarConfig = {}

    const toolbar = createToolbar({
        editor,
        selector: '#toolbar-container',
        config: toolbarConfig,
        mode: 'default', // or 'simple'
    })

    $('#submit-btn').click(function (event) {
        event.preventDefault()
        let title = $('input[name=title]').val()
        let category = $('select[name=category]').val()
        let content = editor.getHtml()
        let csrfToken = $('input[name=csrfmiddlewaretoken]').val()
        if (!title || !content || !category) {
            alert('请输入标题、内容和分类')
            return
        }
        $(this).text('发布中...')
        $(this).prop('disabled', true)
        $.ajax({
            url: '/blog/public/',
            type: 'POST',
            data: {
                title: title,
                content: content,
                category: category,
                csrfmiddlewaretoken: csrfToken,
            },
            success: function (result) {
                alert("发布成功")
                if (result["code"] === 200) {
                    alert(result.toString())
                    let blogId = result["blog_id"]
                    window.location.href = '/blog/detail/' + blogId
                }else{
                    alert(result["message"])
                }
            },
            error: function () {
                alert('发布失败2')
            },
            complete: function () {
                $('#submit-btn').text('发布')
                $('#submit-btn').prop('disabled', false)
            },
        })
    })
}