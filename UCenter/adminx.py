import xadmin
from xadmin import views

from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side
from xadmin.plugins.inline import Inline
from xadmin.plugins.batch import BatchChangeAction

from UCenter.models import User
from GearArt.models import License


class MainDashboard(object):
    widgets = [
        [
            {"type": "chart", "model": "app.accessrecord", 'chart': 'user_count', 'params': {'_p_date__gte': '2013-01-08', 'p': 1, '_p_date__lt': '2013-01-29'}},
            {"type": "list", "model": "app.host", 'params': {
                'o':'-guarantee_date'}},
        ],
    ]
xadmin.site.register(views.website.IndexView, MainDashboard)


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True
xadmin.site.register(views.BaseAdminView, BaseSetting)

class GlobalSetting(object):
    global_search_models = [User,]

    menu_style = 'accordion'  #'accordion'
xadmin.site.register(views.CommAdminView, GlobalSetting)

#class GearInline(object):
#    model = User
#    style = 'table'
    


class UserAdmin(object):
    list_display = ('user', 'gears', 'reputation')
    list_display_links = ('user',)

    search_fields = ['user']
    relfield_style = 'fk-ajax'
    reversion_enable = True

    actions = [BatchChangeAction, ]
    batch_fields = ('contact', 'create_time')
    
    #inlines = [GearInline]
#xadmin.site.unregister(User)    
#xadmin.site.register(Gear, GearAdmin)
xadmin.site.register(License)