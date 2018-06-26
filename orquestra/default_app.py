from confapp import conf
from pyforms_web.basewidget import BaseWidget, no_columns, segment

from pyforms_web.controls.control_button import ControlButton
from pyforms_web.controls.control_text import ControlText
from pyforms_web.controls.control_textarea import ControlTextArea

from pyforms_web.controls.control_combo import ControlCombo
from pyforms_web.controls.control_checkbox import ControlCheckBox
from pyforms_web.controls.control_datetime import ControlDateTime
from pyforms_web.controls.control_list import ControlList
from pyforms_web.controls.control_label import ControlLabel

class DefaultApp(BaseWidget):

    TITLE = 'Demo app'

    LAYOUT_POSITION = 0

    def __init__(self, *args, **kwargs):
        super(DefaultApp, self).__init__(*args, **kwargs)

        self._css_btn = ControlButton(
            '<i class="icon toggle on" ></i>Toggle css', 
            default=self.__toggle_css_evt,
            label_visible=False
        )
        self._toggle_btn = ControlButton(
            '<i class="icon eye" ></i>Toggle visibility', 
            default=self.__toggle_visibility_evt,
            label_visible=False
        )
        self._copy_btn   = ControlButton(
            '<i class="icon copy outline" ></i>Copy the text',
            default=self.__copy_text_evt,
            label_visible=False
        )
        self._input = ControlText('Type something here and press the copy button', changed_event=self.__input_changed_evt)
        self._text  = ControlTextArea('Result')
        self._combo = ControlCombo(
            'Combo',
            items=[('Item 1', 1),('Item 2', 2),('Item 3', 3)]
        )
        self._check = ControlCheckBox('Check box')
        self._list  = ControlList('List')
        self._label = ControlLabel('Label', default='Use the label for a dynamic text')

        self.formset = [
            no_columns('_toggle_btn','_copy_btn', '_css_btn'),
            ' ',
            '_input',
            '_text',
            {
                'Free text': [
                    'h1:Header 1',
                    'h2:Header 2',
                    'h3:Header 3',
                    'h4:Header 4',
                    'h5:Header 5',
                    'h1-right:Header 1',
                    'h2-right:Header 2',
                    'h3-right:Header 3',
                    'h4-right:Header 4',
                    'h5-right:Header 5',
                    '-',
                    'Free text here',
                    'msg:Message text',
                    'info:Info message',
                    'warning:Warning message',
                    'alert:Alert message'
                ],
                'Segments': [
                    'The next example has a segment',
                    segment(
                        '_combo',
                        '_check',
                        css='secondary'
                    ),
                    '_list',
                    '_label'
                ]
            }
        ]

    def __toggle_css_evt(self):
        if self._css_btn.css == 'basic green':
            self._css_btn.css = 'inverted red'
            self._label.css = 'red'
            self._css_btn.label = '<i class="icon toggle on" ></i>Toggle css'
        else:
            self._css_btn.css = 'basic green'
            self._label.css = 'inverted green'
            self._css_btn.label = '<i class="icon toggle off" ></i>Toggle css'

    def __toggle_visibility_evt(self):

        if self._input.visible:
            self._input.hide()
        else:
            self._input.show()

        if self._text.visible:
            self._text.hide()
        else:
            self._text.show()

        if self._copy_btn.visible:
            self._copy_btn.hide()
        else:
            self._copy_btn.show()

        if self._css_btn.visible:
            self._css_btn.hide()
        else:
            self._css_btn.show()
            

    def __copy_text_evt(self):

        self._text.value = self._input.value


    def __input_changed_evt(self):
        print(self._input.value)
