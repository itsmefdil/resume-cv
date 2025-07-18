# Resume Website

A modern, responsive resume website built with HTMX, Flask, and Tailwind CSS. The resume data is dynamically loaded from a YAML file, making it easy to update and maintain.

## Features

- **Modern Design**: Clean, professional layout using Tailwind CSS
- **Interactive Navigation**: HTMX-powered dynamic content loading without page refreshes
- **Responsive**: Mobile-first design that works on all devices
- **YAML-driven**: Easy to update resume data by editing the YAML file
- **Fast Loading**: Minimal JavaScript footprint with HTMX
- **Print-friendly**: Optimized for PDF generation and printing
- **Blog Feature**: Technical blog with categorized posts and modal views
- **PDF Download**: Generate and download resume as PDF using ReportLab

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTMX + Tailwind CSS
- **Data**: YAML for biodata storage
- **Styling**: Tailwind CSS with custom animations

## Project Structure

```
resume/
├── app.py                 # Flask application with blog routes
├── biodata.yaml          # Resume data including blog posts
├── requirements.txt       # Python dependencies
├── static/
│   └── style.css         # Custom CSS styles
└── templates/
    ├── index.html        # Main template
    ├── blog_list.html    # Blog listing page
    ├── blog_post.html    # Individual blog post page
    ├── pdf_resume.html   # PDF template
    └── partials/         # HTMX partial templates
        ├── personal_info.html
        ├── experience.html
        ├── skills.html
        ├── education.html
        ├── projects.html
        └── blog_posts.html
```

## Installation & Setup

1. **Clone or download the project**

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Customize your resume data**:
   Edit `biodata.yaml` with your personal information, experience, skills, education, and projects.

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Open in browser**:
   Navigate to `http://localhost:5000`

## Customization

### Updating Resume Data

Edit the `biodata.yaml` file to update your personal information:

```yaml
personal_info:
  name: "Your Name"
  title: "Your Job Title"
  email: "your.email@example.com"
  # ... other fields
```

### Styling

- Modify `static/style.css` for custom CSS
- Update Tailwind classes in templates for layout changes
- Customize colors in the gradient backgrounds

### Adding New Sections

1. Add new section data to `biodata.yaml`
2. Create a new partial template in `templates/partials/`
3. Add route handler in `app.py`
4. Add navigation button in main template

## Features Breakdown

### HTMX Integration

- Dynamic content loading without page refreshes
- Smooth animations and transitions
- Loading states and error handling

### Responsive Design

- Mobile-first approach
- Flexible grid layouts
- Touch-friendly navigation

### Performance

- Minimal JavaScript
- Fast server-side rendering
- Optimized assets

## Deployment

The application can be deployed to any platform that supports Flask:

- **Heroku**: Add `Procfile` with `web: python app.py`
- **PythonAnywhere**: Upload files and configure WSGI
- **DigitalOcean**: Use App Platform or Droplets
- **Vercel**: With appropriate configuration

## Browser Support

- Modern browsers (Chrome, Firefox, Safari, Edge)
- HTMX requires ES6 support
- Graceful degradation for older browsers

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to fork this project and submit pull requests for any improvements.
