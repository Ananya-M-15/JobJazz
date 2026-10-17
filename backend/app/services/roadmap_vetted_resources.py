"""
Vetted learning resources, official documentation links, and project exercises for JobJazz skills.
All URLs are verified official sites or reputable free educational platforms.
"""
from typing import Literal
from app.schemas.roadmap import LearningResource, ResourceFormat, BudgetPreference


VETTED_CATALOGUE: dict[str, list[dict]] = {
    "Python": [
        {
            "title": "Official Python 3 Documentation & Tutorial",
            "provider": "Python Software Foundation",
            "url": "https://docs.python.org/3/tutorial/",
            "resource_type": "documentation",
            "pricing": "free",
            "difficulty": "beginner",
            "why_relevant": "The official language reference covering syntax, data structures, and standard libraries.",
            "estimated_duration": "10-15 hours",
        },
        {
            "title": "Scientific Computing with Python",
            "provider": "freeCodeCamp",
            "url": "https://www.freecodecamp.org/learn/scientific-computing-with-python/",
            "resource_type": "course",
            "pricing": "free",
            "difficulty": "intermediate",
            "why_relevant": "Hands-on video lectures and interactive coding challenges covering core and advanced Python.",
            "estimated_duration": "20-30 hours",
        },
    ],
    "FastAPI": [
        {
            "title": "FastAPI Official Tutorial & User Guide",
            "provider": "FastAPI / Tiangolo",
            "url": "https://fastapi.tiangolo.com/tutorial/",
            "resource_type": "documentation",
            "pricing": "free",
            "difficulty": "intermediate",
            "why_relevant": "Step-by-step official guide to building asynchronous REST APIs with Pydantic and type hints.",
            "estimated_duration": "8-12 hours",
        },
        {
            "title": "Full Stack FastAPI Template & Architecture",
            "provider": "FastAPI GitHub",
            "url": "https://github.com/fastapi/full-stack-fastapi-template",
            "resource_type": "project_guide",
            "pricing": "free",
            "difficulty": "advanced",
            "why_relevant": "Production-grade project blueprint featuring Docker, PostgreSQL, Alembic, and JWT auth.",
            "estimated_duration": "15 hours",
        },
    ],
    "SQL": [
        {
            "title": "PostgreSQL Official Documentation: SQL Tutorial",
            "provider": "PostgreSQL Global Development Group",
            "url": "https://www.postgresql.org/docs/current/tutorial-sql.html",
            "resource_type": "documentation",
            "pricing": "free",
            "difficulty": "beginner",
            "why_relevant": "Authoritative reference for relational tables, queries, joins, aggregates, and subqueries.",
            "estimated_duration": "6-10 hours",
        },
        {
            "title": "Relational Database Course",
            "provider": "freeCodeCamp",
            "url": "https://www.freecodecamp.org/learn/relational-database/",
            "resource_type": "course",
            "pricing": "free",
            "difficulty": "intermediate",
            "why_relevant": "Interactive terminal-based PostgreSQL and Bash challenges building real database schemas.",
            "estimated_duration": "25 hours",
        },
    ],
    "PostgreSQL": [
        {
            "title": "PostgreSQL Exercises & Interactive Queries",
            "provider": "PGExercises",
            "url": "https://pgexercises.com/",
            "resource_type": "tutorial",
            "pricing": "free",
            "difficulty": "intermediate",
            "why_relevant": "Practical SQL problem sets covering aggregations, recursive queries, CTEs, and windows.",
            "estimated_duration": "10-15 hours",
        },
        {
            "title": "PostgreSQL Official Manual",
            "provider": "PostgreSQL.org",
            "url": "https://www.postgresql.org/docs/current/",
            "resource_type": "documentation",
            "pricing": "free",
            "difficulty": "advanced",
            "why_relevant": "Complete reference on indexing, query optimization (EXPLAIN ANALYZE), and transactions.",
            "estimated_duration": "12 hours",
        },
    ],
    "Docker": [
        {
            "title": "Docker Official Get Started Guide",
            "provider": "Docker Inc.",
            "url": "https://docs.docker.com/get-started/",
            "resource_type": "documentation",
            "pricing": "free",
            "difficulty": "beginner",
            "why_relevant": "Hands-on orientation covering Dockerfile creation, image building, and multi-container Compose.",
            "estimated_duration": "6-8 hours",
        },
        {
            "title": "Docker for Developers",
            "provider": "freeCodeCamp",
            "url": "https://www.freecodecamp.org/news/the-docker-handbook/",
            "resource_type": "tutorial",
            "pricing": "free",
            "difficulty": "intermediate",
            "why_relevant": "Comprehensive handbook covering networking, volumes, multi-stage builds, and production safety.",
            "estimated_duration": "8-10 hours",
        },
    ],
    "Kubernetes": [
        {
            "title": "Kubernetes Official Interactive Tutorials",
            "provider": "Cloud Native Computing Foundation (CNCF)",
            "url": "https://kubernetes.io/docs/tutorials/kubernetes-basics/",
            "resource_type": "documentation",
            "pricing": "free",
            "difficulty": "intermediate",
            "why_relevant": "Learn cluster architecture, pods, deployments, services, and rolling updates in an interactive browser shell.",
            "estimated_duration": "10-14 hours",
        },
    ],
    "AWS": [
        {
            "title": "AWS Cloud Practitioner Essentials",
            "provider": "Amazon Web Services (AWS Skill Builder)",
            "url": "https://explore.skillbuilder.aws/learn/course/external/view/elearning/134/aws-cloud-practitioner-essentials",
            "resource_type": "course",
            "pricing": "free",
            "difficulty": "beginner",
            "why_relevant": "Free official fundamental training covering compute (EC2/Lambda), storage (S3), databases (RDS), and IAM.",
            "estimated_duration": "6 hours",
        },
        {
            "title": "AWS Architecture Center & Implementation Guides",
            "provider": "Amazon Web Services",
            "url": "https://aws.amazon.com/architecture/",
            "resource_type": "documentation",
            "pricing": "free",
            "difficulty": "intermediate",
            "why_relevant": "Reference architectures and well-architected framework principles for cloud engineers.",
            "estimated_duration": "8 hours",
        },
    ],
    "React": [
        {
            "title": "React Official Documentation: Learn React",
            "provider": "React Core Team / Meta",
            "url": "https://react.dev/learn",
            "resource_type": "documentation",
            "pricing": "free",
            "difficulty": "beginner",
            "why_relevant": "Modern guide to components, state management, effects, and custom hooks with interactive sandboxes.",
            "estimated_duration": "12-16 hours",
        },
        {
            "title": "Front End Development Libraries: React",
            "provider": "freeCodeCamp",
            "url": "https://www.freecodecamp.org/learn/front-end-development-libraries/#react",
            "resource_type": "course",
            "pricing": "free",
            "difficulty": "intermediate",
            "why_relevant": "Step-by-step project-based challenges building full React applications.",
            "estimated_duration": "15-20 hours",
        },
    ],
    "JavaScript": [
        {
            "title": "MDN Web Docs: JavaScript Guide",
            "provider": "Mozilla Developer Network",
            "url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide",
            "resource_type": "documentation",
            "pricing": "free",
            "difficulty": "intermediate",
            "why_relevant": "The definitive industry reference covering modern ES6+, async/await, closures, and the event loop.",
            "estimated_duration": "15 hours",
        },
    ],
    "TypeScript": [
        {
            "title": "TypeScript for JavaScript Programmers",
            "provider": "Microsoft",
            "url": "https://www.typescriptlang.org/docs/handbook/typescript-in-5-minutes.html",
            "resource_type": "documentation",
            "pricing": "free",
            "difficulty": "intermediate",
            "why_relevant": "Official quickstart guide on static typing, interfaces, generics, and compiler configuration.",
            "estimated_duration": "6-8 hours",
        },
    ],
    "Machine Learning": [
        {
            "title": "Scikit-Learn Machine Learning in Python",
            "provider": "Inria / Scikit-learn Consortium",
            "url": "https://scikit-learn.org/stable/tutorial/",
            "resource_type": "documentation",
            "pricing": "free",
            "difficulty": "intermediate",
            "why_relevant": "Hands-on tutorials for regression, classification, cross-validation, and pipeline evaluation.",
            "estimated_duration": "15 hours",
        },
        {
            "title": "Machine Learning Specialization Companion",
            "provider": "DeepLearning.AI",
            "url": "https://www.deeplearning.ai/courses/machine-learning-specialization/",
            "resource_type": "course",
            "pricing": "free",
            "difficulty": "beginner",
            "why_relevant": "Foundational course on supervised and unsupervised learning led by Andrew Ng.",
            "estimated_duration": "30 hours",
        },
    ],
    "PyTorch": [
        {
            "title": "PyTorch Official Deep Learning Tutorials",
            "provider": "PyTorch Foundation / Linux Foundation",
            "url": "https://pytorch.org/tutorials/",
            "resource_type": "documentation",
            "pricing": "free",
            "difficulty": "intermediate",
            "why_relevant": "Official walkthroughs for tensors, autograd, neural network modules, and GPU training.",
            "estimated_duration": "12-16 hours",
        },
    ],
    "TensorFlow": [
        {
            "title": "TensorFlow Core Tutorials",
            "provider": "Google TensorFlow Team",
            "url": "https://www.tensorflow.org/tutorials",
            "resource_type": "documentation",
            "pricing": "free",
            "difficulty": "intermediate",
            "why_relevant": "Official guide to Keras models, data pipelines with tf.data, and model export.",
            "estimated_duration": "12-16 hours",
        },
    ],
    "Git": [
        {
            "title": "Pro Git Book (Official Free Edition)",
            "provider": "Scott Chacon & Ben Straub / Git-SCM",
            "url": "https://git-scm.com/book/en/v2",
            "resource_type": "documentation",
            "pricing": "free",
            "difficulty": "beginner",
            "why_relevant": "The official book on branching strategies, rebasing, remotes, and conflict resolution.",
            "estimated_duration": "8-10 hours",
        },
    ],
    "GitHub": [
        {
            "title": "GitHub Skills: Interactive Walkthroughs",
            "provider": "GitHub",
            "url": "https://skills.github.com/",
            "resource_type": "tutorial",
            "pricing": "free",
            "difficulty": "beginner",
            "why_relevant": "Interactive repositories teaching pull requests, issue tracking, and GitHub Actions CI/CD.",
            "estimated_duration": "4-6 hours",
        },
    ],
    "REST APIs": [
        {
            "title": "REST API Design Best Practices",
            "provider": "Red Hat Developer",
            "url": "https://www.redhat.com/en/topics/api/what-is-a-rest-api",
            "resource_type": "article",
            "pricing": "free",
            "difficulty": "beginner",
            "why_relevant": "Clear guide on HTTP methods, status codes, RESTful resource naming, and idempotency.",
            "estimated_duration": "4 hours",
        },
    ],
    "MongoDB": [
        {
            "title": "MongoDB University: Free Developer Courses",
            "provider": "MongoDB Inc.",
            "url": "https://learn.mongodb.com/",
            "resource_type": "course",
            "pricing": "free",
            "difficulty": "beginner",
            "why_relevant": "Official courses covering document modeling, aggregation pipelines, and driver integration.",
            "estimated_duration": "10 hours",
        },
    ],
}


