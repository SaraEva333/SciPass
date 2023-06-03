from django.shortcuts import render, redirect,get_object_or_404
from .models import Sciedit, Iff, Quart, Specialty
from django.db.models import Max
import tabula
import re
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, TemplateView, LogoutView
from django.urls import reverse
from django.contrib.auth.models import User,Permission,Group
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from collections import defaultdict
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFont

def mainPageView(request):

    sciedit = Sciedit.objects.order_by('seid')  # Retrieve data from the Sciedit model
    iff = Iff.objects.all()
    quart = Quart.objects.all()
    specialty = Specialty.objects.all()
    return render(request, 'app/main.html', {'Sciedit': sciedit, 'Iff': iff, 'Quart': quart, 'Specialty': specialty,'user.is_authenticated': User.is_authenticated })

def addDataView(request):
    if request.method == 'POST':
        # Retrieve form data
        title = request.POST.get('title')
        issn = request.POST.get('issn')
        if_value = request.POST.get('if_value')
        db_if = request.POST.get('db_if')
        year_if = request.POST.get('year_if')
        current_quartile = request.POST.get('current_quartile')
        db_quart = request.POST.get('db_quart')
        year_quart = request.POST.get('year_quart')
        code = request.POST.get('code')
        dat = request.POST.get('dat')

        # Get the maximum seid value
        max_seid = Sciedit.objects.aggregate(Max('seid'))['seid__max']

        # Increment the max_seid by 1 to get the new seid
        new_seid = max_seid + 1 if max_seid is not None else 1
        # Get the maximum ifid value
        max_ifid = Iff.objects.aggregate(Max('ifid'))['ifid__max']

        # Increment the max_ifid by 1 to get the new ifid
        new_ifid = max_ifid + 1 if max_ifid is not None else 1

        # Get the maximum qid value
        max_qid = Quart.objects.aggregate(Max('qid'))['qid__max']

        # Increment the max_qid by 1 to get the new qid
        new_qid = max_qid + 1 if max_qid is not None else 1

        # Get the maximum spid value
        max_spid = Specialty.objects.aggregate(Max('spid'))['spid__max']

        # Increment the max_spid by 1 to get the new spid
        new_spid = max_spid + 1 if max_spid is not None else 1

        # Create objects and save data
        seid = Sciedit.objects.create(seid=new_seid,title=title, issn=issn)
        Iff.objects.create(ifid=new_ifid, if_value=if_value, db=db_if, year=year_if, seid=seid)
        Quart.objects.create(qid=new_qid, current_quartile=current_quartile, db=db_quart, year=year_quart, seid=seid)
        Specialty.objects.create(spid=new_spid, code=code, dat=dat, seid=seid)

        return redirect('/')

    return render(request, 'app/add.html')

def authView(request):
    return render(request, 'app/auth.html')

def editView(request, pk):
    seid = Sciedit.objects.values_list('seid', flat=True).order_by('seid')[pk]
    sciedit = get_object_or_404(Sciedit, seid=seid)
    iff = get_object_or_404(Iff, seid=seid)
    quart = get_object_or_404(Quart, seid=seid)
    specialty = get_object_or_404(Specialty, seid=seid)

    if request.method == 'POST':
        # Получите данные из формы
        title = request.POST.get('title')
        issn = request.POST.get('issn')
        if_value = request.POST.get('if_value')
        db_if = request.POST.get('db_if')
        year_if = request.POST.get('year_if')
        current_quartile = request.POST.get('current_quartile')
        db_quart = request.POST.get('db_quart')
        year_quart = request.POST.get('year_quart')
        code = request.POST.get('code')
        dat = request.POST.get('dat')

        # Сохранение обновленных данных
        sciedit.title = title
        sciedit.issn = issn
        sciedit.save()

        iff.if_value = if_value.replace(',', '.')
        iff.db = db_if
        iff.year = year_if
        iff.save()

        quart.current_quartile = current_quartile
        quart.db = db_quart
        quart.year = year_quart
        quart.save()

        specialty.code = code
        specialty.dat = dat
        specialty.save()

        return redirect('/')


    return render(request, 'app/edit.html', {'Sciedit': sciedit, 'Iff': iff, 'Quart': quart, 'Specialty': specialty,'pk': pk,'user.is_authenticated': User.is_authenticated })






