from flask import Blueprint, request, jsonify, session
from extensions import db
from models import Opportunity

opp_bp = Blueprint('opportunities', __name__)


def get_current_admin_id():
    return session.get('admin_id')


def require_login():
    if not get_current_admin_id():
        return jsonify({'error': 'Authentication required.'}), 401
    return None


# US-2.1 View all opportunities
@opp_bp.route('/', methods=['GET'])
def get_opportunities():
    err = require_login()
    if err:
        return err
    admin_id = get_current_admin_id()
    opps = Opportunity.query.filter_by(admin_id=admin_id).order_by(Opportunity.created_at.desc()).all()
    return jsonify([o.to_dict() for o in opps]), 200


# US-2.2 Add new opportunity
@opp_bp.route('/', methods=['POST'])
def create_opportunity():
    err = require_login()
    if err:
        return err

    data = request.get_json()
    admin_id = get_current_admin_id()

    name = (data.get('name') or '').strip()
    duration = (data.get('duration') or '').strip()
    start_date = (data.get('start_date') or '').strip()
    description = (data.get('description') or '').strip()
    skills_raw = (data.get('skills') or '').strip()
    category = (data.get('category') or '').strip()
    future_opportunities = (data.get('future_opportunities') or '').strip()
    max_applicants = data.get('max_applicants')

    missing = []
    if not name:                 missing.append('Opportunity Name')
    if not duration:             missing.append('Duration')
    if not start_date:           missing.append('Start Date')
    if not description:          missing.append('Description')
    if not skills_raw:           missing.append('Skills to Gain')
    if not category:             missing.append('Category')
    if not future_opportunities: missing.append('Future Opportunities')

    if missing:
        return jsonify({'error': f"Required fields missing: {', '.join(missing)}."}), 400

    max_app_int = None
    if max_applicants not in (None, ''):
        try:
            max_app_int = int(max_applicants)
        except (ValueError, TypeError):
            return jsonify({'error': 'Maximum Applicants must be a number.'}), 400

    opp = Opportunity(
        admin_id=admin_id,
        name=name,
        duration=duration,
        start_date=start_date,
        description=description,
        skills=skills_raw,
        category=category,
        future_opportunities=future_opportunities,
        max_applicants=max_app_int
    )
    db.session.add(opp)
    db.session.commit()
    return jsonify(opp.to_dict()), 201


# US-2.4 View opportunity details
@opp_bp.route('/<int:opp_id>', methods=['GET'])
def get_opportunity(opp_id):
    err = require_login()
    if err:
        return err
    admin_id = get_current_admin_id()
    opp = Opportunity.query.filter_by(id=opp_id, admin_id=admin_id).first()
    if not opp:
        return jsonify({'error': 'Opportunity not found.'}), 404
    return jsonify(opp.to_dict()), 200


# US-2.5 Edit an opportunity
@opp_bp.route('/<int:opp_id>', methods=['PUT'])
def update_opportunity(opp_id):
    err = require_login()
    if err:
        return err
    admin_id = get_current_admin_id()
    opp = Opportunity.query.filter_by(id=opp_id, admin_id=admin_id).first()
    if not opp:
        return jsonify({'error': 'Opportunity not found.'}), 404

    data = request.get_json()

    name = (data.get('name') or '').strip()
    duration = (data.get('duration') or '').strip()
    start_date = (data.get('start_date') or '').strip()
    description = (data.get('description') or '').strip()
    skills_raw = (data.get('skills') or '').strip()
    category = (data.get('category') or '').strip()
    future_opportunities = (data.get('future_opportunities') or '').strip()
    max_applicants = data.get('max_applicants')

    missing = []
    if not name:                 missing.append('Opportunity Name')
    if not duration:             missing.append('Duration')
    if not start_date:           missing.append('Start Date')
    if not description:          missing.append('Description')
    if not skills_raw:           missing.append('Skills to Gain')
    if not category:             missing.append('Category')
    if not future_opportunities: missing.append('Future Opportunities')

    if missing:
        return jsonify({'error': f"Required fields missing: {', '.join(missing)}."}), 400

    max_app_int = None
    if max_applicants not in (None, ''):
        try:
            max_app_int = int(max_applicants)
        except (ValueError, TypeError):
            return jsonify({'error': 'Maximum Applicants must be a number.'}), 400

    opp.name = name
    opp.duration = duration
    opp.start_date = start_date
    opp.description = description
    opp.skills = skills_raw
    opp.category = category
    opp.future_opportunities = future_opportunities
    opp.max_applicants = max_app_int
    db.session.commit()
    return jsonify(opp.to_dict()), 200


# US-2.6 Delete an opportunity
@opp_bp.route('/<int:opp_id>', methods=['DELETE'])
def delete_opportunity(opp_id):
    err = require_login()
    if err:
        return err
    admin_id = get_current_admin_id()
    opp = Opportunity.query.filter_by(id=opp_id, admin_id=admin_id).first()
    if not opp:
        return jsonify({'error': 'Opportunity not found.'}), 404
    db.session.delete(opp)
    db.session.commit()
    return jsonify({'message': 'Opportunity deleted successfully.'}), 200