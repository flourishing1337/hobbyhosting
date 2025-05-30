# Admin Panel

This is a lightweight placeholder for the admin panel application. It allows Docker Compose builds to succeed when the real implementation is missing.

The page now includes a basic file upload form that interacts with the `/files` API in the `admin_sync_service`. Uploaded files are listed below the form and can be downloaded by other admins.

Additionally, the panel lists registered users with buttons to promote or demote their admin status using the authentication service.
