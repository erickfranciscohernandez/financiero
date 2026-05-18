#!/usr/bin/env python3
"""
Script de prueba para generar un newsletter con datos de demostración
Útil para ver cómo se vería el newsletter con información completa
"""
import json
from datetime import datetime, timedelta

def create_demo_commits():
    """Create demo commit data that matches the API structure"""
    now = datetime.utcnow()

    demo_data = [
        {
            "sha": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6",
            "commit": {
                "author": {
                    "name": "Erick Francisco Hernandez",
                    "date": (now - timedelta(hours=12)).isoformat() + "Z"
                },
                "message": "feat: implement automated newsletter compilation system"
            },
            "html_url": "https://github.com/erickfranciscohernandez/financiero/commit/a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6",
            "stats": {
                "additions": 342,
                "deletions": 45
            }
        },
        {
            "sha": "b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7",
            "commit": {
                "author": {
                    "name": "Claude AI Assistant",
                    "date": (now - timedelta(hours=8)).isoformat() + "Z"
                },
                "message": "docs: update README with GitHub Pages setup instructions"
            },
            "html_url": "https://github.com/erickfranciscohernandez/financiero/commit/b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7",
            "stats": {
                "additions": 87,
                "deletions": 12
            }
        },
        {
            "sha": "c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8",
            "commit": {
                "author": {
                    "name": "Erick Francisco Hernandez",
                    "date": (now - timedelta(hours=4)).isoformat() + "Z"
                },
                "message": "fix: resolve GitHub Pages 404 error and enable publication"
            },
            "html_url": "https://github.com/erickfranciscohernandez/financiero/commit/c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8",
            "stats": {
                "additions": 23,
                "deletions": 5
            }
        },
        {
            "sha": "d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9",
            "commit": {
                "author": {
                    "name": "Claude AI Assistant",
                    "date": (now - timedelta(hours=2)).isoformat() + "Z"
                },
                "message": "enhance: add detailed statistics and metrics to newsletter"
            },
            "html_url": "https://github.com/erickfranciscohernandez/financiero/commit/d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9",
            "stats": {
                "additions": 156,
                "deletions": 28
            }
        }
    ]

    return demo_data

if __name__ == "__main__":
    print("📋 Datos de demostración para el newsletter:")
    print(json.dumps(create_demo_commits(), indent=2))
