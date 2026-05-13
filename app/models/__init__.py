# 1. Skill + link table first — depends on nothing
from app.models.skill import Skill, JobSkillLink

# 2. User — depends on nothing
from app.models.user import User, UserRole

# 3. Company — depends on User (foreign_key="users.id")
from app.models.company import Company

# 4. Job — depends on Company + Skill
from app.models.job import Job

# 5. Application — depends on User + Job
from app.models.application import Application, ApplicationStatus

# 6. Notification — depends on User
from app.models.notification import Notification