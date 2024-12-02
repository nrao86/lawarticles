import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json

def fetch_legal_updates():
    # List of legal news sources
    sources = [
        'https://www.livelaw.in/top-stories',
        'https://www.barandbench.com/news',
        'https://lawupdates.in/'
    ]
    
    updates = []
    for source in sources:
        try:
            response = requests.get(source, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(response.text, 'html.parser')
            # Extract articles (simplified - you'll need to adjust selectors)
            articles = soup.find_all('article')[:5]
            for article in articles:
                updates.append({
                    'title': article.find('h2').text.strip(),
                    'content': article.find('p').text.strip(),
                    'source': source
                })
        except Exception as e:
            print(f"Error fetching from {source}: {str(e)}")
    
    return updates

def create_markdown_file(update):
    today = datetime.now()
    date_str = today.strftime('%Y-%m-%d')
    file_name = f"docs/{date_str}-legal-update.md"
    
    content = f"""---
layout: post
title: "Legal Update: {update['title']}"
date: {date_str}
categories: [Legal Updates, Daily Digest]
---

# {update['title']}

*Published: {today.strftime('%B %d, %Y')}*

## Summary
{update['content']}

## Key Points
- Important legal development affecting [specific area]
- Implications for practitioners and public
- Changes in legal procedure or interpretation

## Practical Implications
1. For Legal Practitioners:
   - [Specific implications]
   - [Required actions]

2. For the General Public:
   - [How this affects common citizens]
   - [Steps to ensure compliance]

## Source
Original coverage: [{update['source']}]({update['source']})

---
*Note: This is an automated summary. Please refer to original sources and legal professionals for detailed understanding.*
"""

    # Update index page
    try:
        with open('docs/index.md', 'r') as f:
            index_content = f.read()
        
        # Add new entry under Latest Articles
        new_entry = f"- [{update['title']}]({date_str}-legal-update) - *{today.strftime('%B %d, %Y')}*\n"
        insert_point = index_content.find('## Latest Articles\n') + len('## Latest Articles\n')
        updated_index = index_content[:insert_point] + new_entry + index_content[insert_point:]
        
        with open('docs/index.md', 'w') as f:
            f.write(updated_index)
            
    except Exception as e:
        print(f"Error updating index: {str(e)}")

    # Write the new article
    with open(file_name, 'w') as f:
        f.write(content)

def main():
    updates = fetch_legal_updates()
    if updates:
        # Select the most relevant update (you might want to add more sophisticated selection logic)
        create_markdown_file(updates[0])

if __name__ == "__main__":
    main()