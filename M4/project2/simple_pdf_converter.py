"""
Simple PDF Converter for BST Report Summary
===========================================

A more robust converter that handles the text format better.

Author: Van Robbins
Course: C310 - Data Structures and Algorithms
Module: M4 - Project 2
Date: June 22, 2025
"""

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import black, blue, gray, white
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
import re
import os


def create_pdf_styles():
    """Create custom styles for the PDF."""
    styles = getSampleStyleSheet()
    
    custom_styles = {
        'title': ParagraphStyle(
            'Title',
            parent=styles['Title'],
            fontSize=16,
            spaceAfter=20,
            alignment=TA_CENTER,
            textColor=blue,
            bold=True
        ),
        'heading': ParagraphStyle(
            'Heading',
            parent=styles['Heading1'],
            fontSize=13,
            spaceAfter=10,
            spaceBefore=15,
            textColor=black,
            bold=True
        ),
        'subheading': ParagraphStyle(
            'SubHeading',
            parent=styles['Heading2'],
            fontSize=11,
            spaceAfter=8,
            spaceBefore=10,
            textColor=black,
            bold=True
        ),
        'normal': ParagraphStyle(
            'Normal',
            parent=styles['Normal'],
            fontSize=9,
            spaceAfter=4,
            alignment=TA_LEFT,
            fontName='Helvetica'
        ),
        'bullet': ParagraphStyle(
            'Bullet',
            parent=styles['Normal'],
            fontSize=9,
            spaceAfter=3,
            leftIndent=20,
            fontName='Helvetica'
        ),
        'code': ParagraphStyle(
            'Code',
            fontSize=8,
            fontName='Courier',
            spaceAfter=3,
            leftIndent=15,
            textColor=black
        )
    }
    
    return custom_styles


