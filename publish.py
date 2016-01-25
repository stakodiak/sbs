#!/usr/bin/python
import os
import re
import sys


# Make sure user has S3 credentials.
AWS_ACCESS_KEY = os.environ.get('S3_ACCESS_KEY')
AWS_SECRET_KEY = os.environ.get('S3_SECRET_KEY')

if not (AWS_SECRET_KEY and AWS_ACCESS_KEY):
    raise Exception("Could not find AWS credentials.")

# Create directory if it doesn't already exist.
TARGET_DIR = 'articles/'
if not os.path.exists(TARGET_DIR):
    os.makedirs(TARGET_DIR)


def publish(bucket_name, files):
    """Publish files to target S3 bucket.

    `bucket_name` - name of S3 bucket for which credentials can update.
    `files` - a list of filenames.

    Returns public-facing endpoint to URL.
    """
    from boto.s3.connection import S3Connection
    connection = S3Connection(AWS_ACCESS_KEY, AWS_SECRET_KEY)
    bucket = connection.get_bucket(bucket_name)

    # Update files on target S3 bucket.
    updated_files = []
    for filename in files:
        _publish_file(bucket, 'articles/' + filename)
        updated_files.append(filename)

    # Publish homepage.
    _publish_file(bucket, 'index.html')
    return bucket.get_website_endpoint()

def _publish_file(bucket, filename, target=None):
    from boto.s3.key import Key
    key = Key(bucket)
    key.set_metadata('Content-type', 'text/html')
    key.key = target or filename
    key.set_contents_from_filename(filename)

def main():
    """Get files in current directory and publish them to S3."""
    # Filter out in-progress articles.
    targets = filter(lambda f: not re.search(r'^\.', f),
                     os.listdir(TARGET_DIR))

    # Make sure user supplied bucket.
    try:
        bucket_name = sys.argv[1]
    except IndexError:
        print "Please supply a bucket name."
        sys.exit(1)

    # Push files to S3.
    print "Connecting..."
    published_endpoint = publish(bucket_name, files=targets)
    print "Updated", len(targets), "files at:"
    print published_endpoint


if __name__ == '__main__':
    main()
