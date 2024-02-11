from colour import Color
from rich.text import Text


class ColorConfig:
    @staticmethod
    def green_config():
        return ColorConfig(**{
            'start_color': "#233329",
            'end_color': "#63D471",
            'scale': 5,
            'scale_width': 2
        })

    def __init__(
            self,
            start_color: str = "#000000",
            end_color: str = "#000000",
            scale: int = 1,
            scale_width: int = 1,
            **kwargs):
        self.start_color: Color = Color(kwargs.get('start_color', start_color))
        self.end_color: Color = Color(str(kwargs.get('end_color', end_color)))
        self.scale: int = int(kwargs.get('scale', scale))
        self._colors = list(self.start_color.range_to(self.end_color, self.scale))
        self._scale_width: int = int(kwargs.get('scale_width', scale_width))

    def get_test_gradient(self) -> Text:
        output = Text()
        for i in range(0, 20):
            output.append(f"[{i}: #]", style=self[i])
        return output

    def __getitem__(self, item):
        if item == 0:
            return "white"

        if item >= len(self._colors) * self._scale_width:
            return str(self._colors[-1])

        for count, color in enumerate(self._colors):
            if item < (count + 1) * self._scale_width + 1:
                return str(color)
