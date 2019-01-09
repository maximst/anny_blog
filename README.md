Anny blog
=========

```
for m in blog core user_profile radio poll tag; do ./manage.py migrate --fake $m zero; ./manage.py migrate --fake-initial $m; done

./manage.py migrate --fake blog

./manage.py migrate --fake-initial
```
