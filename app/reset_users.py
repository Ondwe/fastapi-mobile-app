#!/usr/bin/env python3
"""
Script to reset the user database and clear any corrupted data
"""
from app.auth import users_db

print("🧹 Resetting user database...")
print(f"Current users: {list(users_db.keys())}")

# Clear all users
users_db.clear()

print("✅ User database cleared!")
print(f"Users after reset: {list(users_db.keys())}")
