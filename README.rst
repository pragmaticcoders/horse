horse
=====

.. image:: https://travis-ci.org/pragmaticcoders/horse.svg?branch=master
   :target: https://travis-ci.org/pragmaticcoders/horse
   :alt: Latest Travis CI build status

Handy Open Recommendation Service

Frontend app url:
   http://test-horse.s3-website-eu-west-1.amazonaws.com/

Backend app url:
   http://horse-env.pqmnkwtbum.eu-west-1.elasticbeanstalk.com/

Frontend app repository:
   https://github.com/pragmaticcoders/horse-frontend

Recommendation assumptions
--------------------------

- User movie recommendations are influenced by general movie popularity.
- Movies liked by followed users are more likely to be recommended. That relation is recursive, but with exponentialy decreasing power.
- Similarity score between any pair of users can be calculated. It is based on a count of commonly liked movies and is adjusted according to a total number of movies graded by both users.
- Movie recommendations are influenced by all points above.


Installation
------------

Python 3.4 is required.

.. code-block::

   $ cd horse
   $ pip install .
   $ python application.py


Testing
-------

.. code-block::

   $ tox


Populate with example dataset
-------

.. code-block::

   $ curl -X POST http://127.0.0.1:5000/populate -d @./examples/populate.json --header "Content-Type: application/json"
