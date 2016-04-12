from django import template
import locale 

register = template.Library() 


@register.filter(name='currency') # Registration of filters
def currency(value): # Value is sent from template
    try:
        locale.setlocale(locale.LC_ALL,'en_US.UTF-8')
    except:
        locale.setlocale(locale.LC_ALL,'')
    loc = locale.localeconv()
    try:
        value = float(value)
    except ValueError:
        value = 0
    return locale.currency(value, loc['currency_symbol'], grouping=True) #  This just returns a string. If value = 20 then output = '$20.00'