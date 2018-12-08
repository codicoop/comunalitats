#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django_summernote.admin import SummernoteModelAdmin
from django.utils.safestring import mark_safe


class CourseAdmin(SummernoteModelAdmin):
    list_display = ('title',)
    summernote_fields = ('objectives',)
    readonly_fields = ('copy_clipboard_field',)

    def get_queryset(self, request):
        qs = super(CourseAdmin, self).get_queryset(request)
        self.request = request
        return qs

    def copy_clipboard_field(self, obj):
        abs_url = self.request.build_absolute_uri(obj.absolute_url)
        return mark_safe("""
    {0} <a href="javascript:copyToClipboard('{0}');"> ─ Copiar &#128203;</a>
    <script>
    function copyToClipboard (str) {{
    var dummy = document.createElement("input");
      document.body.appendChild(dummy);
      dummy.setAttribute("id", "dummy_id");
      document.getElementById("dummy_id").value=str;
      dummy.select();
      document.execCommand("copy");
      document.body.removeChild(dummy);
      alert(str + ' copied.');
    }}
    </script>
    """.format(abs_url))

    copy_clipboard_field.short_description = 'Direcció del curs'
