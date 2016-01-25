# sbs
simple blogging service
```bash
echo "my entry what's up" >> entries/my-first-entry
./build.py
./publish.py my-already-created-bucket
```

#### Make sure to create a S3 bucket.
 Create a S3 bucket and enable "static website hosting." The document root should be `index.html.`
