from PySide6.QtGui import QValidator


class ResolutionValidator(QValidator):
    def __init__(self, min_val, max_val, parent=None):
        super().__init__(parent)
        self.min_val = min_val
        self.max_val = max_val

    def validate(self, input_str, pos):
        if not input_str:
            return QValidator.Intermediate, input_str, pos
        try:
            value = int(input_str)
            if self.min_val <= value <= self.max_val and value % 8 == 0:
                return QValidator.Acceptable, input_str, pos
            else:
                return QValidator.Invalid, input_str, pos
        except ValueError:
            return QValidator.Invalid, input_str, pos

    def fixup(self, input_str):
        try:
            value = max(self.min_val, min(self.max_val, int(input_str)))
            value += -value % 8
            return str(value)
        except ValueError:
            return ""
