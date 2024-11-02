from kivy.uix.anchorlayout import AnchorLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.app import MDApp, StringProperty
from kivy.lang import Builder
from kivymd.uix.bottomnavigation import MDBottomNavigation
from kivymd.uix.button.button import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.chip import MDChip
from kivymd.uix.label.label import MDIcon
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.textfield import MDTextField
from kivymd.uix.menu.menu import MDDropdownMenu
from kivymd.uix.list import OneLineIconListItem
from kivy.metrics import dp
from kivymd.uix.pickers import MDDatePicker
from datetime import date
import utils

SheetManager : utils.sheet_manager = utils.sheet_manager()
sheet_data = SheetManager.get_active_worksheet_data()

class TemplateNavigationBar(MDBottomNavigation):
    pass

class TemplateTopBar(MDTopAppBar):
    pass

class SheetsScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__()
        self.scrollview = MDScrollView(do_scroll_x=False, do_scroll_y=True)
        self.add_widget(self.scrollview)

        self.card_container = GridLayout(cols=1, padding=20, spacing=[0, 20])
        self.card_container.size_hint_y = None
        self.scrollview.add_widget(self.card_container)
        self.card_container.bind(minimum_height=self.card_container.setter("height")) #type: ignore

        for index in range(len(sheet_data)-1, -1, -1):
            card = SheetCard(sheet_data[index])
            card.bind(on_release=lambda x: self.card_function(card.data))
            self.card_container.add_widget(card)

    def card_function(self, data : list):
        self.parent.get_screen("cardview screen").update_form(data)
        self.parent.current = "cardview screen"

class StatisticsScreen(MDScreen):
    pass

class SettingsScreen(MDScreen):
    pass

class FreeCreateButton(AnchorLayout):
    pass


class CardLabel(MDLabel):
    pass

class IconListItem(OneLineIconListItem):
    icon = StringProperty()

class DropDownBase:
    def __init__(self, caller, items=[], position="bottom", width_mult=5):
        self.caller = caller
        self.items = items
        self.menu = MDDropdownMenu(
            caller = self.caller,
            items = self.items,
            position = position,
            width_mult = width_mult
            )
        self.menu.bind()

    def open(self):
        # self.menu.check_position_caller(None, None, None)
        self.menu.open()

    def dropdown_callback(self, text : str):
        self.caller.text = text
        self.menu.dismiss()

class StatusDropdown(DropDownBase):
    choices = [
                {"text": "Paid", "icon": "check-bold"},
                {"text": "Pending", "icon": "alpha-x-circle"},
            ]
    def __init__(self, caller): 
        super().__init__(caller)
        self.items = [{
            "viewclass": "IconListItem",
            "icon": item["icon"],
            "text": item["text"],
            "height": dp(56),
            "on_release": lambda text=item["text"]: self.dropdown_callback(text),
        } for item in self.choices]

class CategoryDropdown(DropDownBase):
    choices = [
                {"text": "food", "icon": "food"},
                {"text": "transportation", "icon": "train-car"},
                {"text": "essentials", "icon": "heart"},
                {"text": "entertainment", "icon": "controller"}
              ]
    def __init__(self, caller):
        super().__init__(caller)
        self.items = [{
            "viewclass": "IconListItem",
            "icon": item["icon"],
            "text": item["text"],
            "height": dp(56),
            "on_release": lambda text=item["text"]: self.dropdown_callback(text),
        } for item in self.choices]

class PaidDropdown(DropDownBase):
    def __init__(self, caller):
        super().__init__(caller)
        self.names = ["Binh", "Hoang"]
        self.items = [{
            "viewclass": "IconListItem",
            "icon": "account",
            "text": name,
            "height": dp(56),
            "on_release": lambda account_name=name: self.dropdown_callback(account_name),
        } for name in self.names]

class FormDatePicker:
    def __init__(self, caller):
        self.caller = caller
        self.date_dialog = MDDatePicker()
        self.date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)

    def open(self):
        self.date_dialog.open()

    def on_cancel(self, *args):
        pass

    def on_save(self, instance, value : date):
        self.caller.text = value.strftime("%d-%m-%Y")
        

class CardViewScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__()
        self.screen_container = GridLayout(cols=1)

        self.form_container = GridLayout(cols=1, padding=10, spacing=10)
        self.add_widget(self.form_container)

        self.product_field = MDTextField(mode="rectangle", hint_text="Product")
        self.price_field = MDTextField(mode="rectangle", hint_text="Price")

        self.date_field = MDTextField(mode="rectangle", hint_text="Date")
        self.date_picker = FormDatePicker(self.date_field)
        self.date_field.bind(focus = lambda obj,focus: self.date_picker.open() if focus else False)

        self.category_field = MDTextField(mode="rectangle", hint_text="Category")
        self.category_dropdown = CategoryDropdown(self.category_field)
        self.category_field.bind(focus = lambda obj,focus: self.category_dropdown.open() if focus else False)

        self.status_field = MDTextField(mode="rectangle", hint_text="Status")
        self.status_dropdown = StatusDropdown(self.status_field)
        self.status_field.bind(focus = lambda obj,focus: self.status_dropdown.open() if focus else False)

        self.paid_for_field = MDTextField(mode="rectangle", hint_text="Paid for")
        self.paid_for_dropdown = PaidDropdown(self.paid_for_field)
        self.paid_for_field.bind(focus = lambda obj,focus: self.paid_for_dropdown.open() if focus else False)

        self.paid_by_field = MDTextField(mode="rectangle", hint_text="Paid by")
        self.paid_by_dropdown = PaidDropdown(self.paid_by_field)
        self.paid_by_field.bind(focus = lambda obj,focus: self.paid_by_dropdown.open() if focus else False)

        self.form_container.add_widget(self.product_field)
        self.form_container.add_widget(self.price_field)
        self.form_container.add_widget(self.date_field)
        self.form_container.add_widget(self.category_field)
        self.form_container.add_widget(self.status_field)
        self.form_container.add_widget(self.paid_for_field)
        self.form_container.add_widget(self.paid_by_field)

    def update_form(self, data : list):
        self.product_field.text = SheetManager.get_data_by_name(data, "product")
        self.price_field.text = SheetManager.get_data_by_name(data, "price") 
        self.date_field.text = SheetManager.get_data_by_name(data, "date")
        self.category_field.text = SheetManager.get_data_by_name(data, "category") 
        self.status_field.text = SheetManager.get_data_by_name(data, "status") 
        self.paid_for_field.text = SheetManager.get_data_by_name(data, "paid for")
        self.paid_by_field.text = SheetManager.get_data_by_name(data, "paid by")

    def cancel_button_callback(self):
        pass

    def save_button_callback(self):
        pass

class CardTextArea(MDBoxLayout):
    price = StringProperty()
    product = StringProperty()
    date = StringProperty()
    def __init__(self, price="", product="", date="", **kwargs):
        super().__init__()
        self.price = price
        self.product = product
        self.date = date
        self.price_label = CardLabel(text=f"Price: {price}")
        self.product_label = CardLabel(text=f"Product: {product}")
        self.date_label = CardLabel(text=f"Date: {date}")
        self.add_widget(self.price_label)
        self.add_widget(self.product_label)
        self.add_widget(self.date_label)
                        

class CardLeftWidget(MDBoxLayout):
    CATEGORY_ICON = {
            "food": ["food", "orange"],
            "transportation": ["train-car", "purple"],
            "essentials": ["heart", "yellow"],
            "entertainment":  ["controller", "green"]
    }

    STATE_COLOR = {
            "paid": {"background": "green", "text": "white"},
            "pending": {"backgroud": "orange", "text": "black"}
    }
    def __init__(self, category="", status="", **kwargs):
        super().__init__()
        self.category = category.lower()
        self.status = status.lower()

        self.secondary_widget = MDChip(text=self.status)
        self.secondary_widget.md_bg_color = self.STATE_COLOR[self.status]["background"]
        self.secondary_widget.text_color = self.STATE_COLOR[self.status]["text"]
        self.secondary_widget.size_hint = (.9, .8)
        self.ids.secondary_container.add_widget(self.secondary_widget)

        self.primary_widget = MDIcon(icon=self.CATEGORY_ICON[self.category][0])
        self.ids.primary_container.md_bg_color = self.CATEGORY_ICON[self.category][1]
        self.ids.primary_container.add_widget(self.primary_widget)


    def modify_icon(self, icon):
        self.primary_widget.icon = icon

    def modify_chip_text(self, text):
        self.secondary_widget.text = text


class SheetCard(ButtonBehavior, MDBoxLayout): #type: ignore
    def __init__(self, data : list,  **kwargs):
        super(SheetCard, self).__init__(**kwargs)
        self.data = data
        self.left_widget = CardLeftWidget(category=SheetManager.get_data_by_name(data, "category"),
                                          status=SheetManager.get_data_by_name(data, "status"))
        self.text_area = CardTextArea(date=SheetManager.get_data_by_name(data, "date"),
                                      product=SheetManager.get_data_by_name(data, "product"),
                                      price=SheetManager.get_data_by_name(data, "price"))
        self.add_widget(self.left_widget)
        self.add_widget(self.text_area)

class Example(MDApp):
    def build(self):
        self.title = "Py-Budgeter"
        self.theme_cls.material_style = "M3"
        return Builder.load_file("./styles.kv")

if __name__ == "__main__":
    Example().run()
