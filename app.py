from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserListView
from kivy.core.window import Window
from kivy.uix.slider import Slider
from kivy.uix.popup import Popup

class EnhancedBookReader(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        
        # Create main layout
        self.main_layout = BoxLayout(orientation='vertical')
        
        # Create top toolbar
        self.toolbar = BoxLayout(
            size_hint=(1, 0.1),
            spacing=5,
            padding=5
        )
        
        # Create buttons
        self.open_button = Button(text='Open Book')
        self.font_size_button = Button(text='Font Size')
        
        self.open_button.bind(on_press=self.show_file_chooser)
        self.font_size_button.bind(on_press=self.show_font_settings)
        
        # Add buttons to toolbar
        self.toolbar.add_widget(self.open_button)
        self.toolbar.add_widget(self.font_size_button)
        
        # Create scroll view for text content
        self.scroll_view = ScrollView()
        self.text_content = Label(
            text='Select a book to read',
            size_hint_y=None,
            text_size=(Window.width - 20, None),
            font_size='14sp'
        )
        self.text_content.bind(texture_size=self.text_content.setter('size'))
        
        # Add widgets
        self.scroll_view.add_widget(self.text_content)
        self.add_widget(self.scroll_view)
        self.add_widget(self.toolbar)
        
    def show_file_chooser(self, instance):
        content = BoxLayout(orientation='vertical')
        file_chooser = FileChooserListView(filters=['*.txt'])
        
        # Modified load_book function to accept the additional arguments
        def load_book(chooser, selection, touch=None):
            if selection:  # Check if a file was selected
                try:
                    with open(selection[0], 'r', encoding='utf-8') as file:
                        self.text_content.text = file.read()
                    popup.dismiss()
                except Exception as e:
                    self.text_content.text = f'Error loading file: {str(e)}'
            
        file_chooser.bind(on_submit=load_book)
        content.add_widget(file_chooser)
        
        popup = Popup(
            title='Select Book',
            content=content,
            size_hint=(0.9, 0.9)
        )
        popup.open()
        
    def show_font_settings(self, instance):
        content = BoxLayout(orientation='vertical')
        
        slider = Slider(
            min=10,
            max=30,
            value=14,
            step=1
        )
        
        def change_font_size(instance, value):
            self.text_content.font_size = f'{value}sp'
            
        slider.bind(value=change_font_size)
        content.add_widget(Label(text='Adjust Font Size'))
        content.add_widget(slider)
        
        popup = Popup(
            title='Font Settings',
            content=content,
            size_hint=(0.8, 0.4)
        )
        popup.open()

class EnhancedBookReaderApp(App):
    def build(self):
        return EnhancedBookReader()

if __name__ == '__main__':
    EnhancedBookReaderApp().run()