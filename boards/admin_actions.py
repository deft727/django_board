from django.http import HttpResponse
import  csv


def is_not_activ(modeladmin, request, queryset):
    for board in queryset:
        board.is_activ = False
        board.save()


def is_activ(modeladmin, request, queryset):
    for board in queryset:
        board.is_activ = True
        board.save()


def export_boards(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="boards.csv"'
    writer = csv.writer(response)
    writer.writerow(['name', 'description',])
    boards = queryset.values_list('name', 'description', )
    for board in boards:
        writer.writerow(board)
    return response
    


is_not_activ.short_description = 'снять с публикации'
is_activ.short_description = 'опубликовать'
export_boards.short_description = 'Export to csv'