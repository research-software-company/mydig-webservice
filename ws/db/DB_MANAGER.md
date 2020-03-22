
### Create the DB:

You can create and update a user with the script "create_user.py"

>usage: create_user.py [-h] [--admin] email password
>
>positional arguments:
>  email       The Email address of the user
>  password    The password
>
>optional arguments:
>  -h, --help  show this help message and exit
>  --admin     Set the user permissions to 'Admin'

Examples:
```
python create_user.py admin@gig.org dig --admin
python create_user.py user1@gig.org dig
```

Another useful Python command:
`db.session.rollback()`