#---------------------------------------------------------------------------------------------------------------------#
# Comfyroll Custom Nodes by RockOfFire and Akatsuzi     https://github.com/RockOfFire/ComfyUI_Comfyroll_CustomNodes                             
# for ComfyUI                                           https://github.com/comfyanonymous/ComfyUI                                               
#---------------------------------------------------------------------------------------------------------------------#

import numpy as np
import torch
import os 
from PIL import Image, ImageDraw, ImageOps, ImageFont
from ..categories import icons
from ..config import color_mapping, COLORS
from ..nodes.graphics_functions import (hex_to_rgb,
                                 get_color_values,
                                 text_panel,
                                 combine_images,
                                 apply_outline_and_border,
                                 get_font_size,
                                 draw_text_on_image,
                                 crop_and_resize_image)                                                       

font_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "fonts")       
file_list = [f for f in os.listdir(font_dir) if os.path.isfile(os.path.join(font_dir, f)) and f.lower().endswith(".ttf")]

#try:
#    import Markdown
#except ImportError:
#    import pip
#    pip.main(['install', 'Markdown'])

#---------------------------------------------------------------------------------------------------------------------#
        
ALIGN_OPTIONS = ["top", "center", "bottom"]                 
ROTATE_OPTIONS = ["text center", "image center"]
JUSTIFY_OPTIONS = ["left", "center", "right"]
PERSPECTIVE_OPTIONS = ["top", "bottom", "left", "right"]

#---------------------------------------------------------------------------------------------------------------------#

def tensor2pil(image):
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))

def pil2tensor(image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0) 
    
#---------------------------------------------------------------------------------------------------------------------#
class CR_MultiPanelMemeTemplate:

    @classmethod
    def INPUT_TYPES(s):

        font_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "fonts")       
        file_list = [f for f in os.listdir(font_dir) if os.path.isfile(os.path.join(font_dir, f)) and f.lower().endswith(".ttf")]
        templates = ["vertical - 2 image + 2 text",
                     "vertical - 3 image + 3 text",
                     "vertical - 4 image + 4 text",
                     "horizontal - 2 image + 2 text",
                     "horizontal - text bar + 2 image",
                     "text bar + 1 image with overlay text",
                     "text bar + 4 image",
                     "text bar + 4 image with overlay text"] 
        colors = COLORS[1:]                     
        
        return {"required": {
                "template": (templates,),
                "image_1": ("IMAGE",),
                "text_1": ("STRING", {"multiline": True, "default": "text_1"}),
                "text_2": ("STRING", {"multiline": True, "default": "text_2"}),
                "text_3": ("STRING", {"multiline": True, "default": "text_3"}),
                "text_4": ("STRING", {"multiline": True, "default": "text_4"}),              
                "font_name": (file_list,),
                "font_size": ("INT", {"default": 50, "min": 1, "max": 1024}),
                "font_color": (colors,),
                "bar_color": (colors,),
                "reverse_panels": (["No", "Yes"],),
               },
                "optional": {
                "image_2": ("IMAGE",),
                "image_3": ("IMAGE",),
                "image_4": ("IMAGE",),
                }        
    }

    RETURN_TYPES = ("IMAGE", "STRING", )
    RETURN_NAMES = ("image", "show_help", )
    FUNCTION = "draw_text"
    CATEGORY = icons.get("Comfyroll/Graphics/Template")

    def draw_text(self, template, image_1, text_1, text_2, text_3, text_4,
                  font_name, font_size, font_color, bar_color, reverse_panels, image_2 = None, image_3 = None, image_4 = None):
        
        show_help = "example help text"
        
        # Convert the PIL image back to a torch tensor
        return image_1, show_help,

