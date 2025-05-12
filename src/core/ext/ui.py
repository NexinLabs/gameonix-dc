import enum
from discord import ui
from discord import Interaction, TextStyle, ButtonStyle



class ButtonStyles(enum.Enum):
    green = ButtonStyle.green
    red = ButtonStyle.red
    grey = ButtonStyle.grey
    blurple = ButtonStyle.blurple


class Button(ui.Button):
    def __init__(self, 
                 label: str, 
                 style: ButtonStyles=ButtonStyle.primary, 
                 emoji: str = None, 
                 custom_id: str = None, 
                 callback=None
    ):
        super().__init__(label=label, style=style, emoji=emoji, custom_id=custom_id)

        if callback:
            self.callback = callback


    @property
    def styles():
        return ButtonStyles
    
class Modal(ui.Modal):
    def __init__(self, title: str, custom_id: str = None):
        super().__init__(title=title, custom_id=custom_id)
        self.text_input = ui.TextInput(label="Input", style=TextStyle.long)
        self.add_item(self.text_input)

    @staticmethod
    async def input(
        interaction:Interaction, 
        title:str="Enter Value", 
        label:str="Enter Value", 
        style:TextStyle=TextStyle.short, 
        custom_id:str=None,
        max_length:int=None, 
        placeholder:str=None
    ) -> str:
        modal = ui.Modal(title=title, custom_id=custom_id)
        modal.add_item(ui.TextInput(label=label, style=style, placeholder=placeholder,  max_length=max_length))
        await interaction.response.send_modal(modal)

        async def mod_val(interaction:Interaction):
            await interaction.response.defer()

        modal.on_submit = mod_val
        await modal.wait()

        if modal.is_finished():
            return modal.children[0].value

__all__ = (
    "CustomButton",
)