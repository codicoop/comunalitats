from io import BytesIO
import zipfile

from django.http import HttpResponse
from django.utils.text import slugify

from cc_courses.models import Activity
from coopolis.storage_backends import PrivateMediaStorage
from dataexports.exports.manager import ExportManager
from coopolis.models import ProjectStage


class ExportFiles:
    """
    Exportació de tots els fitxers en un .zip.
    """
    files = []

    def __init__(self, export_obj):
        self.export_manager = ExportManager(export_obj)

    def export(self):
        self.process_stages()
        self.process_activities()

        file_name = "fitxers.zip"
        response = HttpResponse(
            self.get_zf_contents(),
            content_type="application/x-zip-compressed",
        )
        response["Content-Disposition"] = f"attachment; filename={file_name}"
        return response

    def process_stages(self):
        stages = self.get_project_stages()
        for stage in stages:
            safe_project_name = slugify(stage.project.name)
            self.add_file(
                stage.scanned_certificate.name,
                f"acompanyaments/{safe_project_name}/certificats/",
            )
            for p_file in stage.project.files.all():
                self.add_file(
                    p_file.name,
                    f"acompanyaments/{safe_project_name}/adjunts/",
                )

    def process_activities(self):
        activities = self.get_activities()
        for activity in activities:
            date = activity.date_start.strftime('%Y-%m-%d')
            safe_name = slugify(activity.name)
            folder = f"sessions/{date}/{safe_name}/"
            self.add_file(
                activity.photo1.name,
                folder,
            )
            self.add_file(
                activity.photo2.name,
                folder,
            )
            self.add_file(
                activity.photo3.name,
                folder,
            )
            self.add_file(
                activity.file1.name,
                folder,
            )

    def get_zf_contents(self):
        b = BytesIO()
        zf = zipfile.ZipFile(b, 'w')
        for file in self.files:
            fh = PrivateMediaStorage().open(file["file"])
            safe_file_name = slugify(fh.name)
            try:
                zf.writestr(f"{file['folder']}{safe_file_name}", bytes(fh.read()))
            except Exception as e:
                print(e)
        zf.close()
        return b.getvalue()

    def add_file(self, file_name, folder=""):
        if file_name:
            if PrivateMediaStorage().exists(file_name):
                self.files.append({
                    "folder": folder,
                    "file": file_name,
                })

    def get_project_stages(self):
        return ProjectStage.objects.filter(
            subsidy_period=self.export_manager.subsidy_period
        )

    def get_activities(self):
        return Activity.objects.filter(
            date_start__range=self.export_manager.subsidy_period.range
        )