#---------------------------------------------------------------------------------------------------------------------#
class CR_PopularMemeTemplates:

    @classmethod
    def INPUT_TYPES(s):

        templates = ["Expanding brain",
                     "My honest reaction",
                     "The GF I want",
                     "Who would win?",
                     "I have 4 sides",
                     "This is Fine",
                     "Is This a Pigeon?",
                     "Drake hotline bling"]
        colors = COLORS[1:]                
        
        return {"required": {
                "meme": (templates,),
                "image_1": ("IMAGE",),
                        
                "text_1": ("STRING", {"multiline": True, "default": "text_1"}),
                "text_2": ("STRING", {"multiline": True, "default": "text_2"}),
                "text_3": ("STRING", {"multiline": True, "default": "text_3"}),
                "text_4": ("STRING", {"multiline": True, "default": "text_4"}),
                "font_name": (file_list,),
                "font_size": ("INT", {"default": 50, "min": 1, "max": 1024}),
                "font_color": (colors,),
               },
                "optional": {
                "image_2": ("IMAGE",), 
                "image_3": ("IMAGE",),
                "image_4": ("IMAGE",),
               }
    }

    RETURN_TYPES = ("IMAGE", "STRING", )
    RETURN_NAMES = ("image", "show_help", )
    FUNCTION = "draw_text"
    CATEGORY = icons.get("Comfyroll/Graphics/Template")

    def draw_text(self, meme, image_1, text_1, text_2, text_3, text_4,
                  font_name, font_size, font_color, image_2 = None, image_3 = None, image_4 = None):

        show_help = "example help text"
        
        # Convert the PIL image back to a torch tensor
        return image_1, show_help,    

#---------------------------------------------------------------------------------------------------------------------#
class CR_DrawPerspectiveText:
    
    @classmethod
    def INPUT_TYPES(s):
                        
        return {"required": {
                "image_width": ("INT", {"default": 512, "min": 64, "max": 2048}),
                "image_height": ("INT", {"default": 512, "min": 64, "max": 2048}),  
                "text": ("STRING", {"multiline": True, "default": "text"}),
                "font_name": (file_list,),
                "font_size": ("INT", {"default": 50, "min": 1, "max": 1024}),
                "font_color": (COLORS,),
                "background_color": (COLORS,),
                "align": (ALIGN_OPTIONS,),
                "justify": (JUSTIFY_OPTIONS,),
                "margins": ("INT", {"default": 0, "min": -1024, "max": 1024}),
                "line_spacing": ("INT", {"default": 0, "min": -1024, "max": 1024}),
                "position_x": ("INT", {"default": 0, "min": -4096, "max": 4096}),
                "position_y": ("INT", {"default": 0, "min": -4096, "max": 4096}),
                "perspective_factor": ("FLOAT", {"default": 0.00, "min": 0.00, "max": 1.00, "step": 0.01}),
                "perspective_direction": (PERSPECTIVE_OPTIONS,),          
                },
                "optional": {
                "font_color_hex": ("STRING", {"multiline": False, "default": "#000000"}),
                "bg_color_hex": ("STRING", {"multiline": False, "default": "#000000"})
                }          
    }

    RETURN_TYPES = ("IMAGE", "STRING", )
    RETURN_NAMES = ("image", "show_help", )
    FUNCTION = "draw_text"
    CATEGORY = icons.get("Comfyroll/Graphics/Text")

    def draw_text(self, image_width, image_height, text,
                  font_name, font_size, font_color, background_color,
                  margins, line_spacing,
                  position_x, position_y,
                  align, justify,
                  perspective_factor, perspective_direction,
                  font_color_hex='#000000', bg_color_hex='#000000'):

        # Get RGB values for the text and background colors
        text_color = get_color_values(font_color, font_color_hex, color_mapping)
        bg_color = get_color_values(background_color, bg_color_hex, color_mapping)   
        
        # Create PIL images for the text and background layers and text mask
        size = (image_width, image_height)
        text_image = Image.new('RGB', size, text_color)
        back_image = Image.new('RGB', size, bg_color)
        text_mask = Image.new('L', back_image.size)

        # Draw the text on the text mask
        text_mask = draw_masked_text_v2(text_mask, text, font_name, font_size,
                                        margins, line_spacing,
                                        position_x, position_y,
                                        align, justify,
                                        perspective_factor, perspective_direction)

        # Composite the text image onto the background image using the rotated text mask
        image_out = Image.composite(text_image, back_image, text_mask)
        preview_out = text_mask
        
        show_help = "example help text"
        
        # Convert the PIL image back to a torch tensor
        return pil2tensor(image_out), pil2tensor(preview_out), show_help,  

