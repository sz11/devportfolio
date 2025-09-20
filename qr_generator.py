import qrcode
from PIL import Image, ImageDraw
import requests
from io import BytesIO

def create_favicon_from_svg():
    """
    Create a favicon image from the SVG data used in your website
    """
    # Your favicon SVG as a simple colored circle with 'S'
    from PIL import Image, ImageDraw, ImageFont
    
    # Create a new image with gradient-like colors
    size = 200
    image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Create gradient effect by drawing multiple circles
    center = size // 2
    radius = size // 2 - 10
    
    # Gradient colors from your site (#667eea to #764ba2)
    start_color = (102, 126, 234)  # #667eea
    end_color = (118, 75, 162)     # #764ba2
    
    for i in range(radius):
        # Interpolate between start and end colors
        ratio = i / radius
        r = int(start_color[0] * (1 - ratio) + end_color[0] * ratio)
        g = int(start_color[1] * (1 - ratio) + end_color[1] * ratio)
        b = int(start_color[2] * (1 - ratio) + end_color[2] * ratio)
        
        draw.ellipse([center - radius + i, center - radius + i, 
                     center + radius - i, center + radius - i], 
                    fill=(r, g, b, 255))
    
    # Add the 'S' text
    try:
        # Try to use a nice font, fallback to default if not available
        font = ImageFont.truetype("arial.ttf", size=120)
    except:
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", size=120)
        except:
            font = ImageFont.load_default()
    
    # Get text size and position it in center
    bbox = draw.textbbox((0, 0), "S", font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    text_x = (size - text_width) // 2
    text_y = (size - text_height) // 2 - 10  # Adjust vertical position slightly

    # Make text bold and prominent
    draw.text((text_x, text_y), "S", fill=(255, 255, 255, 255), font=font)
    # Add text shadow for better visibility
    draw.text((text_x+2, text_y+2), "S", fill=(0, 0, 0, 100), font=font)
    draw.text((text_x, text_y), "S", fill=(255, 255, 255, 255), font=font)
    
    return image

def generate_custom_qr_code():
    """
    Generate a custom QR code with your portfolio URL and favicon logo
    """
    # Your portfolio URL
    url = "https://sz11.github.io/devportfolio/"
    
    # Create QR code with high error correction (allows for logo overlay)
    qr = qrcode.QRCode(
        version=1,  # Controls size (1 is smallest)
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction
        box_size=10,  # Size of each box in pixels
        border=4,  # Border size
    )
    
    qr.add_data(url)
    qr.make(fit=True)
    
    # Create QR code image with your brand colors
    qr_img = qr.make_image(
        fill_color="#1a1a1a",  # Dark color for QR pattern
        back_color="white"     # White background
    ).convert('RGB')
    
    # Create or load your favicon
    try:
        # If you have a favicon file, uncomment this line and provide the path
        # logo = Image.open("path/to/your/favicon.png")
        
        # For now, create the favicon programmatically
        logo = create_favicon_from_svg()
    except:
        # Fallback: create a simple logo
        logo = create_favicon_from_svg()
    
    # Calculate logo size (should be about 10-15% of QR code size)
    qr_width, qr_height = qr_img.size
    logo_size = min(qr_width, qr_height) // 6
    
    # Resize logo
    logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
    
    # Create a white background for the logo (helps with scanning)
    logo_bg_size = logo_size + 20
    logo_bg = Image.new('RGB', (logo_bg_size, logo_bg_size), 'white')
    
    # Paste logo onto white background
    logo_bg_pos = ((logo_bg_size - logo_size) // 2, (logo_bg_size - logo_size) // 2)
    logo_bg.paste(logo, logo_bg_pos, logo if logo.mode == 'RGBA' else None)
    
    # Calculate position to center the logo on QR code
    pos = ((qr_width - logo_bg_size) // 2, (qr_height - logo_bg_size) // 2)
    
    # Paste logo onto QR code
    qr_img.paste(logo_bg, pos)
    
    return qr_img

def create_branded_qr_versions():
    """
    Create multiple versions of the QR code for different use cases
    """
    base_qr = generate_custom_qr_code()
    
    # Version 1: Standard (for resume)
    standard_qr = base_qr.copy()
    standard_qr.save("portfolio_qr_standard.png", "PNG", dpi=(300, 300))
    
    # Version 2: Large (for presentations/posters)
    large_qr = base_qr.resize((800, 800), Image.Resampling.LANCZOS)
    large_qr.save("portfolio_qr_large.png", "PNG", dpi=(300, 300))
    
    # Version 3: Small (for business cards)
    small_qr = base_qr.resize((200, 200), Image.Resampling.LANCZOS)
    small_qr.save("portfolio_qr_small.png", "PNG", dpi=(300, 300))
    
    # Version 4: With text label
    create_qr_with_label(base_qr)
    
    print("✅ QR codes generated successfully!")
    print("📁 Files created:")
    print("   - portfolio_qr_standard.png (for resume)")
    print("   - portfolio_qr_large.png (for presentations)")
    print("   - portfolio_qr_small.png (for business cards)")
    print("   - portfolio_qr_with_label.png (with text)")

def create_qr_with_label(qr_img):
    """
    Create a QR code with text label below
    """
    from PIL import ImageFont
    
    # Create new image with space for text
    qr_width, qr_height = qr_img.size
    label_height = 60
    new_height = qr_height + label_height
    
    labeled_img = Image.new('RGB', (qr_width, new_height), 'white')
    labeled_img.paste(qr_img, (0, 0))
    
    # Add text
    draw = ImageDraw.Draw(labeled_img)
    
    try:
        font = ImageFont.truetype("arial.ttf", size=16)
        small_font = ImageFont.truetype("arial.ttf", size=12)
    except:
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Main text
    main_text = "Shuzheng Zheng | Software Developer"
    bbox = draw.textbbox((0, 0), main_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_x = (qr_width - text_width) // 2
    draw.text((text_x, qr_height + 10), main_text, fill="black", font=font)
    
    # URL text
    url_text = "sz11.github.io/devportfolio"
    bbox = draw.textbbox((0, 0), url_text, font=small_font)
    text_width = bbox[2] - bbox[0]
    text_x = (qr_width - text_width) // 2
    draw.text((text_x, qr_height + 35), url_text, fill="gray", font=small_font)
    
    labeled_img.save("portfolio_qr_with_label.png", "PNG", dpi=(300, 300))

if __name__ == "__main__":
    print("🎨 Generating custom QR codes for your portfolio...")
    print("🌐 URL: https://sz11.github.io/devportfolio/")
    print("🎯 Creating multiple versions...")
    
    try:
        create_branded_qr_versions()
        print("\n✨ All done! Your QR codes are ready for your resume and career fair!")
        print("\n💡 Recommendation: Use 'portfolio_qr_standard.png' on your resume")
        print("📱 Test the QR codes with your phone before printing!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💾 Make sure you have the required packages:")
        print("   pip install qrcode[pil] pillow")