Rebuild ceph with code coverage enabled

This script pulls the latest (already-released) build out of Brew and
scratch-builds it with code coverage enabled. It generates a Yum repository and
stores the artifacts on a remote server.

This allows QE to use these builds to get code coverage metrics.


Prerequisites
-------------

You will need the ``brewkoji`` package::

    (Add the RCMTOOLS repository to /etc/yum.repos.d)

    sudo yum -y install brewkoji

Getting the code
----------------

Clone this repository::

    git clone https://github.com/ktdreyer/build-ceph-coverage
    cd build-ceph-coverage

Running
-------

Ensure you have a Kerberos ticket::

   kinit kdreyer

Run the script::

   ./rebuild.py
