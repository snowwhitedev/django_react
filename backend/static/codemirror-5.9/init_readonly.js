(function(){
    var $ = django.jQuery;
    $(document).ready(function(){
        $('textarea.html-editor').each(function(idx, el){
            var markdwonit= window.markdownit()
                    .use(window.markdownitFootnote)
                    .use(window.markdownitMark)
                    .use(window.markdownitSub)
                    .use(window.markdownitSup);

            el.style = "display:none;"
            var prevHtml = '<div id="preview'+ el.name + '" style="max-height:280px; overflow:auto;"></div>';
            $("#markdowneditor"+el.name).after(prevHtml);
            $("#preview"+el.name).html(markdwonit.render(el.value));
        });
    });
})();