def allDataView(request, pk):
    seid = Sciedit.objects.values_list('seid', flat=True).order_by('seid')[pk]
    sciedit = get_object_or_404(Sciedit, seid=seid)
    iff = get_object_or_404(Iff, seid=seid)
    quart = get_object_or_404(Quart, seid=seid)
    specialty = get_object_or_404(Specialty, seid=seid)

    scieditAll = Sciedit.objects.order_by('seid')  # Retrieve data from the Sciedit model
    iffAll = Iff.objects.all()
    quartAll = Quart.objects.all()
    specialtyAll = Specialty.objects.all()

    def ifv(db):
        values_str = ""  # Initialize an empty string
        for item in scieditAll:
            if item.title == sciedit.title and item.issn == sciedit.issn:
                for iff in item.iff_set.all():
                    if iff.db == db:
                        if values_str:
                            values_str += '<br>' + str(iff.if_value)  # Use <br> tag for line break
                        else:
                            values_str += str(iff.if_value)  # Convert decimal to string
        return values_str

    def ify(db):
        values_str = ''
        for item in scieditAll:
            if item.title == sciedit.title and item.issn == sciedit.issn :
                for iff in item.iff_set.all():
                    if iff.db == db:
                        if values_str:
                            values_str += '<br>' + str(iff.year)  # Use <br> tag for line break
                        else:
                            values_str += str(iff.year)
        return values_str
    def qv(db):
        values_str = ""  # Initialize an empty string
        for item in scieditAll:
            if item.title == sciedit.title and item.issn == sciedit.issn:
                for quart in item.quart_set.all():
                    if quart.db == db:
                        if values_str:
                            values_str += '<br>' + str(quart.current_quartile)  # Use <br> tag for line break
                        else:
                            values_str += str(quart.current_quartile)  # Convert decimal to string
        return values_str

    def qy(db):
        values_str = ""  # Initialize an empty string
        for item in scieditAll:
            if item.title == sciedit.title and item.issn == sciedit.issn:
                for quart in item.quart_set.all():
                    if quart.db == db:
                        if values_str:
                            values_str += '<br>' + str(quart.year)  # Use <br> tag for line break
                        else:
                            values_str += str(quart.year)  # Convert decimal to string
        return values_str

    def sv():
        values_str = ""  # Initialize an empty string
        for item in scieditAll:
            if item.title == sciedit.title:
                for specialty in item.specialty_set.all():
                        if values_str:
                            values_str += '<br>' + str(specialty.code)  # Use <br> tag for line break
                        else:
                            values_str += str(specialty.code)  # Convert decimal to string
        return values_str

    def sy():
        values_str = ""  # Initialize an empty string
        for item in scieditAll:
            if item.title == sciedit.title:
                for specialty in item.specialty_set.all():
                        if values_str:
                            values_str += '<br>' + str(specialty.dat)  # Use <br> tag for line break
                        else:
                            values_str += str(specialty.dat)  # Convert decimal to string
        return values_str

    vscopus = ifv('Scopus')
    vwos = ifv('WoS')
    vrinc = ifv('РИНЦ')
    yscopus = ify('Scopus')
    ywos = ify('WoS')
    yrinc = ify('РИНЦ')


    qscopus = qv('Scopus')
    qwos = qv('WoS')
    qrinc = qv('РИНЦ')
    qvak = qv('ВАК')
    qyscopus = qy('Scopus')
    qywos = qy('WoS')
    qyrinc = qy('РИНЦ')
    qyvak = qy('ВАК')

    sc=sv()
    sd = sy()

    return render(request, 'app/all.html',
                  {'Sciedit': sciedit, 'vscopus': vscopus, 'vwos': vwos, 'vrinc': vrinc,
                   'yscopus': yscopus, 'ywos': ywos, 'yrinc': yrinc,  'qscopus': qscopus, 'qwos': qwos,
                   'qrinc': qrinc, 'qvak': qvak, 'qyscopus': qyscopus, 'qywos': qywos, 'qyrinc': qyrinc,
                   'qyvak': qyvak, 'scode': sc, 'sdat': sd})