#---------------------------------------------------------------------------------------------------------------------#
class CR_OverlayTransparentImage:
    
    @classmethod
    def INPUT_TYPES(s):
                  
        return {"required": {
                "back_image": ("IMAGE",),
                "overlay_image": ("IMAGE",),
                "align": (ALIGN_OPTIONS, ),
                "transparency": ("FLOAT", {"default": 0, "min": 0, "max": 1, "step": 0.1}),
                "position_x": ("INT", {"default": 0, "min": -4096, "max": 4096}),
                "position_y": ("INT", {"default": 0, "min": -4096, "max": 4096}),
                "rotation_angle": ("FLOAT", {"default": 0.0, "min": -360.0, "max": 360.0, "step": 0.1}),
                }        
        }

    RETURN_TYPES = ("IMAGE", )
    FUNCTION = "overlay_image"
    CATEGORY = icons.get("Comfyroll/Graphics/Layout")

    def overlay_image(self, back_image, overlay_image, align,
                      transparency, position_x, position_y, rotation_angle):
        
        # Convert tensor images
        #back_image = back_image[0, :, :, :]
        #overlay_image = overlay_image[0, :, :, :]

        # Create PIL images for the text and background layers and text mask
        back_image = tensor2pil(back_image)
        overlay_image = tensor2pil(overlay_image)

        # Apply transparency to overlay image
        overlay_image.putalpha(int(255 * (1 - transparency)))

        # Rotate overlay image
        overlay_image = overlay_image.rotate(rotation_angle, expand=True)

        # Calculate the new size of the back image considering the rotated overlay image
        new_size = (max(back_image.width, position_x + overlay_image.width),
                    max(back_image.height, position_y + overlay_image.height))

        # Create a new back image with the updated size
        new_back_image = Image.new('RGBA', new_size, (0, 0, 0, 0))

        # Paste the original back image onto the new back image
        new_back_image.paste(back_image, (0, 0))

        # Paste the rotated overlay image onto the new back image at the specified position
        new_back_image.paste(overlay_image, (position_x, position_y), overlay_image)

        # Convert the PIL image back to a torch tensor
        return pil2tensor(new_back_image),

