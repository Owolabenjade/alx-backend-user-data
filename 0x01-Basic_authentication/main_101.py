#!/usr/bin/env python3
""" Main 101 - Test wildcard excluded paths
"""
from api.v1.auth.auth import Auth

a = Auth()

# Test with wildcard
excluded_paths = ["/api/v1/stat*"]
print("Excluded paths: {}".format(excluded_paths))
print()

# Test various paths
test_paths = [
    "/api/v1/users",
    "/api/v1/status",
    "/api/v1/stats",
    "/api/v1/stat",
    "/api/v1/statistics",
    "/api/v1/stat/data",
    "/api/v1/sta",
    "/api/v1/states"
]

for path in test_paths:
    result = a.require_auth(path, excluded_paths)
    print("{}: {}".format(path, result))

print("\n--- Testing with multiple patterns ---")
excluded_paths = ["/api/v1/stat*", "/api/v1/users", "/auth/*"]
print("Excluded paths: {}".format(excluded_paths))
print()

test_paths = [
    "/api/v1/users",
    "/api/v1/status",
    "/api/v1/stats",
    "/api/v1/data",
    "/auth/login",
    "/auth/logout",
    "/authenticate"
]

for path in test_paths:
    result = a.require_auth(path, excluded_paths)
    print("{}: {}".format(path, result))