def deleteDataView(request, pk):
    seid = Sciedit.objects.values_list('seid', flat=True).order_by('seid')[pk]
    sciedit = get_object_or_404(Sciedit, seid=seid)
    iff = get_object_or_404(Iff, seid=seid)
    quart = get_object_or_404(Quart, seid=seid)
    specialty = get_object_or_404(Specialty, seid=seid)

    if request.method == 'POST':
        # Удаление объектов
        sciedit.delete()
        iff.delete()
        quart.delete()
        specialty.delete()

        return redirect('/')

    return render(request, 'app/delete.html',
                  {'Sciedit': sciedit, 'Iff': iff, 'Quart': quart, 'Specialty': specialty, 'pk': pk,'user.is_authenticated': User.is_authenticated })



def exportView(request, pk):
    row_indexes = pk.split(',')
    registerFont(TTFont('Arial', 'Arial.ttf'))
    seid_list = Sciedit.objects.values_list('seid', flat=True).order_by('seid')
    selected_seids = [seid_list[int(index)] for index in row_indexes]

    sciedit = Sciedit.objects.filter(seid__in=selected_seids)

    # Generate PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="exported_data.pdf"'

    # Create the PDF object
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    # Define the styles for the paragraphs
    styles = getSampleStyleSheet()
    styles['Normal'].fontName = 'Arial'  # Set the font to Arial

    # Group the publications by name and ISSN
    grouped_publications = defaultdict(list)
    for item in sciedit:
        grouped_publications[(item.title, item.issn)].append(item)

    # Write the data to the PDF
    for publications in grouped_publications.values():
        # Combine the data from multiple publications into one entry
        combined_title = ", ".join(set(item.title for item in publications))
        combined_issn = ", ".join(set(item.issn for item in publications))
        combined_scopus_if = ", ".join(set(f"{item.iff_set.filter(db='Scopus').first().if_value} {item.iff_set.filter(db='Scopus').first().year}" if item.iff_set.filter(db='Scopus').exists() else "" for item in publications))
        combined_scopus_quart = ", ".join(set(f"{item.quart_set.filter(db='Scopus').first().current_quartile} {item.quart_set.filter(db='Scopus').first().year}" if item.quart_set.filter(db='Scopus').exists() else "" for item in publications))
        combined_wos_if = ", ".join(set(f"{item.iff_set.filter(db='WoS').first().if_value} {item.iff_set.filter(db='WoS').first().year}" if item.iff_set.filter(db='WoS').exists() else "" for item in publications))
        combined_wos_quart = ", ".join(set(f"{item.quart_set.filter(db='WoS').first().current_quartile} {item.quart_set.filter(db='WoS').first().year}" if item.quart_set.filter(db='WoS').exists() else "" for item in publications))
        combined_rsci_if = ", ".join(set(f"{item.iff_set.filter(db='РИНЦ').first().if_value} {item.iff_set.filter(db='РИНЦ').first().year}" if item.iff_set.filter(db='РИНЦ').exists() else "" for item in publications))
        combined_rsci_quart = ", ".join(set(f"{item.quart_set.filter(db='РИНЦ').first().current_quartile} {item.quart_set.filter(db='РИНЦ').first().year}" if item.quart_set.filter(db='РИНЦ').exists() else "" for item in publications))
        combined_vac_quart = ", ".join(set(f"{item.quart_set.filter(db='ВАК').first().current_quartile} {item.quart_set.filter(db='ВАК').first().year}" if item.quart_set.filter(db='ВАК').exists() else "" for item in publications))
        combined_specializations = ", ".join(set(f"{item.specialty_set.first().code}, {item.specialty_set.first().dat}" if item.specialty_set.exists() else "" for item in publications))

        elements.append(Paragraph(f'<b>Title of the publication:</b> {combined_title}', styles['Normal']))
        elements.append(Paragraph(f'<b>ISSN:</b> {combined_issn}', styles['Normal']))
        elements.append(Paragraph(f'<b>Scopus impact factor:</b> {combined_scopus_if}', styles['Normal']))
        elements.append(Paragraph(f'<b>Scopus quartile:</b> {combined_scopus_quart}', styles['Normal']))
        elements.append(Paragraph(f'<b>WOS impact factor:</b> {combined_wos_if}', styles['Normal']))
        elements.append(Paragraph(f'<b>WoS quartile:</b> {combined_wos_quart}', styles['Normal']))
        elements.append(Paragraph(f'<b>RSCI impact factor:</b> {combined_rsci_if}', styles['Normal']))
        elements.append(Paragraph(f'<b>RSCI quartile:</b> {combined_rsci_quart}', styles['Normal']))
        elements.append(Paragraph(f'<b>Vac quartile:</b> {combined_vac_quart}', styles['Normal']))
        elements.append(Paragraph(f'<b>Specialization:</b> {combined_specializations}', styles['Normal']))

        elements.append(Spacer(1, 12))  # Add some space between entries

    # Build the PDF document
    doc.build(elements)

    return response



