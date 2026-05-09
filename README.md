# Password Manager
Manage passwords using CLI 

# First time setup
python vault.py init

# Add a password
python vault.py add github john@email.com

# Get it (copies to clipboard)
python vault.py get github

# Get it printed to terminal
python vault.py get github --show

# List all sites
python vault.py list

# Delete an entry
python vault.py delete github
