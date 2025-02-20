#!/usr/bin/env python

# ChatGPT Ref: https://chat.openai.com/c/24090115-3356-40f3-9c6f-50ee84c6e48f

# Usage Example:
#   ./extract-coredata-model-hierarchy.py /Users/devalias/Library/Reminders/Container_v1/Stores/Data-5070B790-D66D-40F7-8F4A-EC8E0FA88F3A.sqlite

import argparse
import sqlite3

# Set up argument parsing
parser = argparse.ArgumentParser(description='Extract and organize model hierarchy from a CoreData SQLite database.')
parser.add_argument('db_path', help='Path to the CoreData SQLite database file.')

# Parse arguments
args = parser.parse_args()

# Connect to the SQLite database using the provided path
conn = sqlite3.connect(args.db_path)
cur = conn.cursor()

# Execute the SQL query to fetch model data
cur.execute("SELECT Z_ENT, Z_NAME, Z_SUPER FROM Z_PRIMARYKEY")
data = cur.fetchall()

# Close the database connection
conn.close()

# Process and organize the data

# Convert list of tuples into a dictionary for easier processing
# models = {ent: {'name': name, 'super': super_, 'children': []} for ent, name, super_ in data}
models = {ent: {'id': ent, 'name': name, 'super': super_, 'children': []} for ent, name, super_ in data}

# Organize models into a hierarchy
for ent, model in models.items():
  super_ = model['super']
  if super_ != 0:
    models[super_]['children'].append(model)

# Function to format the hierarchy as a markdown list
def format_as_markdown(model, indent=0):
  # markdown = "  " * indent + f"- {model['name']}\n"
  # markdown = "  " * indent + f"- {model['id']}: {model['name']}\n"

  # Calculate table name for top-level models
  table_name = f" (Table: Z{model['name'].upper()})" if model['super'] == 0 and model['id'] < 16000 else ""
  markdown = "  " * indent + f"- {model['id']}: {model['name']}{table_name}\n"

  for child in model['children']:
    markdown += format_as_markdown(child, indent + 1)
  return markdown

# Generate markdown for top-level models
markdown = ""
for model in models.values():
  if model['super'] == 0:
    markdown += format_as_markdown(model)

print(markdown)