class LoginView(LoginView,TemplateView):
    template_name = "app/login.html"

    def dispatch(self, request, *args, **kwargs):
        context = {}
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                context['error'] = "Логин или пароль неправильные"
        return render(request, self.template_name, context)


class RegisterView(TemplateView):
    template_name = "app/register.html"
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            name = request.POST.get('username')
            first_name = name.split(' ')[0]
            last_name = name.split(' ')[-1]
            username = name.split(' ')[1]
            email = request.POST.get('email')
            password = request.POST.get('password')
            User.objects.create_user(username, email=email, first_name=first_name, last_name=last_name, password=password)
            adept_group = Group.objects.get(name='users')
            user = User.objects.get(username=username)
            user.groups.add(adept_group)
            return redirect(reverse("login"))


        return render(request, self.template_name)

class Logout(LogoutView):
    success_url = '/'


def extract_table_data_quartile(table_text):
    rows = table_text.split('\n')

    table_data = []

    # Пропускаем первую строку, так как это заголовок таблицы
    for i in range(1, len(rows)):
        row = re.sub(r'\\\\?r', ' ', rows[i].strip())  # Replace '\\r' or '\r' with a space

        # Пропускаем пустые строки
        if row == '' :
            continue

        columns = row.split()

        # Проверяем, достаточно ли элементов в списке columns
        if len(columns) >= 3:
            # Извлекаем нужные данные из столбцов
            quartile = ''
            for col in columns:
                if re.match(r'[КQ][1-4]', col):
                    quartile = col
                    break

            publication_name = ''
            for col in columns[1:]:
                if re.match(r'^[КQ][1-4]$', col):
                    break
                publication_name += col.replace("NaN", "") + ' '
            publication_name = publication_name.strip()

            # Если у издания есть квартиль, но отсутствует название, объединяем данные с предыдущей строкой
            if publication_name == '' and quartile == '':
                continue

            # Если у издания есть название, но отсутствует квартиль, используем данные из следующей строки
            if publication_name != '' and quartile == '':
                next_row = re.sub(r'\\\\?r', ' ', rows[i + 1].strip())  # Replace '\\r' or '\r' with a space
                next_columns = next_row.split()
                if len(next_columns) >= 3:
                    for col in next_columns:
                        if re.match(r'[КQ][1-4]', col):
                            quartile = col
                            break
            # Если у издания есть название, но отсутствует квартиль, используем данные из следующей строки
            if publication_name != '' and quartile == '':
               next_row = re.sub(r'\\\\?r', ' ', rows[i + 2].strip())  # Replace '\\r' or '\r' with a space
               next_columns = next_row.split()
               if len(next_columns) >= 3:
                  for col in next_columns:
                      if re.match(r'[КQ][1-4]', col):
                        quartile = col
                        break
            if publication_name == '' and quartile  != '':
                continue
            # Создаем словарь с извлеченными данными
            row_data = {
                'publication_name': publication_name,
                'quartile': quartile.replace(' ', '')
            }

            # Добавляем словарь в список данных таблицы
            table_data.append(row_data)

    return table_data

