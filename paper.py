import sys, os
from os import path
from reportlab.lib.pagesizes import landscape, portrait
from reportlab.pdfgen import canvas


def generate_pdf_blank(width, height, background, dark, output_file):
    c = canvas.Canvas(output_file, pagesize=(width, height))

    # Apply background color
    c.setFillColor(background)
    c.rect(0, 0, width, height, fill=True, stroke=False)
    
    c.save()


def generate_pdf_grid(width, height, background, dark, output_file):
    line_spacing = int(16.5)
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


def generate_pdf_dot(width, height, background, dark, output_file):
    
    line_spacing = int(16.5)
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


def generate_pdf_batch(out_dir, size_name, width, height):
    
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
            action(width, height, color, dark, file_path)
            print(f"PDF file '{filename}' has been generated.")


def main():
    if len(sys.argv) < 2:
        print("Usage: python paper.py <paper_size>")
        print("Available paper sizes: A0, A1, A2, A3, A4, ALL")
        return

    paper_size = sys.argv[1].upper()

    if paper_size not in ['A0', 'A1', 'A2', 'A3', 'A4', 'ALL']:
        print("Invalid paper size. Available options: A0, A1, A2, A3, A4, ALL")
        return

    paper_sizes = {
        'A0': (3370.39, 2383.94),
        'A1': (2383.94, 1683.78),
        'A2': (1683.78, 1190.55),
        'A3': (1190.55, 841.89),
        'A4': (841.89, 595.28)
    }
    
    out_dir = path.join(path.curdir, "out")
    os.makedirs(out_dir, exist_ok=True)
    
    if paper_size == "ALL":
        for size_name, (width, height) in paper_sizes.items():
            generate_pdf_batch(out_dir, size_name, width, height)
    else:
        width, height = paper_sizes[paper_size]
        generate_pdf_batch(out_dir, paper_size, width, height)


if __name__ == '__main__':
    main()

