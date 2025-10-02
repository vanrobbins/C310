"""
PDF Converter for BST Report Summary
====================================

This script converts the BST_Report_Summary.txt file to a well-formatted PDF document.

Author: Van Robbins
Course: C310 - Data Structures and Algorithms
Module: M4 - Project 2
Date: June 22, 2025
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import black, blue, gray, white
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.pdfgen import canvas
import os
import sys
from datetime import datetime


def create_custom_styles():
    """Create custom styles for the PDF document."""
    styles = getSampleStyleSheet()
    
    # Title style
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=18,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=blue
    )
    
    # Heading style
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading1'],
        fontSize=14,
        spaceAfter=12,
        spaceBefore=20,
        textColor=black,
        underline=True
    )
    
    # Subheading style
    subheading_style = ParagraphStyle(
        'CustomSubheading',
        parent=styles['Heading2'],
        fontSize=12,
        spaceAfter=8,
        spaceBefore=12,
        textColor=black,
        bold=True
    )
    
    # Normal text style
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6,
        alignment=TA_JUSTIFY
    )
    
    # Code style
    code_style = ParagraphStyle(
        'CustomCode',
        parent=styles['Code'],
        fontSize=9,
        fontName='Courier',
        spaceAfter=6,
        leftIndent=20
    )
    
    return {
        'title': title_style,
        'heading': heading_style,
        'subheading': subheading_style,
        'normal': normal_style,
        'code': code_style
    }


def parse_text_file(filename):
    """Parse the text file and extract content sections."""
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()
    
    sections = []
    current_section = {'title': '', 'content': []}
    
    lines = content.split('\n')
    
    for line in lines:
        line = line.rstrip()
        
        # Main title
        if '=' * 60 in line and not current_section['title']:
            continue
        elif line and '=' * 60 in lines[lines.index(line) + 1:lines.index(line) + 2] if lines.index(line) + 1 < len(lines) else False:
            if current_section['title']:
                sections.append(current_section)
            current_section = {'title': line, 'content': [], 'type': 'main_title'}
        elif line and '=' * 20 in lines[lines.index(line) + 1:lines.index(line) + 2] if lines.index(line) + 1 < len(lines) else False:
            if current_section['title']:
                sections.append(current_section)
            current_section = {'title': line, 'content': [], 'type': 'heading'}
        elif line and '-' * 20 in lines[lines.index(line) + 1:lines.index(line) + 2] if lines.index(line) + 1 < len(lines) else False:
            if current_section['title']:
                sections.append(current_section)
            current_section = {'title': line, 'content': [], 'type': 'subheading'}
        elif line.strip():
            current_section['content'].append(line)
    
    if current_section['title']:
        sections.append(current_section)
    
    return sections


def create_table_from_text(text_lines):
    """Create a table from text lines that contain pipe-separated values."""
    table_data = []
    
    for line in text_lines:
        if '|' in line and line.strip().startswith('|'):
            # Split by pipe and clean up
            row = [cell.strip() for cell in line.split('|')[1:-1]]  # Remove empty first/last elements
            table_data.append(row)
    
    if not table_data:
        return None
    
    # Create table with styling
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), gray),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), white),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 1, black)
    ]))
    
    return table


def convert_to_pdf(input_file, output_file):
    """Convert the text summary to a formatted PDF."""
    print(f"Converting {input_file} to {output_file}...")
    
    # Create PDF document
    doc = SimpleDocTemplate(output_file, pagesize=letter,
                          rightMargin=72, leftMargin=72,
                          topMargin=72, bottomMargin=18)
    
    # Get custom styles
    styles = create_custom_styles()
    
    # Story list to hold all content
    story = []
    
    # Read and parse the text file
    try:
        sections = parse_text_file(input_file)
    except Exception as e:
        print(f"Error reading file: {e}")
        # Fallback: read as simple text
        with open(input_file, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Create simple document
        story.append(Paragraph("BINARY SEARCH TREE IMPLEMENTATION AND ANALYSIS", styles['title']))
        story.append(Spacer(1, 12))
        
        for line in content.split('\n'):
            if line.strip():
                if '=' in line and len(line) > 20:
                    continue  # Skip separator lines
                elif line.isupper() and len(line.split()) <= 8:
                    story.append(Paragraph(line, styles['heading']))
                else:
                    story.append(Paragraph(line, styles['normal']))
            else:
                story.append(Spacer(1, 6))
        
        # Build PDF
        doc.build(story)
        print(f"✓ PDF created successfully: {output_file}")
        return
    
    # Add title
    story.append(Paragraph("BINARY SEARCH TREE IMPLEMENTATION AND ANALYSIS", styles['title']))
    story.append(Paragraph("Report Summary", styles['subheading']))
    story.append(Spacer(1, 12))
    
    # Add metadata
    story.append(Paragraph("Author: Van Robbins", styles['normal']))
    story.append(Paragraph("Course: C310 - Data Structures and Algorithms", styles['normal']))
    story.append(Paragraph("Module: M4 - Project 2", styles['normal']))
    story.append(Paragraph(f"Date: {datetime.now().strftime('%B %d, %Y')}", styles['normal']))
    story.append(Spacer(1, 20))
    
    # Process sections
    for section in sections:
        if section.get('type') == 'main_title':
            continue  # Skip, already handled
        elif section.get('type') == 'heading':
            story.append(Paragraph(section['title'], styles['heading']))
        elif section.get('type') == 'subheading':
            story.append(Paragraph(section['title'], styles['subheading']))
        else:
            story.append(Paragraph(section['title'], styles['heading']))
        
        # Process content
        table_lines = []
        for line in section['content']:
            if '|' in line and line.strip().startswith('|'):
                table_lines.append(line)
            else:
                # If we have accumulated table lines, create table first
                if table_lines:
                    table = create_table_from_text(table_lines)
                    if table:
                        story.append(table)
                        story.append(Spacer(1, 12))
                    table_lines = []
                
                # Add regular content
                if line.strip():
                    if line.startswith('   ✓') or line.startswith('   -'):
                        story.append(Paragraph(line, styles['code']))
                    elif line.startswith('✓') or line.strip().startswith('-'):
                        story.append(Paragraph(line, styles['normal']))
                    else:
                        story.append(Paragraph(line, styles['normal']))
                else:
                    story.append(Spacer(1, 6))
        
        # Handle any remaining table lines
        if table_lines:
            table = create_table_from_text(table_lines)
            if table:
                story.append(table)
        
        story.append(Spacer(1, 12))
    
    # Build the PDF
    doc.build(story)
    print(f"✓ PDF created successfully: {output_file}")


def main():
    """Main function to convert the summary to PDF."""
    input_file = "BST_Report_Summary.txt"
    output_file = "BST_Report_Summary.pdf"
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"❌ Error: {input_file} not found!")
        print("Make sure you're running this script in the project directory.")
        sys.exit(1)
    
    try:
        convert_to_pdf(input_file, output_file)
        print(f"\n✅ SUCCESS: PDF report generated!")
        print(f"📁 Location: {os.path.abspath(output_file)}")
        print(f"📄 File size: {os.path.getsize(output_file)} bytes")
        
    except Exception as e:
        print(f"❌ Error creating PDF: {e}")
        print("Make sure you have reportlab installed: pip install reportlab")
        sys.exit(1)


if __name__ == "__main__":
    main()