def extract_table_data(table_text):
    rows = table_text.split('\n')

    table_data = []
    previous_publication_name = None
    previous_issn = None

    # Пропускаем первую строку, так как это заголовок таблицы
    for i in range(8, len(rows)):
        row = re.sub(r'\\\\?r', ' ', rows[i].strip())  # Replace '\\r' or '\r' with a space

        # Пропускаем пустые строки
        if row == '':
            continue

        columns = row.split()

        # Проверяем, достаточно ли элементов в списке columns
        if len(columns) >= 4:
            # Извлекаем нужные данные из столбцов
            number = columns[0]

            # Извлекаем publication_name
            publication_name = ''
            for col in columns[1:]:
                if re.search(r'\(|\d', col):  # Check for "(" or digit
                    if not re.search(r'^\d+\.\d+\.\d+\.$', col) and not re.search(r'^\d{2}\.\d{2}\.\d{2}\. –$',
                                                                                  col) and not re.search(
                            r'^\d+\.\d+\.\d+$', col):
                        break
                publication_name += col + ' '
            publication_name = publication_name.strip()

            # Извлекаем ISSN
            issn = None
            for col in reversed(columns):
                if re.match(r'\d{4}-\d{3}[0-9X]$', col):  # Check for valid ISSN format
                    issn = col.replace("-","")
                    break

            specialty_match = re.findall(
                r'(\d{1,2}\.\d{1,2}\.\d{1,2}\.|\d{1,2}\.\d{1,2}\.\d{1,2} – |\d{2}\.\d{2}\.\d{2}\.|\d{2}\.\d{2}\.\d{2} – )', row)

            if len(specialty_match) > 1:
                for i in range(len(specialty_match) - 1):
                    specialty = specialty_match[i].replace(' – ', '.')
                    specialty = specialty_match[i].replace(' ', '')
                    row_data = {
                        'publication_name': publication_name if publication_name != 'NaN' and  issn is not None else previous_publication_name,
                        'issn': issn.replace(' ', '') if issn is not None and publication_name != 'NaN' else previous_issn,
                        'specialty': specialty.replace(" –",".").replace(' ', '').replace('–', '.'),
                    }
                    table_data.append(row_data)
                    previous_publication_name = publication_name if publication_name != 'NaN' and  issn is not None else previous_publication_name
                    previous_issn = issn.replace(' ', '') if issn is not None and publication_name != 'NaN' else previous_issn
                specialty = specialty_match[-1]

            else:
                specialty = ''
            # Создаем словарь с извлеченными данными
            row_data = {
                'publication_name': publication_name if publication_name != 'NaN' and  issn is not None else previous_publication_name,
                'issn': issn if issn is not None and publication_name != 'NaN' else previous_issn,
                'specialty': specialty.replace(" –",".").replace(' ', '').replace('–', '.'),
            }

            # Добавляем словарь в список данных таблицы
            table_data.append(row_data)
            previous_publication_name = publication_name if publication_name != 'NaN' and  issn is not None else previous_publication_name
            previous_issn = issn.replace(' ', '') if issn is not None and publication_name != 'NaN' else previous_issn

    return table_data
def merge_quartile_data(page_data, table_data):
    merged_data = []

    # Создаем копию page_data_quartile
    remaining_page_data = page_data[:]

    for table_row in table_data:
        publication_name = table_row['publication_name']
        quartile = ""

        for page_row in page_data:
            if page_row['publication_name'] == publication_name:
                quartile = page_row['quartile']
                try:
                    remaining_page_data.remove(page_row)
                except ValueError:
                    pass
                break

        merged_row = dict(table_row)
        merged_row['quartile'] = quartile
        merged_data.append(merged_row)

    # Добавляем оставшиеся записи из remaining_page_data в merged_data
    merged_data.extend(remaining_page_data)

    return merged_data