VETTED_PROJECT_TEMPLATES: dict[str, dict] = {
    "Python": {
        "title": "Command-Line Career Portfolio & Data Parser",
        "description": "Build an object-oriented Python CLI tool that parses structured files, validates inputs, and outputs formatted summaries.",
        "deliverable": "A tested Python package on GitHub with README, unit tests, and virtual environment setup.",
        "hours": 8.0,
    },
    "FastAPI": {
        "title": "Production REST API with Auth & Database",
        "description": "Build an asynchronous CRUD REST API for job tracking with JWT bearer authentication, Pydantic v2 schemas, and PostgreSQL integration.",
        "deliverable": "A deployed FastAPI service with Swagger documentation, automated pytest test suite, and Alembic migrations.",
        "hours": 12.0,
    },
    "SQL": {
        "title": "Relational Career Analytics Database",
        "description": "Design an indexed PostgreSQL schema modeling job postings, companies, and skills. Write complex analytical queries using window functions, CTEs, and aggregations.",
        "deliverable": "A documented SQL schema script with realistic seed data and 10 analytical report queries.",
        "hours": 6.0,
    },
    "Docker": {
        "title": "Multi-Service Containerized Environment",
        "description": "Containerize a backend application and a PostgreSQL database using multi-stage Dockerfiles and Docker Compose.",
        "deliverable": "A reproducible Docker Compose configuration running health checks, persistent volumes, and non-root execution.",
        "hours": 6.0,
    },
    "Kubernetes": {
        "title": "Local Cluster Deployment with K8s Manifests",
        "description": "Deploy a containerized API to Minikube or Kind using declarative Deployments, Services, ConfigMaps, and Resource Limits.",
        "deliverable": "A repository containing clean Kubernetes YAML manifests with a rolling update demonstration.",
        "hours": 8.0,
    },
    "AWS": {
        "title": "Cloud-Hosted Serverless API Architecture",
        "description": "Deploy an API using AWS Lambda and API Gateway, storing documents in Amazon S3 with IAM role-based least privilege.",
        "deliverable": "A working AWS cloud architecture with architecture diagram and deployment documentation.",
        "hours": 10.0,
    },
    "React": {
        "title": "Interactive JobJazz Dashboard Feature",
        "description": "Develop a responsive React component showcasing progress tracking, filtering, and live state updates with Tailwind CSS.",
        "deliverable": "A deployed React front-end application with reusable component architecture and accessible UI.",
        "hours": 10.0,
    },
    "Machine Learning": {
        "title": "End-to-End Skill Match Predictor",
        "description": "Build a predictive model using Scikit-learn or PyTorch, including data preprocessing, feature engineering, cross-validation, and metric reporting.",
        "deliverable": "A documented Jupyter notebook and clean inference script published to GitHub with performance benchmarks.",
        "hours": 14.0,
    },
}


