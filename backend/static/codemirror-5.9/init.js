(function(){
    var $ = django.jQuery;
    $(document).ready(function(){
        var maxPolicyId = 0;
        $.ajax({
            url: '/ajax/getMaxPolicyItemId/',
            data:{'user': 'user'},
            dataType: 'json',
            success: function(data){
                maxPolicyId = data['id__max'] == null ? 1: parseInt(data['id__max']) + 1;
            }
        });
        $('textarea.html-editor').each(function(idx, el){
            var mainForm = "<input type='hidden' name='documentMainForm' value='mainform'>"
            $("#markdowneditor"+el.name).after(mainForm);
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
                        label: '<strong>PI</strong>',
                        callback: function (cm) {
                            var selection = cm.getSelection();
                            var prevCursorPos = cm.getCursor();
                            var tagStr_start = `\n@POLICYITEM[${maxPolicyId}]\n`;
                            var tagStr_end = `\n@ENDPOLICYITEM\n`;
                            cm.replaceSelection( tagStr_start + selection + tagStr_end);
                            var curCursorPos = cm.getCursor();
                            cm.markText(
                                {line:prevCursorPos.line + 1, ch:0},
                                {line:prevCursorPos.line + 1, ch:prevCursorPos.ch + tagStr_start.length},
                                {css:"color:red"}
                            );
                            
                            cm.markText(
                                {line:curCursorPos.line - 1, ch: 0},
                                {line:curCursorPos.line - 1, ch: tagStr_end.length - 1},
                                {css:"color:red"}
                            );
                            if (!selection) {
                                cm.setCursor(prevCursorPos.line + 1, 0);
                            }
                            maxPolicyId++;
                        }
                    },
                    {
                        class: 'bold',
                        label: '<strong>Prev</strong>',
                        callback: function (cm) {
                            var content = cm.getValue();
                            // $("#preview"+el.name).html(marked(content));
                            $("#preview"+el.name).html(markdwonit.render(content));
                            if (editorShow) {
                                $(".CodeMirror").hide();
                                $("#preview"+el.name).show();
                            } else {
                                $(".CodeMirror").show();
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

            $("#check_document").on('click', function(e){
                e.preventDefault();
                var docBody = codeEditor.getValue()
                $.ajax({
                     url: '/ajax/checkValidBody/',
                     data:{'docBody': docBody},
                     dataType: 'json',
                     success: function(data){
                        if (!data.valid){
                            alert("There are some policy items colliding Id with existing ones. Check and submit again!");
                        }
                        else {
                            $("#add_document").click();
                        }
                     }
                 });
            })
        });
    });
})();