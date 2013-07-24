from django.conf import settings

import boto
import os

def remove_local_images():
    """Remove all images from the web server."""
    file_list = [f for f in os.listdir(settings.MEDIA_IMAGE_ROOT)]
    for f in file_list:
        os.remove(settings.MEDIA_IMAGE_ROOT + f)

def s3_upload(employee):
    """Upload profile image to Amazon S3."""
    file_name  = '%s/%s' % (settings.MEDIA_ROOT, employee.image.name)
    bucket_key = 'media/%s%s/%s.jpg' % (settings.IMAGE_URL, employee.pk, 
        employee.pk)

    s3 = boto.connect_s3(settings.AWS_ACCESS_KEY_ID, 
        settings.AWS_SECRET_ACCESS_KEY)
    bucket = s3.get_bucket(settings.BUCKET_NAME)
    key = bucket.new_key(bucket_key)
    key.set_contents_from_filename(file_name)
    key.set_acl('public-read')

def tier_lab_sum(employees):
    """Return the tier lab sum of employees."""
    if employees:
        try:
            # check to see if list contains Employee model
            employees[0].tier_lab
            return sum([e.tier_lab for e in employees])
        except AttributeError:
            print 'AttributeError: tier_lab_sum()'

def tier_balance(first, second):
    """Check to see if the employee tier levels are balanced."""
    print ('-' * 10) + ' Tier Balance ' + ('-' * 10)
    var   = (len(first) + len(second))/5
    ratio = len(first)/float(len(second))
    f_sum = tier_lab_sum(first)
    s_sum = tier_lab_sum(second)
    mtier = s_sum * ratio
    print 'First Tier: %s, Second Tier: %s, Ratio: %s' % (f_sum, s_sum, ratio)
    if f_sum >= mtier - var and f_sum <= mtier + var:
        return True