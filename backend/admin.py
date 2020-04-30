from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django import forms
from django.db import models

from django.template.response import TemplateResponse
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from .models import GoogleAccount
from .models import EmailPattern
from .models import Document
from .models import PolicyItem
from .models import Question
from .models import PolicyItemQuestion
from .models import Repetition

from mindojopolicy.widgets import HtmlEditor, HtmlReadOnly, HtmlEditorQ

from .actions.admin.policyitem import savePolicyItems,savePolicyItemsByItems, savePolicyDocId, deletePolicyItemsByDoc, confirmPolicyItems, isValidBody
from .actions.admin.handbook import saveUserHandbook, saveHandbookByUser, deleteHandbookByGroup, deleteHandbookByDoc, saveDocumentStructure
from .actions.admin.repetition import deleteRepItemByDoc, deleteRepItemByQuestion

from mindojopolicy.settings import(
    POLICY_ITEM_IMPORTANCE_HIGH,
    POLICY_ITEM_IMPORTANCE_MEDIUM,
    POLICY_ITEM_IMPORTANCE_LOW
)

global selectedPolicyId
selectedPolicyId = -1
global updatedPolicyIds
updatedPolicyIds = []
global documentError
documentError = False
global parsedPoItems
parsedPoItems = []

class CustomUserInline(admin.StackedInline):
    model = GoogleAccount
    can_delete = False
    verbose_name_plural = 'usergmail'

class CustomUserAdmin(BaseUserAdmin):
    save_on_top = True
    list_display = ('username', 'email',  'first_name', 'last_name', 'is_staff', 'last_login')
    fieldsets = (
        (None, {
            'fields': ('username', 'password' , 'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'is_superuser', 'groups')
        }),
    )
    inlines = [CustomUserInline]

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
    def save_related(self, request, form, formsets, change):
        
        super().save_related(request, form, formsets, change)
        saveHandbookByUser(form.instance.id, form.instance.groups.all())
    
class CustomGroupAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name',)
        }),
    )
    
    def delete_model(self, request, obj):
        deleteHandbookByGroup(obj.id)
        super().delete_model(request, obj)

class DocumentEditorForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['groups'].required = False
        
    class Meta:
        model = Document
        fields = ('title', 'body', 'groups')
        widgets = {
            'body': HtmlEditor(attrs={'style': 'width: 80%; height: 100%;', 'id':'markdowneditorbody'})
        }

class DocumentAdmin(admin.ModelAdmin):
    save_on_top = True
    
    form = DocumentEditorForm
    filter_horizontal = ('groups',)
    fieldsets = (
        (None, {
            'fields': ('title', 'body', 'groups')
        }),
    )

    change_form_template = 'admin/mydocument.html'

    def save_model(self, request, obj, form, change):
        global updatedPolicyIds
        global documentError
        global parsedPoItems
        #save policy items
        if change == True:
            res = savePolicyItemsByItems(parsedPoItems, obj)
        else:
            res = savePolicyItems(obj) #policy items will be saved docId = 1 for new document 
        if res == False:
            documentError =  True
            self.change_view(request=request, object_id=obj.id)
        else:
            obj.policyItems = res[0]
            obj.description = res[1]
            updatedPolicyIds = res[2]
            super().save_model(request, obj, form, change)
            savePolicyDocId(obj.policyItems, obj.id)
            saveDocumentStructure(obj)
            documentError = False
        parsedPoItems = []
    def save_related(self, request, form, formsets, change):
        if not documentError:
            super().save_related(request, form, formsets, change)
            # group change
            saveUserHandbook(form.instance.id, form.instance.groups.all(), form.instance.policyItems, updatedPolicyIds)

    def delete_model(self, request, obj):
        deleteHandbookByDoc(obj.id)
        deleteRepItemByDoc(obj.policyItems)
        super().delete_model(request, obj)
        
    def change_view(self, request, object_id, form_url='', extra_context=None):
        global documentError
        global parsedPoItems
        if documentError: #this is for new objects
            context = {}
            return TemplateResponse(request, "admin/save_document_save_error.html", context)

        if not request.POST.get('documentMainForm') or not object_id:
            extra_context = extra_context or {}
            return super().change_view(
                request, object_id, form_url, extra_context=extra_context,
            )
        else:
            form = self.form(request.POST)
            docBody = request.POST.get('body')

            #checking validating document
            validDoc = isValidBody(docBody)
            if not validDoc:
                context = {
                    'opts': self.model._meta,
                    'obj_id': object_id
                }
                return TemplateResponse(request, "admin/document_invalidbody.html", context)

            res =  confirmPolicyItems(docBody, object_id)
                        
            if res == False:
                context = {
                    'form': form,
                    'opts': self.model._meta,
                    'obj_id': object_id
                }
                return TemplateResponse(request, "admin/save_document_save_error.html", context)
            
            removedPolItems = res['removedItems']
            parsedPoItems = res['items']
            
            if len(removedPolItems) == 0:
                return super().change_view(
                    request, object_id, form_url, extra_context=extra_context,
                )
            context = {
                'form': form,
                'removedPolItems': removedPolItems,
                'opts': self.model._meta,
                'obj_id': object_id
            }
            return TemplateResponse(request, "admin/save_document_confirmation.html", context)
    
