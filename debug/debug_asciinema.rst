Debug Asciinema
==============================================================================
Asciinema is a tool can record terminal session and replay it back. It is good for demo.

.. code-block:: bash

    # record a new session
    asciinema rec example.cast --overwrite

    # upload to asciinema.org
    asciinema upload example_123.cast

Then you can use this in restructured text to refer to the video.

.. image:: https://asciinema.org/a/123456.svg
    :target: https://asciinema.org/a/123456


1. Demo
------------------------------------------------------------------------------
::

    s3 buc
    iam role
    ec2 inst
    lbd func
    sfn stat

    !@us west
    cf st
    dyn tab
    rds snap
