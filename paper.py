import sys, os
from os import path
from reportlab.lib.pagesizes import landscape, portrait
from reportlab.pdfgen import canvas
from enum import Enum
import argparse


class IPadModel(Enum):
    IPAD_PRO_2021 = "ipad_pro" # iPad Pro (12.9-inch, 2021)
    IPAD_AIR_2020 = "ipad_air" # iPad Air (2020)

ipad_models = {
    IPadModel.IPAD_PRO_2021: {"resolution": (2732, 2048), "ppi": 264, "scale": 2},
    IPadModel.IPAD_AIR_2020: {"resolution": (2360, 1640), "ppi": 264, "scale": 2}
}

paper_inch_sizes = {
    "a0": (33.11, 46.81),
    "a1": (23.39, 33.11),
    "a2": (16.54, 23.39),
    "a3": (11.69, 16.54),
    "a4": (8.27, 11.69),
    "a5": (5.8, 8.3),
    "a6": (4.1, 5.8)
}

def get_paper_dimensions(ipad_model, paper_size):

    if ipad_model not in ipad_models:
        raise ValueError("Invalid iPad model")

    if paper_size not in paper_inch_sizes.keys():
        raise ValueError("Invalid paper size")

    model_info = ipad_models[ipad_model]
    resolution = model_info["resolution"]
    ppi = model_info["ppi"]
    scale_factor = model_info["scale"]

    paper_width, paper_height = paper_inch_sizes[paper_size]
    pixel_width = round(paper_width * ppi / scale_factor)
    pixel_height = round(paper_height * ppi / scale_factor)

    return pixel_width, pixel_height


def mm_to_inch(mm):
    inch = mm / 25.4
    return inch


def get_block_width(ipad_model):
    if ipad_model not in ipad_models:
        raise ValueError("Invalid iPad model")
    
    model_info = ipad_models[ipad_model]
    ppi = model_info["ppi"]
    scale_factor = model_info["scale"]

    return round(mm_to_inch(5) * ppi / scale_factor)


def generate_pdf_blank(width, height, block_width, background, dark, output_file):
    c = canvas.Canvas(output_file, pagesize=(width, height))

    # Apply background color
    c.setFillColor(background)
    c.rect(0, 0, width, height, fill=True, stroke=False)
    
    c.save()


def generate_pdf_grid(width, height, block_width, background, dark, output_file):
    line_spacing = int(block_width)
    thicker_line_spacing = 10 * line_spacing

    c = canvas.Canvas(output_file, pagesize=(width, height))

    # Apply background color
    c.setFillColor(background)
    c.rect(0, 0, width, height, fill=True, stroke=False)

    # Determine line colors and widths based on dark mode
    normal_line_color = "#58595B" if dark else "rgba(0, 0, 0, 0.1)"
    thicker_line_color = "#8C8E91" if dark else "rgba(0, 0, 0, 0.2)"
    line_width = 0.54 if dark else 1

    # Generate horizontal lines
    for y in range(int(height) - line_spacing, line_spacing, -line_spacing):
        # Determine if the current line is a thicker line
        if (int(height) - y) % thicker_line_spacing == 0:
            c.setStrokeColor(thicker_line_color)
            c.setLineWidth(line_width)
        else:
            c.setStrokeColor(normal_line_color)
            c.setLineWidth(line_width)
        c.line(0, y, width, y)

    # Generate vertical lines
    for x in range(line_spacing, int(width), line_spacing):
        # Determine if the current line is a thicker line
        if x % thicker_line_spacing == 0:
            c.setStrokeColor(thicker_line_color)
            c.setLineWidth(line_width)
        else:
            c.setStrokeColor(normal_line_color)
            c.setLineWidth(line_width)
        c.line(x, 0, x, height)

    c.save()


def generate_pdf_dot(width, height, block_width, background, dark, output_file):
    
    line_spacing = int(block_width)
    thicker_line_spacing = 10 * line_spacing

    c = canvas.Canvas(output_file, pagesize=(width, height))

    # Apply background color
    c.setFillColor(background)
    c.rect(0, 0, width, height, fill=True, stroke=False)
    
    normal_dot_size = 1.09
    thicker_dot_size = 2.18

    # Determine dot colors and transparency based on dark mode
    normal_dot_color = "#6D6E70" if dark else "#000000"
    thicker_dot_color = "96989B" if dark else "#000000"
    
    normal_dot_transparency = 1 if dark else 0.3
    thicker_dot_transparency = 1 if dark else 0.5

    # Generate dots at the intersections
    for y in range(int(height) - line_spacing, line_spacing, -line_spacing):
        for x in range(line_spacing, int(width), line_spacing):
            # Determine if the current dot is a thicker dot
            if (int(height) - y) % thicker_line_spacing == 0 and x % thicker_line_spacing == 0:
                dot_size = thicker_dot_size
                dot_color = thicker_dot_color
                dot_transparency = thicker_dot_transparency
            else:
                dot_size = normal_dot_size
                dot_color = normal_dot_color
                dot_transparency = normal_dot_transparency
            
            c.setFillColorRGB(*hex_to_rgb(dot_color), alpha=dot_transparency)
            c.ellipse(x - dot_size / 2, y - dot_size / 2, x + dot_size / 2, y + dot_size / 2, fill=True, stroke=False)

    c.save()
    
    
def hex_to_rgb(hex_value):
    hex_value = hex_value.lstrip("#")
    rgb_tuple = tuple(int(hex_value[i:i+2], 16) for i in (0, 2, 4))
    return tuple(comp / 255 for comp in rgb_tuple)


def generate_pdf_batch(out_dir, size_name, width, height, block_width):
    
    size_dir = os.path.join(out_dir, size_name)
    os.makedirs(size_dir, exist_ok=True)
    
    patterns = [
        ("BLANK", generate_pdf_blank),
        ("GRID", generate_pdf_grid),
        ("DOT", generate_pdf_dot)
    ]
    
    configs = [
        ("YELLOW", "#F7F6E8", False),
        ("WHITE", "#FFFFFF", False),
        ("BLACK", "#333333", True)
    ]
    
    for (pattern, action) in patterns:
        for (color_code, color, dark) in configs:
            filename = f"{size_name} {color_code} {pattern}.pdf"
            file_path = os.path.join(size_dir, filename)
            action(width, height, block_width, color, dark, file_path)
            print(f"PDF file '{filename}' has been generated.")


def main():
    parser = argparse.ArgumentParser(description="Generate PDFs for paper sizes on an iPad.")
    parser.add_argument("paper_size", choices=["all"] + list(paper_inch_sizes.keys()), help="Paper size")
    parser.add_argument("--model", choices=[m.value for m in IPadModel], default=IPadModel.IPAD_PRO_2021.value,
                        help="iPad model")
    parser.add_argument("--direction", choices=["landscape", "portrait"], default="landscape",
                        help="Paper direction")

    args = parser.parse_args()

    paper_size = args.paper_size
    ipad_model = IPadModel(args.model)
    direction = args.direction.lower()

    out_dir = path.join(path.curdir, "out")
    os.makedirs(out_dir, exist_ok=True)

    if paper_size == "all":
        paper_sizes_to_process = list(paper_inch_sizes.keys())
    else:
        paper_sizes_to_process = [paper_size]

    for name in paper_sizes_to_process:
        width, height = get_paper_dimensions(ipad_model, name)
        if direction == "landscape":
            width, height = height, width  # Swap width and height for landscape orientation
        block_width = get_block_width(ipad_model)

        generate_pdf_batch(out_dir, name.upper(), width, height, block_width)



if __name__ == '__main__':
    main()