#---------------------------------------------------------------------------------------------------------------------#
class CR_SimpleAnnotations:

    @classmethod
    def INPUT_TYPES(s):

        bar_opts = ["top", "bottom", "top and bottom", "no bars"]      
        
        return {"required": {
                "image": ("IMAGE",),  
                "text_top": ("STRING", {"multiline": True, "default": "text_top"}),
                "text_bottom": ("STRING", {"multiline": True, "default": "text_bottom"}),
                "font_name": (file_list,),
                "max_font_size": ("INT", {"default": 100, "min": 50, "max": 150}),
                "font_color": (COLORS,),
                "bar_color": (COLORS,),
                "bar_options": (bar_opts,),
                "bar_scaling_factor": ("FLOAT", {"default": 0.2, "min": 0.1, "max": 2, "step": 0.1}),
                },
                "optional": {
                "font_color_hex": ("STRING", {"multiline": False, "default": "#000000"}),
                "bar_color_hex": ("STRING", {"multiline": False, "default": "#000000"})
                }
    }

    RETURN_TYPES = ("IMAGE", "STRING", )
    RETURN_NAMES = ("image", "show_help", )
    FUNCTION = "make_meme"
    CATEGORY = icons.get("Comfyroll/Graphics/Text")

    def make_meme(self, image,
                  text_top, text_bottom,
                  font_name, max_font_size,
                  font_color, bar_color, bar_options, bar_scaling_factor,
                  font_color_hex='#000000',
                  bar_color_hex='#000000'):

        text_color = get_color_values(font_color, font_color_hex, color_mapping)
        bar_color = get_color_values(bar_color, bar_color_hex, color_mapping)              

        # Convert tensor images
        image_3d = image[0, :, :, :]

        # Calculate the height factor
        if bar_options == "top":
            height_factor = 1 + bar_scaling_factor
        elif bar_options == "bottom":
            height_factor = 1 + bar_scaling_factor
        elif bar_options == "top and bottom":
            height_factor = 1 + 2 * bar_scaling_factor
        else:
            height_factor = 1.0

        # Create PIL images for the image and text bars
        back_image = tensor2pil(image_3d)   
        size = back_image.width, int(back_image.height * height_factor)
        result_image = Image.new("RGB", size)

        # Define font settings
        font_file = "fonts\\" + str(font_name)
        resolved_font_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), font_file)
    
        # Create the drawing context
        draw = ImageDraw.Draw(result_image)
 
        # Create two color bars at the top and bottom
        bar_width = back_image.width
        bar_height = back_image.height // 5    ### add parameter for this in adv node
        top_bar = Image.new("RGB", (bar_width, bar_height), bar_color)
        bottom_bar = Image.new("RGB", (bar_width, bar_height), bar_color)

        # Composite the result image onto the input image
        if bar_options == "top" or bar_options == "top and bottom":
            image_out = result_image.paste(back_image, (0, bar_height))
        else:
            image_out = result_image.paste(back_image, (0, 0))
        
        # Get the font size and draw the text
        if bar_options == "top" or bar_options == "top and bottom":
            result_image.paste(top_bar, (0, 0))
            font_top = get_font_size(draw, text_top, bar_width, bar_height, resolved_font_path, max_font_size)
            draw_text_on_image(draw, 0, bar_width, bar_height, text_top, font_top, text_color, "No")
            
        if bar_options == "bottom" or bar_options == "top and bottom":
            result_image.paste(bottom_bar, (0, (result_image.height - bar_height)))
            font_bottom = get_font_size(draw, text_bottom, bar_width, bar_height, resolved_font_path, max_font_size)
            if bar_options == "bottom":
                y_position = back_image.height
            else:
                y_position = bar_height + back_image.height
            draw_text_on_image(draw, y_position, bar_width, bar_height, text_bottom, font_bottom, text_color, "No")

        # Overlay text on image
        if bar_options == "bottom" and text_top > "":
            font_top = get_font_size(draw, text_top, bar_width, bar_height, resolved_font_path, max_font_size)
            draw_text_on_image(draw, 0, bar_width, bar_height, text_top, font_top, text_color, "No")

        if (bar_options == "top" or bar_options == "none") and text_bottom > "":
            font_bottom = get_font_size(draw, text_bottom, bar_width, bar_height, resolved_font_path, max_font_size)
            y_position = back_image.height
            draw_text_on_image(draw, y_position, bar_width, bar_height, text_bottom, font_bottom, text_color, "No")

        if bar_options == "none" and text_bottom > "":
            font_bottom = get_font_size(draw, text_bottom, bar_width, bar_height, resolved_font_path, max_font_size)
            y_position = back_image.height - bar_height
            draw_text_on_image(draw, y_position, bar_width, bar_height, text_bottom, font_bottom, text_color, "No")
 
        show_help = "example help text"
        
        image_out = np.array(result_image).astype(np.float32) / 255.0
        image_out = torch.from_numpy(image_out).unsqueeze(0)          
        
        # Convert the PIL image back to a torch tensor
        #return (pil2tensor(image_out), show_help, )
        return (image_out, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_ApplyAnnotations:

    @classmethod
    def INPUT_TYPES(s):

        font_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "fonts")       
        file_list = [f for f in os.listdir(font_dir) if os.path.isfile(os.path.join(font_dir, f)) and f.lower().endswith(".ttf")]
        bar_opts = ["no bars", "top", "bottom", "top and bottom"]      
        
        return {"required": {
                "image": ("IMAGE", ),  
                "annotation_stack": ("ANNOTATION_STACK", ),
                }
    }

    RETURN_TYPES = ("IMAGE", "STRING", )
    RETURN_NAMES = ("image", "show_help", )
    FUNCTION = "apply_annotations"
    CATEGORY = icons.get("Comfyroll/Graphics/Text")

    def apply_annotations(self, image, annotation_stack):

        show_help = "example help text"

        return (image_out, show_help, )

