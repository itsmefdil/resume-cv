from flask import Flask, render_template, jsonify, make_response, url_for
import yaml
import os
import io
import frontmatter
import markdown
from datetime import datetime

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib import colors

    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    print("Warning: reportlab not available. PDF generation will be disabled.")

app = Flask(__name__)


def load_biodata():
    """Load biodata from YAML file"""
    with open("biodata.yaml", "r") as file:
        return yaml.safe_load(file)


def load_blog_posts():
    """Load blog posts from markdown files"""
    blog_posts = []
    blog_dir = "blog"

    if not os.path.exists(blog_dir):
        return []

    for filename in os.listdir(blog_dir):
        if filename.endswith(".md"):
            filepath = os.path.join(blog_dir, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                post = frontmatter.load(f)

                # Convert markdown content to HTML
                html_content = markdown.markdown(
                    post.content,
                    extensions=["codehilite", "fenced_code", "tables", "toc", "nl2br"],
                    extension_configs={
                        "codehilite": {
                            "css_class": "codehilite",
                            "use_pygments": True,
                            "noclasses": False,
                        }
                    },
                )

                # Create post data
                post_data = {
                    "title": post.metadata.get("title", "Untitled"),
                    "date": post.metadata.get("date", ""),
                    "category": post.metadata.get("category", "General"),
                    "summary": post.metadata.get("summary", ""),
                    "tags": post.metadata.get("tags", []),
                    "read_time": post.metadata.get("read_time", "5 min read"),
                    "content": html_content,
                    "filename": filename,
                }
                blog_posts.append(post_data)

    # Sort by date (newest first)
    blog_posts.sort(key=lambda x: x["date"], reverse=True)
    return blog_posts


def generate_pdf_with_reportlab(biodata):
    """Generate PDF using reportlab as fallback"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18,
    )

    # Get styles
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Heading1"],
        fontSize=24,
        spaceAfter=30,
        alignment=1,  # Center
        textColor=colors.HexColor("#1f2937"),
    )

    subtitle_style = ParagraphStyle(
        "CustomSubtitle",
        parent=styles["Heading2"],
        fontSize=16,
        spaceAfter=12,
        textColor=colors.HexColor("#3b82f6"),
    )

    heading_style = ParagraphStyle(
        "CustomHeading",
        parent=styles["Heading3"],
        fontSize=14,
        spaceAfter=12,
        textColor=colors.HexColor("#1f2937"),
    )

    # Story container
    story = []

    # Header
    story.append(Paragraph(biodata["personal_info"]["name"], title_style))
    story.append(Paragraph(biodata["personal_info"]["title"], subtitle_style))

    # Contact info
    contact_info = f"""
    {biodata['personal_info']['email']} • {biodata['personal_info']['phone']}<br/>
    {biodata['personal_info']['location']}<br/>
    {biodata['personal_info']['linkedin']} • {biodata['personal_info']['github']}
    """
    story.append(Paragraph(contact_info, styles["Normal"]))
    story.append(Spacer(1, 12))

    # Summary
    story.append(Paragraph("Professional Summary", heading_style))
    story.append(Paragraph(biodata["personal_info"]["summary"], styles["Normal"]))
    story.append(Spacer(1, 12))

    # Experience
    story.append(Paragraph("Work Experience", heading_style))
    for job in biodata["experience"]:
        job_title = f"<b>{job['position']}</b> at <b>{job['company']}</b>"
        story.append(Paragraph(job_title, styles["Normal"]))
        story.append(
            Paragraph(f"{job['duration']} • {job['location']}", styles["Normal"])
        )

        for responsibility in job["responsibilities"]:
            story.append(Paragraph(f"• {responsibility}", styles["Normal"]))
        story.append(Spacer(1, 6))

    story.append(Spacer(1, 12))

    # Skills
    story.append(Paragraph("Technical Skills", heading_style))
    skills_text = ", ".join(biodata["skills"]["technical"])
    story.append(Paragraph(skills_text, styles["Normal"]))
    story.append(Spacer(1, 12))

    # Education
    story.append(Paragraph("Education", heading_style))
    for edu in biodata["education"]:
        edu_text = f"<b>{edu['degree']}</b><br/>{edu['institution']} • {edu['year']}"
        if "gpa" in edu:
            edu_text += f" • GPA: {edu['gpa']}"
        story.append(Paragraph(edu_text, styles["Normal"]))

    story.append(Spacer(1, 12))

    # Projects
    story.append(Paragraph("Featured Projects", heading_style))
    for project in biodata["projects"]:
        project_title = f"<b>{project['name']}</b>"
        story.append(Paragraph(project_title, styles["Normal"]))
        story.append(Paragraph(project["description"], styles["Normal"]))

        tech_text = "Technologies: " + ", ".join(project["technologies"])
        story.append(Paragraph(tech_text, styles["Normal"]))
        story.append(Spacer(1, 6))

    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer


@app.route("/")
def index():
    """Main resume page"""
    biodata = load_biodata()
    blog_posts = load_blog_posts()[:2]  # Get only first 2 posts for preview
    return render_template("index.html", data=biodata, blog_posts=blog_posts)


@app.route("/api/section/<section_name>")
def get_section(section_name):
    """API endpoint to get specific sections for HTMX requests"""
    biodata = load_biodata()

    if section_name in biodata:
        return render_template(
            f"partials/{section_name}.html",
            data=biodata[section_name],
            full_data=biodata,
        )
    else:
        return jsonify({"error": "Section not found"}), 404


@app.route("/blog")
def blog_list():
    """Blog listing page"""
    biodata = load_biodata()
    blog_posts = load_blog_posts()
    return render_template("blog_list.html", posts=blog_posts, data=biodata)


@app.route("/api/blog")
def get_blog_section():
    """API endpoint to get blog section for HTMX"""
    biodata = load_biodata()
    blog_posts = load_blog_posts()
    return render_template(
        "partials/blog_posts.html", data=blog_posts, full_data=biodata
    )


@app.route("/api/blog/<filename>")
def get_blog_post_api(filename):
    """API endpoint to get individual blog post for HTMX"""
    biodata = load_biodata()
    blog_posts = load_blog_posts()

    # Find post by filename
    post = None
    for p in blog_posts:
        if p["filename"] == filename:
            post = p
            break

    if post:
        return render_template(
            "partials/blog_post_detail.html", post=post, data=biodata
        )
    else:
        return (
            "<div class='text-center p-8'><h2 class='text-2xl font-bold text-red-600'>Blog post not found</h2></div>",
            404,
        )


@app.route("/blog/<filename>")
def blog_post(filename):
    """Individual blog post page by filename"""
    biodata = load_biodata()
    blog_posts = load_blog_posts()

    # Find post by filename
    post = None
    for p in blog_posts:
        if p["filename"] == filename:
            post = p
            break

    if post:
        return render_template("blog_post.html", post=post, data=biodata)
    else:
        return "Blog post not found", 404


@app.route("/download")
def download_resume():
    """Download resume as PDF"""
    if not REPORTLAB_AVAILABLE:
        return (
            jsonify(
                {"error": "PDF generation not available. Please install reportlab."}
            ),
            500,
        )

    try:
        biodata = load_biodata()
        filename = f"{biodata['personal_info']['name'].replace(' ', '_')}_Resume.pdf"

        # Generate PDF using reportlab
        pdf_buffer = generate_pdf_with_reportlab(biodata)
        pdf_data = pdf_buffer.getvalue()

        # Create response
        response = make_response(pdf_data)
        response.headers["Content-Type"] = "application/pdf"
        response.headers["Content-Disposition"] = f'attachment; filename="{filename}"'

        return response

    except Exception as e:
        print(f"PDF generation error: {str(e)}")
        return jsonify({"error": f"Failed to generate PDF: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
