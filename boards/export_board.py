from .models import  Board
import xlwt
from django.template.loader import render_to_string
from weasyprint import HTML
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages



def export_boards_pdf(request, pk):
    board = Board.objects.get(pk=pk)
    topics = board.topic_set.all()
    if len(topics)>1:
        html_string = render_to_string(
            'topic_posts_to_pdf.html', { 'topics': topics, 'board': board})

        html = HTML(string=html_string)
        html.write_pdf(target=f'/tmp/{board.name}.pdf')

        fs = FileSystemStorage('/tmp')
        with fs.open(f'{board.name}.pdf') as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{board.name}.pdf"'
            return response
    else:
        messages.add_message(request,messages.ERROR,'Nothing import top pdf')
        try:
            return redirect(request.META.get('HTTP_REFERER','redirect_if_referer_not_found'))
        except:
            return redirect('home')


def export_boards_xls(request,pk):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="TopicsXml.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Topics')

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['subject', 'board','starter'  ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    rows = Board.objects.get(pk=pk).topic_set.all().values_list('subject', 'board','starter')
    if len(rows)>1:
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)

        wb.save(response)
        return response
    else:
        messages.add_message(request,messages.ERROR,'Nothing import to xls')
        try:
            return redirect(request.META.get('HTTP_REFERER','redirect_if_referer_not_found'))
        except:
            return redirect('home')