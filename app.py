from flask import Flask, render_template, request, redirect, url_for
import base64
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Needed for security
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2MB max file size

# In-memory storage for lesson plans (for MVP only)
lesson_plans = []

# Allowed file extensions for diagrams
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'svg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_uploaded_file(file_field):
    """Process uploaded file and return base64 encoded string"""
    print(f"Processing file field: {file_field}")  # Debug print

    if file_field not in request.files:
        print(f"File field {file_field} not in request.files")  # Debug print
        return None

    file = request.files.get(file_field)
    print(f"File object: {file}")  # Debug print
    print(f"File filename: {file.filename}")  # Debug print

    if file and file.filename and allowed_file(file.filename):
        print(f"File is valid, processing...")  # Debug print

        # Read file and encode as base64
        file_data = file.read()
        encoded_file = base64.b64encode(file_data).decode('utf-8')
        mime_type = file.content_type
        result = f"data:{mime_type};base64,{encoded_file}"
        print(f"Successfully processed file, result length: {len(result)}")  # Debug print
        return result
    else:
        print(f"File is invalid or not allowed")  # Debug print
        if file and file.filename:
            print(f"File extension: {file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else 'none'}")  # Debug print

    return None

@app.context_processor
def inject_feedback_data():
    """Make current URL available to all templates for feedback links"""
    return dict(current_url=request.url)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create', methods=['GET'])
def create_plan_form():
    return render_template('create_plan.html')

@app.route('/create', methods=['POST'])
def create_plan():
    print("Create plan route called")  # Debug print
    print(f"Request method: {request.method}")  # Debug print
    print(f"Request form: {request.form}")  # Debug print
    print(f"Request files: {request.files}")  # Debug print

    # Extract form data
    teacher_name = request.form.get('teacher_name')
    pesh_year = request.form.get('pesh_year')
    date = request.form.get('date')
    class_duration = request.form.get('class_duration')
    start_time = request.form.get('start_time')
    end_time = request.form.get('end_time')
    school_name = request.form.get('school_name')
    year = request.form.get('year')
    class_id = request.form.get('class_id')
    class_level = request.form.get('class_level')
    class_size = request.form.get('class_size')
    boys = request.form.get('boys')
    girls = request.form.get('girls')
    topic = request.form.get('topic')
    unit_duration = request.form.get('unit_duration')
    day_of_unit = request.form.get('day_of_unit')
    lesson_theme = request.form.get('lesson_theme')
    ability_level = request.form.get('ability_level')
    psychomotor_objs = request.form.get('psychomotor_objs')
    cognitive_objs = request.form.get('cognitive_objs')
    affective_objs = request.form.get('affective_objs')
    venue = request.form.get('venue')
    equipment = request.form.get('equipment')
    safety_concerns = request.form.get('safety_concerns')
    
    # Lesson section times and details
    intro_time = request.form.get('intro_time')
    intro_cues = request.form.get('intro_cues')
    intro_equipment = request.form.get('intro_equipment')
    
    sd_time = request.form.get('sd_time')
    sd_cues = request.form.get('sd_cues')
    sd_equipment = request.form.get('sd_equipment')
    
    appli_time = request.form.get('appli_time')
    appli_cues = request.form.get('appli_cues')
    appli_equipment = request.form.get('appli_equipment')
    
    ca_time = request.form.get('ca_time')
    ca_cues = request.form.get('ca_cues')
    ca_equipment = request.form.get('ca_equipment')
    
    followup_actions = request.form.get('followup_actions')
    self_reflection = request.form.get('self_reflection')
    
    # Process uploaded diagram files
    print("Processing uploaded files...")  # Debug print

    intro_diagram = process_uploaded_file('intro_file')
    sd_diagram = process_uploaded_file('sd_file')
    appli_diagram = process_uploaded_file('appli_file')
    ca_diagram = process_uploaded_file('ca_file')

    print(f"Intro diagram processed: {intro_diagram is not None}")  # Debug print
    print(f"SD diagram processed: {sd_diagram is not None}")  # Debug print
    print(f"Appli diagram processed: {appli_diagram is not None}")  # Debug print
    print(f"CA diagram processed: {ca_diagram is not None}")  # Debug print
    
    # Create new plan with all fields
    new_plan = {
        'id': len(lesson_plans) + 1,
        'teacher_name': teacher_name,
        'pesh_year': pesh_year,
        'date': date,
        'class_duration': class_duration,
        'start_time': start_time,
        'end_time': end_time,
        'school_name': school_name,
        'year': year,
        'class_id': class_id,
        'class_level': class_level,
        'class_size': class_size,
        'boys': boys,
        'girls': girls,
        'topic': topic,
        'unit_duration': unit_duration,
        'day_of_unit': day_of_unit,
        'lesson_theme': lesson_theme,
        'ability_level': ability_level,
        'psychomotor_objs': psychomotor_objs,
        'cognitive_objs': cognitive_objs,
        'affective_objs': affective_objs,
        'venue': venue,
        'equipment': equipment,
        'safety_concerns': safety_concerns,
        'intro_time': intro_time,
        'intro_cues': intro_cues,
        'intro_equipment': intro_equipment,
        'intro_diagram': intro_diagram,
        'sd_time': sd_time,
        'sd_cues': sd_cues,
        'sd_equipment': sd_equipment,
        'sd_diagram': sd_diagram,
        'appli_time': appli_time,
        'appli_cues': appli_cues,
        'appli_equipment': appli_equipment,
        'appli_diagram': appli_diagram,
        'ca_time': ca_time,
        'ca_cues': ca_cues,
        'ca_equipment': ca_equipment,
        'ca_diagram': ca_diagram,
        'followup_actions': followup_actions,
        'self_reflection': self_reflection
    }
    
    # Store the plan
    lesson_plans.append(new_plan)
    
    # Redirect to view the plan
    return redirect(url_for('view_plan', plan_id=new_plan['id']))

@app.route('/plan/<int:plan_id>')
def view_plan(plan_id):
    # Find the plan with the matching ID
    plan = next((p for p in lesson_plans if p['id'] == plan_id), None)
    if plan is None:
        return "Plan not found!", 404

    print(f"Viewing plan {plan_id}")  # Debug print
    print(f"Intro diagram exists: {plan.get('intro_diagram') is not None}")  # Debug print
    print(f"SD diagram exists: {plan.get('sd_diagram') is not None}")  # Debug print
    print(f"Appli diagram exists: {plan.get('appli_diagram') is not None}")  # Debug print
    print(f"CA diagram exists: {plan.get('ca_diagram') is not None}")  # Debug print
    
    return render_template('view_plan.html', plan=plan)

if __name__ == '__main__':
    app.run(debug=True)