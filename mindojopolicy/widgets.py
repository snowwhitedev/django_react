from django import forms

class HtmlEditor(forms.Textarea):
    def __init__(self, *args, **kwargs):
        super(HtmlEditor, self).__init__(*args, **kwargs)
        self.attrs['class'] = 'html-editor'

    class Media:
        css = {
            'all': (
                'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.9.0/codemirror.css',
                '/static/codemirror-5.9/custom.css'
            )
        }
        js = (
            'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.9.0/codemirror.js',
            'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.9.0/mode/xml/xml.js',
            'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.9.0/mode/htmlmixed/htmlmixed.js',
            'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.9.0/mode/markdown/markdown.js',
            'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.9.0/addon/display/panel.js',
            # "https://cdn.jsdelivr.net/npm/marked/marked.min.js",
            "https://cdnjs.cloudflare.com/ajax/libs/markdown-it/10.0.0/markdown-it.min.js",
            '/static/codemirror-5.9/init.js',
            '/static/codemirror-5.9/markdown-it-footnote.min.js',
            '/static/codemirror-5.9/markdown-it-mark.min.js',
            '/static/codemirror-5.9/markdown-it-sub.min.js',
            '/static/codemirror-5.9/markdown-it-sup.min.js',
            '/static/codemirror-5.9/editor-button.js'
        )

class HtmlEditorQ(forms.Textarea):
    def __init__(self, *args, **kwargs):
        super(HtmlEditorQ, self).__init__(*args, **kwargs)
        self.attrs['class'] = 'html-editor'

    class Media:
        css = {
            'all': (
                'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.9.0/codemirror.css',
                '/static/codemirror-5.9/custom_q.css'
            )
        }
        js = (
            'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.9.0/codemirror.js',
            'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.9.0/mode/xml/xml.js',
            'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.9.0/mode/htmlmixed/htmlmixed.js',
            'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.9.0/mode/markdown/markdown.js',
            'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.9.0/addon/display/panel.js',
            "https://cdnjs.cloudflare.com/ajax/libs/markdown-it/10.0.0/markdown-it.min.js",
            '/static/codemirror-5.9/init_q.js',
            '/static/codemirror-5.9/markdown-it-footnote.min.js',
            '/static/codemirror-5.9/markdown-it-mark.min.js',
            '/static/codemirror-5.9/markdown-it-sub.min.js',
            '/static/codemirror-5.9/markdown-it-sup.min.js',
            '/static/codemirror-5.9/editor-button.js'
        )

class HtmlReadOnly(forms.Textarea):
    def __init__(self, *args, **kwargs):
        super(HtmlReadOnly, self).__init__(*args, **kwargs)
        self.attrs['class'] = 'html-editor'

    class Media:
        js = (
            "https://cdnjs.cloudflare.com/ajax/libs/markdown-it/10.0.0/markdown-it.min.js",
            '/static/codemirror-5.9/init_readonly.js',
            '/static/codemirror-5.9/markdown-it-footnote.min.js',
            '/static/codemirror-5.9/markdown-it-mark.min.js',
            '/static/codemirror-5.9/markdown-it-sub.min.js',
            '/static/codemirror-5.9/markdown-it-sup.min.js'
        )