#---------------------------------------------------------------------------------------------------------------------#
class CR_AddAnnotation:

    @classmethod
    def INPUT_TYPES(s):

        font_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "fonts")       
        file_list = [f for f in os.listdir(font_dir) if os.path.isfile(os.path.join(font_dir, f)) and f.lower().endswith(".ttf")]
        bar_opts = ["no bars", "top", "bottom", "top and bottom"]      
        
        return {"required": {
                "text": ("STRING", {"multiline": True, "default": "text_top"}),
                "font_name": (file_list,),
                "font_size": ("INT", {"default": 100, "min": 20, "max": 150}),
                "font_color": (COLORS,),
                "position_x": ("INT", {"default": 0, "min": 0, "max": 4096}),
                "position_y": ("INT", {"default": 0, "min": 0, "max": 4096}),
                "justify": (JUSTIFY_OPTIONS,),
                },
                "optional": {
                "annotation_stack": ("ANNOTATION_STACK",),
                "font_color_hex": ("STRING", {"multiline": False, "default": "#000000"}),
                }
    }

    RETURN_TYPES = ("ANNOTATION_STACK", "STRING", )
    RETURN_NAMES = ("ANNOTATION_STACK", "show_help", )
    FUNCTION = "add_annotation"
    CATEGORY = icons.get("Comfyroll/Graphics/Text")

    def add_annotation(self, image, 
                       font_name, font_size, font_color,
                       position_x, position_y, justify,
                       annotation_stack=None, font_color_hex='#000000'):
 
        show_help = "example help text"
 
        return (annotation_stack, show_help, )
        
