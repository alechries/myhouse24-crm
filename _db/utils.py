from _db import models
from django.http import HttpResponse
import xlwt

def form_save(form):
    if form.is_valid():
        return form.save()
    else:
        print(form)
        print(form.errors)
        return None


def forms_save(forms):
    for form in forms:
        if not form.is_valid():
            print(form.prefix)
            print(form.errors)
            return False
    for form in forms:
        ins = form.save()
        print(f'Save [{ins}] - {form.prefix}')
    return True


def model_to_xls(xls_name, xls_columns, model_rows):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="{xls_name}.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Transfers')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    for col_num in range(len(xls_columns)):
        ws.write(row_num, col_num, xls_columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    for row in model_rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response