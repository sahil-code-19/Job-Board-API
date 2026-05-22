"""
seed.py  —  Dummy data seeder for Job Board API
Run from project root:
    python seed.py

Requires:  asyncpg  (already in your venv via asyncpg dependency)
DB config is read from app/.env  (DATABASE_URL)
"""

import asyncio
import asyncpg
import sys
from pathlib import Path

# Add current directory to sys.path to allow importing from 'app'
sys.path.append(str(Path(__file__).parent))
from app.core.security import pwd_hasher

# ── read DATABASE_URL from app/.env ────────────────────────────────────────
env_path = Path(__file__).parent / "app" / ".env"
DATABASE_URL = None
for line in env_path.read_text().splitlines():
    if line.startswith("DATABASE_URL"):
        DATABASE_URL = line.split("=", 1)[1].strip()
        break

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not found in app/.env")

# asyncpg uses plain postgresql:// (strip the +asyncpg driver part)
DSN = DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")


# ── pwdlib hash of "Password@123" ─────────────────────────────────────────
HASHED_PW = pwd_hasher.hash("Password@123")


async def seed(conn: asyncpg.Connection):
    print("[*] Starting seed...")

    # ── 1. USERS ──────────────────────────────────────────────────────────
    print("  -> users")
    users = [
        ("admin@jobboard.io",  "admin_user",    HASHED_PW, "admin",     True),
        ("alice@example.com",  "alice_dev",     HASHED_PW, "candidate", True),
        ("bob@example.com",    "bob_designer",  HASHED_PW, "candidate", True),
        ("carol@example.com",  "carol_pm",      HASHED_PW, "candidate", True),
        ("dave@startup.io",    "dave_employer", HASHED_PW, "employer",  True),
        ("eve@techcorp.com",   "eve_employer",  HASHED_PW, "employer",  True),
        ("frank@bigco.com",    "frank_hr",      HASHED_PW, "employer",  True),
        ("grace@example.com",  "grace_data",    HASHED_PW, "candidate", False),
        ("henry@example.com",  "henry_backend", HASHED_PW, "candidate", True),
        ("irene@ventures.com", "irene_cto",     HASHED_PW, "employer",  True),
    ]
    await conn.executemany(
        """
        INSERT INTO users (email, username, hashed_password, role, is_active, created_at)
        VALUES ($1, $2, $3, $4, $5, NOW())
        ON CONFLICT (email) DO NOTHING
        """,
        users,
    )

    # helper to fetch user id by username
    async def uid(username: str) -> int:
        return await conn.fetchval(
            "SELECT id FROM users WHERE username = $1", username
        )

    # ── 2. COMPANIES ──────────────────────────────────────────────────────
    print("  -> companies")
    companies = [
        ("Startup.io",
         "A fast-growing startup building the future of remote collaboration.",
         "https://startup.io",     await uid("dave_employer")),
        ("TechCorp Ltd.",
         "Enterprise software solutions for Fortune 500 companies.",
         "https://techcorp.com",   await uid("eve_employer")),
        ("BigCo Inc.",
         "A multinational corporation with teams across 40+ countries.",
         "https://bigco.com",      await uid("frank_hr")),
        ("Ventures Labs",
         "Deep-tech research lab focused on AI and robotics.",
         "https://ventureslabs.io", await uid("irene_cto")),
    ]
    await conn.executemany(
        """
        INSERT INTO companies (name, description, website, owner_id, created_at)
        VALUES ($1, $2, $3, $4, NOW())
        ON CONFLICT (name) DO NOTHING
        """,
        companies,
    )

    async def cid(name: str) -> int:
        return await conn.fetchval(
            "SELECT id FROM companies WHERE name = $1", name
        )

    # ── 3. SKILLS ─────────────────────────────────────────────────────────
    print("  -> skills")
    skill_names = [
        "Python", "FastAPI", "PostgreSQL", "Docker", "React",
        "TypeScript", "Machine Learning", "Figma", "Project Management",
        "AWS", "Go", "Kubernetes",
    ]
    await conn.executemany(
        "INSERT INTO skills (name) VALUES ($1) ON CONFLICT (name) DO NOTHING",
        [(s,) for s in skill_names],
    )

    async def sid(name: str) -> int:
        return await conn.fetchval(
            "SELECT id FROM skills WHERE name = $1", name
        )

    # ── 4. JOBS ───────────────────────────────────────────────────────────
    print("  -> jobs")
    jobs_data = [
        # (title, desc, salary, type, category, location, company_name, co_website, co_desc, views, applicants)
        ("Backend Python Developer",
         "Build scalable REST APIs using FastAPI and PostgreSQL.",
         "$80,000 – $110,000", "Full-time", "Engineering", "Remote",
         "Startup.io", "https://startup.io",
         "Remote-first startup redefining collaboration.", 342, 18),

        ("DevOps Engineer",
         "Manage CI/CD pipelines, Kubernetes clusters, and cloud infrastructure on AWS.",
         "$90,000 – $130,000", "Full-time", "DevOps", "New York, NY",
         "Startup.io", "https://startup.io",
         "Remote-first startup redefining collaboration.", 210, 9),

        ("Senior Frontend Developer",
         "Craft pixel-perfect UIs with React and TypeScript for our SaaS dashboard.",
         "$95,000 – $125,000", "Full-time", "Engineering", "San Francisco, CA",
         "TechCorp Ltd.", "https://techcorp.com",
         "Enterprise software at scale.", 560, 31),

        ("Product Manager",
         "Drive product strategy and work cross-functionally with engineering and design.",
         "$100,000 – $140,000", "Full-time", "Product", "Austin, TX",
         "TechCorp Ltd.", "https://techcorp.com",
         "Enterprise software at scale.", 415, 22),

        ("UI/UX Designer",
         "Design intuitive user experiences from wireframes to high-fidelity prototypes in Figma.",
         "$70,000 – $95,000", "Contract", "Design", "Remote",
         "TechCorp Ltd.", "https://techcorp.com",
         "Enterprise software at scale.", 188, 7),

        ("Data Engineer",
         "Build and maintain data pipelines using Python and cloud-native tools.",
         "$85,000 – $115,000", "Full-time", "Data", "Chicago, IL",
         "BigCo Inc.", "https://bigco.com",
         "Global operations, local impact.", 299, 14),

        ("Go Backend Engineer",
         "Develop high-performance services in Go for our real-time data platform.",
         "$105,000 – $145,000", "Full-time", "Engineering", "Seattle, WA",
         "BigCo Inc.", "https://bigco.com",
         "Global operations, local impact.", 377, 20),

        ("ML Research Engineer",
         "Research and implement state-of-the-art ML models for robotics applications.",
         "$120,000 – $160,000", "Full-time", "AI/ML", "Boston, MA",
         "Ventures Labs", "https://ventureslabs.io",
         "Pushing the frontier of AI and robotics.", 503, 26),

        ("Part-time Data Analyst",
         "Analyse research datasets and produce weekly insight reports.",
         "$35/hr", "Part-time", "Data", "Remote",
         "Ventures Labs", "https://ventureslabs.io",
         "Pushing the frontier of AI and robotics.", 142, 5),
    ]

    for (title, desc, salary, jtype, jcat, loc,
         co_name, co_website, co_desc, views, applicants) in jobs_data:
        await conn.execute(
            """
            INSERT INTO jobs
              (title, description, salary_range, job_type, job_category,
               location, company_id, company_website, company_description,
               views, applicants, date_posted)
            VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,NOW())
            ON CONFLICT DO NOTHING
            """,
            title, desc, salary, jtype, jcat, loc,
            await cid(co_name), co_website, co_desc, views, applicants,
        )

    async def jid(title: str) -> int:
        return await conn.fetchval(
            "SELECT id FROM jobs WHERE title = $1", title
        )

    # ── 5. JOB-SKILL LINKS ────────────────────────────────────────────────
    print("  -> job_skill_links")
    job_skill_map = {
        "Backend Python Developer":  ["Python", "FastAPI", "PostgreSQL", "Docker"],
        "DevOps Engineer":           ["Docker", "Kubernetes", "AWS"],
        "Senior Frontend Developer": ["React", "TypeScript"],
        "Product Manager":           ["Project Management"],
        "UI/UX Designer":            ["Figma", "TypeScript"],
        "Data Engineer":             ["Python", "PostgreSQL", "AWS"],
        "Go Backend Engineer":       ["Go", "Docker", "Kubernetes"],
        "ML Research Engineer":      ["Python", "Machine Learning", "AWS"],
        "Part-time Data Analyst":    ["Python", "PostgreSQL"],
    }
    for job_title, skills in job_skill_map.items():
        j = await jid(job_title)
        for skill_name in skills:
            s = await sid(skill_name)
            await conn.execute(
                """
                INSERT INTO job_skill_links (job_id, skill_id)
                VALUES ($1, $2)
                ON CONFLICT DO NOTHING
                """,
                j, s,
            )

    # ── 6. APPLICATIONS ───────────────────────────────────────────────────
    print("  -> applications")
    applications = [
        ("alice_dev",     "Backend Python Developer",  "accepted",
         "/resumes/alice_dev_resume.pdf",
         "I have 4 years of FastAPI experience and shipped 3 production APIs."),
        ("alice_dev",     "Go Backend Engineer",       "pending",
         "/resumes/alice_dev_resume.pdf",
         "Excited to transition into Go — built two hobby projects."),
        ("bob_designer",  "UI/UX Designer",            "reviewed",
         "/resumes/bob_designer_resume.pdf",
         "Five years of Figma experience with a strong portfolio."),
        ("carol_pm",      "Product Manager",           "pending",
         "/resumes/carol_pm_resume.pdf",
         "Driven 0-to-1 products at two early-stage startups."),
        ("carol_pm",      "Data Engineer",             "rejected",
         "/resumes/carol_pm_resume.pdf",
         "Looking to pivot into data engineering; strong SQL background."),
        ("henry_backend", "Backend Python Developer",  "reviewed",
         "/resumes/henry_backend_resume.pdf",
         "Three years of Python microservices in fintech."),
        ("henry_backend", "ML Research Engineer",      "pending",
         "/resumes/henry_backend_resume.pdf",
         "Published two papers on transformer optimisation."),
        ("grace_data",    "Part-time Data Analyst",    "pending",
         "/resumes/grace_data_resume.pdf",
         "Seeking flexible hours while finishing my MSc in Data Science."),
    ]
    for username, job_title, status, resume, cover in applications:
        await conn.execute(
            """
            INSERT INTO applications
              (candidate_id, job_id, status, resume_path, cover_letter, applied_at)
            VALUES ($1, $2, $3, $4, $5, NOW())
            ON CONFLICT DO NOTHING
            """,
            await uid(username), await jid(job_title), status, resume, cover,
        )

    # ── 7. NOTIFICATIONS ──────────────────────────────────────────────────
    print("  -> notifications")
    notifications = [
        ("alice_dev",     'Your application for "Backend Python Developer" has been accepted.', True),
        ("alice_dev",     'Your application for "Go Backend Engineer" is under review.',        False),
        ("bob_designer",  'Your application for "UI/UX Designer" is now being reviewed.',       False),
        ("carol_pm",      'Unfortunately your application for "Data Engineer" was not selected.', True),
        ("carol_pm",      'Your application for "Product Manager" has been received.',           False),
        ("henry_backend", 'A new job matching your profile: "ML Research Engineer".',           False),
        ("dave_employer", 'Your post "Backend Python Developer" received 18 applications.',      True),
        ("eve_employer",  'Your post "Senior Frontend Developer" received 31 applications.',     True),
        ("admin_user",    "System: 4 new companies registered this month.",                      True),
    ]
    for username, message, is_read in notifications:
        await conn.execute(
            """
            INSERT INTO notifications (user_id, message, is_read, created_at)
            VALUES ($1, $2, $3, NOW())
            """,
            await uid(username), message, is_read,
        )

    print("\n[OK] Seed complete! All dummy data inserted successfully.")


async def main():
    print(f"Connecting to: {DSN}\n")
    conn = await asyncpg.connect(DSN)
    try:
        async with conn.transaction():
            await seed(conn)
    finally:
        await conn.close()


if __name__ == "__main__":
    asyncio.run(main())