def get_vetted_resources_for_skill(
    skill: str,
    format_pref: ResourceFormat = ResourceFormat.MIX,
    budget_pref: BudgetPreference = BudgetPreference.FREE,
) -> list[LearningResource]:
    """Retrieve verified, high-quality resources matching skill and preferences."""
    raw_list = VETTED_CATALOGUE.get(skill, [])
    if not raw_list:
        # Fallback to general skill search link or default
        return [
            LearningResource(
                title=f"{skill} Technical Documentation & Guides",
                provider="Official Sources / DevDocs",
                url=f"https://devdocs.io/#q={skill.lower()}",
                resource_type="documentation",
                skill=skill,
                why_relevant=f"Comprehensive API and syntax reference for {skill}.",
                pricing="free",
                difficulty="intermediate",
                estimated_duration="Self-paced",
                is_verified=True,
                source="vetted_catalogue",
            )
        ]

    results = []
    for item in raw_list:
        # Budget filter
        if budget_pref == BudgetPreference.FREE and item["pricing"] != "free":
            continue

        # Format filter
        if format_pref == ResourceFormat.DOCS and item["resource_type"] not in ("documentation", "article"):
            continue
        if format_pref == ResourceFormat.COURSES and item["resource_type"] not in ("course", "tutorial"):
            continue

        results.append(
            LearningResource(
                title=item["title"],
                provider=item["provider"],
                url=item["url"],
                resource_type=item["resource_type"],
                skill=skill,
                why_relevant=item["why_relevant"],
                pricing=item["pricing"],
                difficulty=item["difficulty"],
                estimated_duration=item.get("estimated_duration", "Self-paced"),
                is_verified=True,
                source="vetted_catalogue",
            )
        )

    if not results and raw_list:
        # If filtering produced empty list, include the first vetted resource anyway
        first = raw_list[0]
        results.append(
            LearningResource(
                title=first["title"],
                provider=first["provider"],
                url=first["url"],
                resource_type=first["resource_type"],
                skill=skill,
                why_relevant=first["why_relevant"],
                pricing=first["pricing"],
                difficulty=first["difficulty"],
                estimated_duration=first.get("estimated_duration", "Self-paced"),
                is_verified=True,
                source="vetted_catalogue",
            )
        )

    return results