def addPDFView(request):
    if request.method == 'POST':
        pdf_file = request.FILES.get('pdf_file')
        pdf_file_quartile = request.FILES.get('pdf_file1')
        merged_data = None

        if pdf_file_quartile:
            # Process quartile PDF file
            df_quartile = tabula.read_pdf(pdf_file_quartile, pages='all', lattice=True, multiple_tables=False)
            pdf_text_quartile = ''
            for i in range(len(df_quartile)):
                pdf_text_quartile += df_quartile[i].to_string(index=False)
            page_data_quartile = extract_table_data_quartile(pdf_text_quartile)

            if merged_data is None:
                merged_data = page_data_quartile
            else:
                merged_data = merge_quartile_data(page_data_quartile, merged_data)

        if pdf_file:
            # Process main PDF file
            df = tabula.read_pdf(pdf_file, pages='all', lattice=True, multiple_tables=False)
            pdf_text = ''
            for i in range(len(df)):
                pdf_text += df[i].to_string(index=False)
            table_data = extract_table_data(pdf_text)

            if merged_data is None:
                merged_data = table_data
            else:
                merged_data = merge_quartile_data(merged_data, table_data)
            return render(request, 'app/pdf.html', {'table_data': merged_data})

        if 'save_data' in request.POST:
            title_list = request.POST.getlist('title')
            issn_list = request.POST.getlist('issn')
            if_value_list = request.POST.getlist('if_value')
            db_if_list = request.POST.getlist('db_if')
            year_if_list = request.POST.getlist('year_if')
            current_quartile_list = request.POST.getlist('current_quartile')
            code_list = request.POST.getlist('code')

            # Get the common values for year_quart, db_quart, and dat
            year_quart = request.POST.get('year_quart')
            db_quart = request.POST.get('db_quart')

            num_rows = len(title_list)  # Number of rows in the table

            for i in range(num_rows):
                title = title_list[i]
                issn = issn_list[i]
                if_value = if_value_list[i] if if_value_list[i] != '' else 0
                db_if = db_if_list[i]
                year_if = year_if_list[i] if if_value_list[i] != '' else '0000'
                current_quartile = current_quartile_list[i]
                code = code_list[i]

                # Create objects and save data
                # Get the maximum seid value
                max_seid = Sciedit.objects.aggregate(Max('seid'))['seid__max']

                # Increment the max_seid by 1 to get the new seid
                new_seid = max_seid + 1 if max_seid is not None else 1
                # Get the maximum ifid value
                max_ifid = Iff.objects.aggregate(Max('ifid'))['ifid__max']

                # Increment the max_ifid by 1 to get the new ifid
                new_ifid = max_ifid + 1 if max_ifid is not None else 1

                # Get the maximum qid value
                max_qid = Quart.objects.aggregate(Max('qid'))['qid__max']

                # Increment the max_qid by 1 to get the new qid
                new_qid = max_qid + 1 if max_qid is not None else 1

                # Create objects and save data
                seid = Sciedit.objects.create(seid=new_seid, title=title, issn=issn)
                Iff.objects.create(ifid=new_ifid, if_value=if_value, db=db_if, year=year_if, seid=seid)
                Quart.objects.create(qid=new_qid, current_quartile=current_quartile, db=db_quart, year=year_quart,
                                     seid=seid)

                if code:
                    # Get the maximum spid value
                    max_spid = Specialty.objects.aggregate(Max('spid'))['spid__max']

                    # Increment the max_spid by 1 to get the new spid
                    new_spid = max_spid + 1 if max_spid is not None else 1

                    # Create Specialty object and save data
                    dat = request.POST.get('dat')

                    Specialty.objects.create(spid=new_spid, code=code, dat=dat, seid=seid)

            return redirect('/')

    else:
        return render(request, 'app/pdf.html')