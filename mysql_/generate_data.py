import json
import string
import random
import pandas as pd


items = []
items_json = []
for _ in range(10):
    jid = ''.join(random.sample(string.ascii_letters, 8))
    
    item = {'job_id': jid, 'job_name': 'foo_' + jid}
    items.append(item)

    new_jid = jid if random.random() > 0.5 else 'j_' + jid
    items_json.append({
        'job_id': new_jid,
        'xdata': json.dumps(item)
    })

pd.DataFrame(items).to_csv('items.csv', header=True, index=False)

with open('items_json.csv', 'w') as f:
    for item in items_json:
        row = '{}::{}\n'.format(item['job_id'], item['xdata'])
        f.write(row)