def validate_and_sanitize_resource(raw: dict) -> LearningResource | None:
    """Validate resource syntax, filter hallucinated/dummy URLs, and annotate verification status."""
    url = str(raw.get("url", "")).strip()
    if not (url.startswith("http://") or url.startswith("https://")):
        return None

    # Filter obvious placeholder or invalid domains
    blacklisted_domains = [
        "example.com",
        "url.com",
        "link.com",
        "placeholder",
        "yourdomain",
        "mysite",
        "fake",
        "test.com",
    ]
    if any(bl in url.lower() for bl in blacklisted_domains):
        return None

    title = str(raw.get("title", "")).strip()
    if not title or len(title) < 3:
        return None

    skill = str(raw.get("skill", "")).strip() or "General"
    provider = str(raw.get("provider", "Educational Resource")).strip()
    pricing = raw.get("pricing", "free")
    if pricing not in ("free", "paid", "unknown"):
        pricing = "unknown"

    # Check if this URL or provider is known in our vetted catalogue
    is_verified = False
    for vetted_list in VETTED_CATALOGUE.values():
        for vetted in vetted_list:
            if vetted["url"].lower() in url.lower() or url.lower() in vetted["url"].lower():
                is_verified = True
                break
        if is_verified:
            break

    return LearningResource(
        title=title,
        provider=provider,
        url=url,
        resource_type=raw.get("resource_type", "tutorial"),
        skill=skill,
        why_relevant=raw.get("why_relevant", f"Covers key concepts required for {skill}."),
        pricing=pricing,
        difficulty=raw.get("difficulty", "intermediate"),
        estimated_duration=raw.get("estimated_duration", "Self-paced"),
        is_verified=is_verified,
        source="gemini_grounded" if raw.get("source") == "gemini_grounded" else ("vetted_catalogue" if is_verified else "external"),
    )
