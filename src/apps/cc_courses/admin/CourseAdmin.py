

from django_summernote.admin import SummernoteModelAdmin
from django.utils.safestring import mark_safe


class CourseAdmin(SummernoteModelAdmin):
    class Media:
        js = ('js/grappellihacks.js',)

    list_display = ('date_start', 'title', 'hours', 'activities_list_field', 'copy_clipboard_list_field',)
    summernote_fields = ('description',)
    readonly_fields = ('copy_clipboard_field', 'created',)
    exclude = ('slug',)
    search_fields = ('date_start', 'title__unaccent', 'description__unaccent',)
    list_filter = ('date_start',)

    def get_queryset(self, request):
        qs = super(CourseAdmin, self).get_queryset(request)
        self.request = request
        return qs

    def activities_list_field(self, obj):
        return mark_safe(u'<a href="../../%s/%s/?course_id__exact=%d">Sessions</a>' % (
            obj._meta.app_label, 'activity', obj.id))

    activities_list_field.short_description = 'Sessions'

    def copy_clipboard_field(self, obj):
        if obj.absolute_url:
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
        else:
            return "(estarà disponible un cop creat)"

    copy_clipboard_field.short_description = "Link a l'acció"

    def copy_clipboard_list_field(self, obj):
        abs_url = self.request.build_absolute_uri(obj.absolute_url)
        return mark_safe("""
    <a href="javascript:copyToClipboard('{0}');">Copiar &#128203;</a>
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

    copy_clipboard_list_field.short_description = "Link a l'acció"
