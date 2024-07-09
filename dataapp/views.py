import os
import pandas as pd
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models import Q

from .forms import UploadFileForm, DataFilterForm
from django.views import View
from .models import UploadedFile, FileData
import traceback


class FilteredDataView(View):
    def get(self, request):
        form = DataFilterForm(request.GET or None)
        item = request.GET.get('type', None)

        if item:
            # filtered_data = FileData.objects.filter(Q(name__icontains=item))
            filtered_data = FileData.objects.filter(Q(name__icontains=item) | Q(value__icontains=item))
        else:
            filtered_data = FileData.objects.all()

        if request.headers.get('Accept') == 'application/json':
            data_list = list(filtered_data.values())
            return JsonResponse(data_list, safe=False)
        else:
            return render(request, 'filter.html', {'form': form, 'data': list(filtered_data.values())})


def handle_uploaded_file(uploaded_file):
    """Process and store the uploaded data file."""
    file_name = uploaded_file.name
    file_type = file_name.split('.')[-1].lower()

    # Save the file to the temporary location
    fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'uploads'))
    filename = fs.save(uploaded_file.name, uploaded_file)
    file_path = fs.path(filename)

    try:
        if file_type == 'csv':
            df = pd.read_csv(file_path, encoding='utf-8')
        elif file_type == 'json':
            df = pd.read_json(file_path, typ='series')
            df = pd.DataFrame([df])
        else:
            raise ValueError('Unsupported file type')

        # Clear existing data related to uploaded_file
        UploadedFile.objects.filter(file=uploaded_file).delete()

        # Create UploadedFile instance
        uploaded_file_instance = UploadedFile.objects.create(file=uploaded_file)

        # Save data to FileData model
        for index, row in df.iterrows():
            # Iterate over each row and save its key-value pairs
            for key, value in row.items():
                FileData.objects.create(uploaded_file=uploaded_file_instance, name=key, value=value)

        return True
    except Exception as e:
        print(f"Error reading file with pandas: {e}")
        print("Traceback:", traceback.format_exc())
        raise e
    finally:
        # Clean up the temporary file
        if os.path.exists(file_path):
            os.remove(file_path)


@csrf_exempt
def upload_file(request):
    """View for uploading data files via the web interface."""
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                uploaded_file = form.cleaned_data['file']
                handle_uploaded_file(uploaded_file)
                # messages.success(request, 'File uploaded successfully!')
                return redirect('filtered_data')
            except Exception as e:
                print("Exception occurred. Details:", str(e), "Traceback:", traceback.format_exc())
                messages.error(request, f"{e}")
                return render(request, 'upload.html', {'form': form})
        else:
            # messages.error(request, 'Invalid file type. Only CSV or JSON files are allowed.')
            return render(request, 'upload.html', {'form': form})
    else:
        form = UploadFileForm()
        return render(request, 'upload.html', {'form': form})


# @csrf_exempt
# def query_data(request):
#     item = request.GET.get('type', None)
#     if item:
#         # files = FileData.objects.filter(value__icontains=item)
#         files = FileData.objects.filter(Q(name__icontains=item) | Q(value__icontains=item))
#     else:
#         files = FileData.objects.all()
#
#     data = []
#     for fd in files:
#         data.append({
#             'uploaded_file': fd.uploaded_file.file.url,
#             'name': fd.name,
#             'value': fd.value
#         })
#
#     return JsonResponse(data, safe=False)