#---------------------------------------------------------------------------------------------------------------------#
class CR_SimpleImageWatermark:
    
    @classmethod
    def INPUT_TYPES(cls):
    
        ALIGN_OPTIONS = ["center", "top left", "top center", "top right", "bottom left", "bottom center", "bottom right"]  

        return {"required": {
                "image": ("IMAGE",),
                "watermark_image": ("IMAGE",),
                "watermark_scale": ("FLOAT", {"default": 1, "min": 0.1, "max": 5.00, "step": 0.01}),
                "opacity": ("FLOAT", {"default": 0.30, "min": 0.00, "max": 1.00, "step": 0.01}),
                "align": (ALIGN_OPTIONS,),
                "x_margin": ("INT", {"default": 20, "min": -1024, "max": 1024}),
                "y_margin": ("INT", {"default": 20, "min": -1024, "max": 1024}),
            }
        }

    RETURN_TYPES = ("IMAGE", )
    FUNCTION = "overlay_image"
    CATEGORY = icons.get("Comfyroll/Graphics/Image")

    def overlay_image(self, image, watermark_image, watermark_scale, opacity, align, x_margin, y_margin):
    
        # Create PIL images for the background layer
        image = tensor2pil(image)
        watermark_image = tensor2pil(watermark_image)
        
        # Open images using Pillow
        image = image.convert("RGBA")
        watermark = watermark_image.convert("RGBA")

        # Resize watermark if needed
        watermark = watermark.resize(image.size)

        # Create a transparent layer for the watermark
        watermark_layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(watermark_layer)

        # Calculate the position to place the watermark based on the alignment
        if align == 'center':
            watermark_pos = ((image.width - watermark.width) // 2, (image.height - watermark.height) // 2)
        elif align == 'top left':
            watermark_pos = (x_margin, y_margin)
        elif align == 'top center':
            watermark_pos = ((image.width - watermark.width) // 2, y_margin)
        elif align == 'top right':
            watermark_pos = (image.width - watermark.width - x_margin, y_margin)
        elif align == 'bottom left':
            watermark_pos = (x_margin, image.height - watermark.height - y_margin)
        elif align == 'bottom center':
            watermark_pos = ((image.width - watermark.width) // 2, image.height - watermark.height - y_margin)
        elif align == 'bottom right':
            watermark_pos = (image.width - watermark.width - x_margin, image.height - watermark.height - y_margin)

        # Paste the watermark onto the transparent layer
        #watermark_layer.paste(watermark, watermark_pos, watermark)

        # Blend the images using the specified opacity
        #image = Image.alpha_composite(image, watermark_layer)
            
        # Adjust the opacity of the watermark layer if needed
        if opacity != 1:
            watermark_layer = reduce_opacity(watermark_layer, opacity)
        
        # Composite the text layer on top of the original image
        image_out = Image.composite(watermark_layer, image, watermark_layer)

        # Convert the PIL image back to a torch tensor
        return pil2tensor(image_out) 

#---------------------------------------------------------------------------------------------------------------------#
class CR_ComicPanelTemplatesAdvanced:

    @classmethod
    def INPUT_TYPES(s):
    
        directions = ["left to right", "right to left"]

        templates = ["custom",
                     "G22", "G33",
                     "H2", "H3",
                     "H12", "H13",
                     "H21", "H23",
                     "H31", "H32",
                     "V2", "V3",
                     "V12", "V13",
                     "V21", "V23",
                     "V31", "V32"]                           
        
        return {"required": {
                    "page_width": ("INT", {"default": 512, "min": 8, "max": 4096}),
                    "page_height": ("INT", {"default": 512, "min": 8, "max": 4096}),
                    "template": (templates,),
                    "reading_direction": (directions,),
                    "border_thickness": ("INT", {"default": 5, "min": 0, "max": 1024}),
                    "outline_thickness": ("INT", {"default": 2, "min": 0, "max": 1024}),
                    "outline_color": (COLORS,), 
                    "panel_color": (COLORS,),
                    "background_color": (COLORS,),
               },
                "optional": {
                    "images1": ("IMAGE",),
                    "images2": ("IMAGE",),
                    "images3": ("IMAGE",),
                    "images4": ("IMAGE",),
                    "custom_panel_layout": ("STRING", {"multiline": False, "default": "H123"}),
                    "outline_color_hex": ("STRING", {"multiline": False, "default": "#000000"}),
                    "panel_color_hex": ("STRING", {"multiline": False, "default": "#000000"}),
                    "bg_color_hex": ("STRING", {"multiline": False, "default": "#000000"}),
               }
    }

    RETURN_TYPES = ("IMAGE", "STRING", )
    RETURN_NAMES = ("image", "show_help", )
    FUNCTION = "layout"
    CATEGORY = icons.get("Comfyroll/Graphics/Template")
    
    def layout(self, page_width, page_height, template, reading_direction,
               border_thickness, outline_thickness, 
               outline_color, panel_color, background_color,
               images1=None, images2=None, images3=None, images4=None, custom_panel_layout='G44',
               outline_color_hex='#000000', panel_color_hex='#000000', bg_color_hex='#000000'):

        

        panels = []
        k = 0
        batches = 0
        
        # Convert tensor images to PIL
        if images1 is not None:
            images1 = [tensor2pil(image) for image in images1]
            len_images1 = len(images1)
            batches+=1
            
        if images2 is not None:
            images2 = [tensor2pil(image) for image in images2]
            len_images2 = len(images2)
            batches+=1
            
        if images3 is not None:
            images3 = [tensor2pil(image) for image in images3]
            len_images3 = len(images3)
            batches+=1
            
        if images4 is not None:
            images4 = [tensor2pil(image) for image in images4]
            len_images4 = len(images4)
            batches+=1

        # Get RGB values for the text and background colors    
        outline_color = get_color_values(outline_color, outline_color_hex, color_mapping)
        panel_color = get_color_values(panel_color, panel_color_hex, color_mapping)
        bg_color = get_color_values(background_color, bg_color_hex, color_mapping)                    

        # Create page and apply bg color
        size = (page_width - (2 * border_thickness), page_height - (2 * border_thickness))  
        page = Image.new('RGB', size, bg_color)
        draw = ImageDraw.Draw(page)
 
        if template == "custom":
            template = custom_panel_layout
        
        # Calculate panel positions and add to bg image
        first_char = template[0]
        if first_char == "G":
            rows = int(template[1])
            columns = int(template[2])
            panel_width = (page.width - (2 * columns * (border_thickness + outline_thickness))) // columns
            panel_height = (page.height  - (2 * rows * (border_thickness + outline_thickness))) // rows
            #Batch Loop
            #for b in range(batches):
            # Row loop
            for i in range(rows):
                # Column Loop
                for j in range(columns):
                    # Draw the panel
                    create_and_paste_panel(page, border_thickness, outline_thickness,
                                           panel_width, panel_height, page.width,
                                           panel_color, bg_color, outline_color,
                                           images1, i, j, k, len_images1, reading_direction)
                    k += 1

        elif first_char == "H":
            rows = len(template) - 1
            panel_height = (page.height  - (2 * rows * (border_thickness + outline_thickness))) // rows
            #Batch Loop
            #for b in range(batches):
            # Row loop
            for i in range(rows):
                columns = int(template[i+1])
                panel_width = (page.width - (2 * columns * (border_thickness + outline_thickness))) // columns
                # Column Loop
                for j in range(columns):
                    # Draw the panel
                    create_and_paste_panel(page, border_thickness, outline_thickness,
                                           panel_width, panel_height, page.width,
                                           panel_color, bg_color, outline_color,
                                           images1, i, j, k, len_images1, reading_direction)
                    k += 1
                    
        elif first_char == "V":
            columns = len(template) - 1
            panel_width = (page.width - (2 * columns * (border_thickness + outline_thickness))) // columns
            #Batch Loop
            #for b in range(batches):
            # Column Loop
            for j in range(columns):
                rows = int(template[j+1])
                panel_height = (page.height  - (2 * rows * (border_thickness + outline_thickness))) // rows
                # Row loop
                for i in range(rows):
                    # Draw the panel
                    create_and_paste_panel(page, border_thickness, outline_thickness,
                                           panel_width, panel_height, page.width,
                                           panel_color, bg_color, outline_color,
                                           images1, i, j, k, len_images1, reading_direction)
                    k += 1 
        
        # Add a border to the page
        if border_thickness > 0:
            page = ImageOps.expand(page, border_thickness, bg_color)
            
        show_help = "example help text"

        return (pil2tensor(page), show_help, )             
               
#---------------------------------------------------------------------------------------------------------------------#
# MAPPINGS
#---------------------------------------------------------------------------------------------------------------------#
# For reference only, actual mappings are in __init__.py
'''
NODE_CLASS_MAPPINGS = {
    "CR Multi-Panel Meme Template": CR_MultiPanelMemeTemplate,
    "CR Popular Meme Templates": CR_PopularMemeTemplates,
    "CR Draw Perspective Text": CR_DrawPerspectiveText,
    "CR Overlay Transparent Image":CR_OverlayTransparentImage,
    "CR Simple Annotations": CR_SimpleAnnotations,
    "CR Apply Annotations": CR_ApplyAnnotations,
    "CR Add Annotation": CR_AddAnnotation,
    "CR Simple Image Watermark": CR_SimpleImageWatermark,
    "CR Comic Panel Templates Advanced": CR_ComicPanelTemplatesAdvanced,    
}
'''