class PolicyItemForm(forms.ModelForm):
    model = PolicyItem

    class Meta:
        fields = ('docTitle', 'itemText', 'importance')
        widgets = {
            'docTitle': forms.TextInput(attrs={'readonly':'readonly', 'class': 'vTextField'}),
            'itemText': HtmlReadOnly(attrs={'readonly': 'readonly', 'id':'markdowneditoritemText'}),
            'importance': forms.Select(attrs=None, choices=([POLICY_ITEM_IMPORTANCE_HIGH, 'High'], [POLICY_ITEM_IMPORTANCE_MEDIUM, 'Medium'], [POLICY_ITEM_IMPORTANCE_MEDIUM, 'Low']))
        }
    class Media:
        css = {
            'all': (
                '/static/policy/style.css',
            )
        }
        js = (
            '/static/policy/init.js',
        )

class PolicyItemInline(admin.StackedInline):
    model = PolicyItemQuestion
    # model = PolicyItem
    can_delete = False

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        global selectedPolicyId
        if db_field.name == "questions":
            selectedPolicyId = pId = int(request.path.split('/')[4])
            kwargs["queryset"] = Question.objects.filter(policy_id=pId)
            
        return super().formfield_for_foreignkey(db_field, request, **kwargs)    

class PolicyItemAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ['docTitle', 'itemText']
    list_filter = ['docTitle']
    form = PolicyItemForm
    inlines = [PolicyItemInline]

    change_form_template = 'admin/mypolicyitem.html'
    def has_add_permission(self, request, obj=None):
        return False

    # def has_delete_permission(self, request, obj=None):
    #     return False

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
            return actions

class QuestionForm(forms.ModelForm):
    model = Question

    class Meta:
        fields = '__all__'
        widgets = {
            'question': HtmlEditorQ(attrs={'style': 'width: 80%; height: 100%;', 'id':'markdowneditorquestion'}),
            'answer': HtmlEditorQ(attrs={'style': 'width: 80%; height: 100%;', 'id':'markdowneditoranswer'}),
        }


class QuestionAdmin(admin.ModelAdmin):
    form = QuestionForm
    fieldsets = (
        (None, {
            'fields': ('question', 'answer')
        }),
    )
    def save_model(self, request, obj, form, change):
        global selectedPolicyId
        obj.policy_id = selectedPolicyId
        super().save_model(request, obj, form, change)
        change = True
        if change:
            deleteRepItemByQuestion(obj.id)

    def get_model_perms(self, request):
        return {}
    def delete_model(self, request, obj):
        deleteRepItemByQuestion(obj.id)
        super().delete_model(request, obj)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

admin.site.unregister(Group)
admin.site.register(Group, CustomGroupAdmin)
admin.site.register(EmailPattern)
admin.site.register(Document, DocumentAdmin)

admin.site.register(PolicyItem, PolicyItemAdmin)

admin.site.register(Question, QuestionAdmin)

from .models import CronLog
class CronLogAdmin(admin.ModelAdmin):
    list_display = ['description', 'cron_time']
admin.site.register(CronLog, CronLogAdmin)