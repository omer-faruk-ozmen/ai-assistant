from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

from models.user import User
from models.patient import Patient
from models.diagnosis import Diagnosis
from models.examination import Examination
from models.intervention import Intervention
from models.conclusion import Conclusion
