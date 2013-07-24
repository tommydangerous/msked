from msked import settings
from django.core.management import setup_environ
setup_environ(settings)

from employees.models import Employee

import csv

file_name = 'employees.csv'
if not settings.DEV:
   file_name = '%s/%s' % (settings.project_name, file_name)
with open(file_name, 'rb') as f:
   reader = csv.reader(f)
   for row in reader:
      names = row[0].split(' ')
      if len(names) >= 2:
         first_name = names[0].title()
         last_name  = names[-1].title()
         try:
            employee = Employee.objects.get(first_name=first_name, 
               last_name=last_name)
         except Employee.DoesNotExist:
            employee = Employee.objects.create(first_name=first_name,
               last_name=last_name, tier_lab=2)
            print '%s %s' % (employee.first_name, employee.last_name)