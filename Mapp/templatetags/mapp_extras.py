from django import template

register = template.Library()


@register.filter()
def uppercase(value):
    return value.upper()

@register.filter()
def duplicate(albumitem,duplicate_list):

    is_duplicate = False
    for value in duplicate_list:
        if value['Album_Name'] == albumitem.Album_Name:
            is_duplicate  = True
            break

    if is_duplicate:
        return albumitem.Album_Name +" ("+ str(albumitem.Album_Year)+")"
    else:
        return albumitem.Album_Name