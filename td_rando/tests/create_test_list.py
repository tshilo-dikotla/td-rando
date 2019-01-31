import os
import csv
import random
from tempfile import mkdtemp


default_drug_assignments = ['NVP', 'AZT']


def create_test_list(full_path=None, drug_assignments=None, count=None, first_sid=None):
    first_sid = first_sid or 0
    count = count or 10
    if not full_path:
        full_path = os.path.join(mkdtemp(), 'randomizationlist.csv')
    drug_assignments = drug_assignments or default_drug_assignments
    with open(full_path, 'w') as f:
        writer = csv.DictWriter(
            f, fieldnames=['sid', 'drug_assignment'])
        writer.writeheader()
        for i in range(first_sid, count + first_sid):
            drug_assignment = random.choice(drug_assignments)
            writer.writerow(
                dict(sid=i, drug_assignment=drug_assignment))
    return full_path