def process_table_lines(lines):
    """Convert table lines to a reportlab Table."""
    if not lines:
        return None
    
    table_data = []
    for line in lines:
        line = line.strip()
        line = clean_text_for_pdf(line)  # Clean special characters
        if '|' in line and line.startswith('|') and line.endswith('|'):
            # Split by | and clean, removing empty first/last elements
            cells = [cell.strip() for cell in line.split('|')]
            cells = [clean_text_for_pdf(cell) for cell in cells if cell]  # Clean each cell
            
            # Skip separator lines (lines with only dashes)
            if cells and all(cell.replace('-', '').strip() == '' for cell in cells):
                continue  # Skip separator rows
            
            if cells:  # Only add non-empty rows
                table_data.append(cells)
    
    if not table_data or len(table_data) < 2:  # Need at least header + 1 row
        return None
    
    # Create table with auto column widths
    table = Table(table_data, hAlign='CENTER')
    
    # Style the table
    table.setStyle(TableStyle([
        # Header row styling
        ('BACKGROUND', (0, 0), (-1, 0), gray),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        
        # Data rows styling
        ('BACKGROUND', (0, 1), (-1, -1), white),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        
        # Grid and borders
        ('GRID', (0, 0), (-1, -1), 1, black),
        ('LINEBELOW', (0, 0), (-1, 0), 2, black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
    ]))
    
    return table


def clean_text_for_pdf(text):
    """Clean text to handle special characters for PDF generation."""
    # Handle mathematical notation
    text = text.replace('×', ' x ')  # Multiplication symbol
    text = text.replace('₂', '2')    # Subscript 2
    text = text.replace('₁', '1')    # Subscript 1  
    text = text.replace('₃', '3')    # Subscript 3
    text = text.replace('log₂(n)', 'log2(n)')  # Specific log2 notation
    text = text.replace('≈', '~')    # Approximately symbol
    text = text.replace('✓', 'OK')   # Check mark
    text = text.replace('❌', 'X')   # Cross mark
    
    # Handle other common special characters
    text = text.replace('"', '"').replace('"', '"')  # Smart quotes
    text = text.replace(''', "'").replace(''', "'")  # Smart apostrophes
    text = text.replace('—', '-').replace('–', '-')  # Em/en dashes
    
    return text


def convert_text_to_pdf(input_file, output_file):
    """Convert text file to formatted PDF."""
    print(f"Converting {input_file} to {output_file}...")
    
    # Create document
    doc = SimpleDocTemplate(
        output_file, 
        pagesize=letter,
        rightMargin=60, 
        leftMargin=60,
        topMargin=60, 
        bottomMargin=60
    )
    
    styles = create_pdf_styles()
    story = []
    
    # Read the file
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
      # Process lines
    i = 0
    table_lines = []
    
    while i < len(lines):
        line = lines[i].rstrip()
        
        # Clean the line for PDF compatibility
        line = clean_text_for_pdf(line)
        
        # Skip empty lines at the start
        if not line.strip() and not story:
            i += 1
            continue
          # Handle tables
        if '|' in line and line.strip().startswith('|') and line.strip().endswith('|'):
            table_lines.append(line)
            i += 1
            continue
        elif line.strip().startswith('|') and '|' in line:  # Alternative table format
            table_lines.append(line)
            i += 1
            continue
        else:
            # Process any accumulated table
            if table_lines:
                table = process_table_lines(table_lines)
                if table:
                    story.append(Spacer(1, 5))
                    story.append(table)
                    story.append(Spacer(1, 10))
                table_lines = []
        
        # Main title (first line)
        if i == 0 or (len(story) == 0 and 'BINARY SEARCH TREE' in line.upper()):
            story.append(Paragraph(line, styles['title']))
            story.append(Spacer(1, 15))
        
        # Section headers (lines with === under them)
        elif i + 1 < len(lines) and '=' * 10 in lines[i + 1]:
            story.append(Paragraph(line, styles['heading']))
            i += 1  # Skip the === line
        
        # Subsection headers (lines with --- under them)
        elif i + 1 < len(lines) and '-' * 10 in lines[i + 1]:
            story.append(Paragraph(line, styles['subheading']))
            i += 1  # Skip the --- line
        
        # Skip separator lines
        elif '=' * 10 in line or '-' * 10 in line:
            pass
        
        # Bullet points and lists
        elif line.strip().startswith(('✓', '-', '•')) or re.match(r'^\s*\d+\.', line):
            story.append(Paragraph(line, styles['bullet']))
        
        # Code-like lines (indented)
        elif line.startswith('   ') and line.strip():
            story.append(Paragraph(line, styles['code']))
        
        # Regular text
        elif line.strip():
            # Handle metadata lines
            if line.startswith(('Author:', 'Course:', 'Module:', 'Date:')):
                story.append(Paragraph(f"<b>{line}</b>", styles['normal']))
            else:
                story.append(Paragraph(line, styles['normal']))
        
        # Empty lines
        else:
            story.append(Spacer(1, 6))
        
        i += 1
    
    # Handle any remaining table
    if table_lines:
        table = process_table_lines(table_lines)
        if table:
            story.append(table)
    
    # Build PDF
    doc.build(story)
    print(f"✓ PDF created: {output_file}")


def main():
    """Main function."""
    input_file = "BST_Report_Summary.txt"
    output_file = "BST_Report_Summary.pdf"
    
    if not os.path.exists(input_file):
        print(f"❌ Error: {input_file} not found!")
        return
    
    try:
        convert_text_to_pdf(input_file, output_file)
        
        file_size = os.path.getsize(output_file)
        print(f"\n✅ SUCCESS!")
        print(f"📁 PDF Location: {os.path.abspath(output_file)}")
        print(f"📄 File Size: {file_size:,} bytes")
        
        # Try to open the PDF
        try:
            os.startfile(output_file)
            print(f"🔍 Opening PDF in default viewer...")
        except:
            print(f"💡 Open the PDF manually: {output_file}")
            
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
