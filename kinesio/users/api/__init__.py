from .for_medics import CurrentMedicDetailUpdateAPIView, RelatedPatientsOfMedicAPIView
from .for_patients import CurrentPatientDetailUpdateAPIView, MedicListAPIView
from .login import login
from .notifications import ChangeDeviceIDAPIView
from .register import register
from .secret_questions import SecretQuestionAPIView
from .user_exists import users_exists
from .continue_session import continue_session
from .sharing import share_sessions, unshare_sessions
