from fetch_updates import fetch_updates


updates = fetch_updates()
for update in updates:
    print(update)