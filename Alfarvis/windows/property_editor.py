#!/usr/bin/env python3


class PropertyEditor(object):
    property_editor_class = None
    parent_widget = None
    previous_property_editor = None

    @classmethod
    def addPropertyEditor(self, property_editor):
        if self.parent_widget is not None:
            self.closePreviousPropertyEditor()
            self.parent_widget.addWidget(property_editor)
            self.previous_property_editor = property_editor
            self.parent_widget.setStretchFactor(1, 1)
            self.parent_widget.update()

    @classmethod
    def closePreviousPropertyEditor(self):
        if self.previous_property_editor is not None:
            self.previous_property_editor.close()
            self.parent_widget.update()
        self.previous_property_editor = None
