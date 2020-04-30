(function(){
    var $ = django.jQuery;
    $(document).ready(function(){
        
        $('textarea.html-editor').each(function(idx, el){
            
            var prevHtml = '<div id="preview'+ el.name + '" style="max-height:280px; overflow:auto;"></div>';
            $("#markdowneditor"+el.name).after(prevHtml);
            $("#preview"+el.name).hide();
            var editorShow = true;

            var markdwonit= window.markdownit()
                    .use(window.markdownitFootnote)
                    .use(window.markdownitMark)
                    .use(window.markdownitSub)
                    .use(window.markdownitSup);

            var codeEditor = CodeMirror.fromTextArea(el, {
                lineNumbers: true,
                mode: 'markdown',
                buttons: [
                    {
                        class: 'bold',
                        label: '<strong>Prev</strong>',
                        callback: function (cm) {
                            var content = cm.getValue();
                             $("#preview"+el.name).html(markdwonit.render(content));
                            if (editorShow) {
                                $("#markdowneditor"+el.name + "+div .CodeMirror").hide();
                                $("#preview"+el.name).show();
                            } else {
                                $("#markdowneditor"+el.name + "+div .CodeMirror").show();
                                $("#preview"+el.name).hide();
                            }
                            editorShow = !editorShow
                        }
                    }
                ],
            });
            
            var element_id = el.id;
            var label = $("#" + element_id).prev();
            label.css("height","280px");

            var content = codeEditor.getValue();
            $("#preview"+el.name).html(markdwonit.render(content));
        });
    });
})();