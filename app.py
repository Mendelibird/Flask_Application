# Import core components
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import (LoginManager, login_user, login_required,logout_user, current_user)
import os
from models import db, User, Opportunity, create_admin_if_not_exists

# Configure and initialise application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rad_portal.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Configure Flask Login
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id: str):
    return db.session.get(User, int(user_id))

# Database setup and admin user creation if required
with app.app_context():
    db.create_all()
    create_admin_if_not_exists()

# Public Routes
@app.route('/')
def index():
    return render_template('index.html', current_user=current_user)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = (request.form.get('name') or '').strip()
        email = (request.form.get('email') or '').strip().lower()
        password = request.form.get('password') or ''

        if not name or not email or not password:
            flash('All fields are required.', 'danger')
            return redirect(url_for('register'))

        if User.query.filter_by(email=email).first():
            flash('Email address already exists.', 'warning')
            return redirect(url_for('register'))

        if User.query.filter_by(name=name).first():
            flash('Username already taken.', 'warning')
            return redirect(url_for('register'))

        user = User(name=name, email=email)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = (request.form.get('email') or '').strip().lower()
        password = request.form.get('password') or ''

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            flash('Login successful.', 'success')
            return redirect(url_for('home'))

        flash('Login failed. Check your email and/or password.', 'danger')

    return render_template('login.html')

# Authenticated Routes
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/home')
@login_required
def home():
    opportunities = Opportunity.query.all()
    return render_template('home.html', opportunities=opportunities)


@app.route('/home/create', methods=['GET', 'POST'])
@login_required
def create_opportunity():
    if request.method == 'POST':
        title = (request.form.get('title') or '').strip()
        description = (request.form.get('description') or '').strip()
        business_unit = (request.form.get('business_unit') or '').strip()
        predicted_benefits = (request.form.get('predicted_benefits') or '').strip()
        business_criticality = (request.form.get('business_criticality') or '').strip()

        if not title or not description or not business_unit or not predicted_benefits or not business_criticality:
            flash('All fields are required.', 'danger')
            return redirect(url_for('create_opportunity'))

        existing = Opportunity.query.filter_by(title=title).first()
        if existing:
            flash("An opportunity with this title already exists. Please choose a different title.", "danger")
            return redirect(url_for('create_opportunity'))

        opp = Opportunity(
            title=title,
            description=description,
            business_unit=business_unit,
            predicted_benefits=predicted_benefits,
            business_criticality=business_criticality,
            submitted_by=current_user.user_id
        )
        db.session.add(opp)
        db.session.commit()

        flash('Opportunity created successfully.', 'success')
        return redirect(url_for('home'))

    return render_template('create_opportunity.html')

@app.route('/home/edit/<int:opportunity_id>', methods=['GET', 'POST'])
@login_required
def edit_opportunity(opportunity_id: int):
    opportunity = Opportunity.query.get(opportunity_id)

    if opportunity is None:
        return 'Opportunity not found.', 404

    is_admin = (current_user.role == 'admin')
    is_owner = (opportunity.submitted_by == current_user.user_id)

    if not (is_admin or is_owner):
        flash("You are not authorised to edit this opportunity.", "danger")
        return redirect(url_for('home'))

    if request.method == 'POST':
        title = (request.form.get('title') or '').strip()
        description = (request.form.get('description') or '').strip()
        business_unit = (request.form.get('business_unit') or '').strip()
        predicted_benefits = (request.form.get('predicted_benefits') or '').strip()
        business_criticality = (request.form.get('business_criticality') or '').strip()

        status = (request.form.get('status') or '').strip()
        value_score = (request.form.get('value_score') or '').strip()
        effort_score = (request.form.get('effort_score') or '').strip()

        errors = []
        if not title:
            errors.append("Title is required.")
        if not description:
            errors.append("Description is required.")
        if not business_unit:
            errors.append("Business Unit is required.")
        if not predicted_benefits:
            errors.append("Predicted benefits are required.")
        if not business_criticality:
            errors.append("Business criticality is required.")

        existing = Opportunity.query.filter(
            Opportunity.title == title,
            Opportunity.opportunity_id != opportunity_id
        ).first()
        if existing:
            flash("An opportunity with this title already exists. Please choose a different title.", "danger")
            return redirect(url_for('edit_opportunity', opportunity_id=opportunity_id))

        if is_admin:
            if status:
                opportunity.status = status

            if value_score:
                try:
                    v = int(value_score)
                    if 1 <= v <= 100:
                        opportunity.value_score = v
                    else:
                        errors.append("Value score must be between 1 and 100.")
                except ValueError:
                    errors.append("Value score must be an integer.")

            if effort_score:
                try:
                    e = int(effort_score)
                    if 1 <= e <= 100:
                        opportunity.effort_score = e
                    else:
                        errors.append("Effort score must be between 1 and 100.")
                except ValueError:
                    errors.append("Effort score must be an integer.")

        if errors:
            for e in errors:
                flash(e, 'danger')
            return render_template('edit_opportunity.html', opportunity=opportunity)

        opportunity.title = title
        opportunity.description = description
        opportunity.business_unit = business_unit
        opportunity.predicted_benefits = predicted_benefits
        opportunity.business_criticality = business_criticality

        db.session.commit()
        flash("Opportunity updated successfully.", "success")
        return redirect(url_for('home'))

    return render_template('edit_opportunity.html', opportunity=opportunity)

@app.route('/home/delete/<int:opportunity_id>', methods=['POST'])
@login_required
def delete_opportunity(opportunity_id):
    """Delete an opportunity (admin only)."""
    if current_user.role != 'admin':
        flash('You are not authorised to delete opportunities.', 'danger')
        return redirect(url_for('home'))

    opp = Opportunity.query.get_or_404(opportunity_id)

    try:
        db.session.delete(opp)
        db.session.commit()
        flash('Opportunity deleted successfully.', 'success')
    except Exception:
        db.session.rollback()
        flash('An error occurred while deleting the opportunity.', 'danger')

    return redirect(url_for('home'))

# Application entry point
if __name__ == '__main__':

    app.run(debug=True)
