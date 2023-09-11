.. _Python: https://www.python.org/
.. _Click: https://click.palletsprojects.com
.. _Embedded Sass Protocol: https://github.com/sass/sass/blob/main/spec/embedded-protocol.md
.. _Dart Sass: https://github.com/sass/dart-sass
.. _Protobuf: https://pypi.org/project/protobuf/

===================
Flêchette insolente
===================

Named after french version of `Dart Sass`_, this is a laboratory for research and
development on using Dart sass with its `Embedded Sass Protocol`_.


Dependencies
************

* `Python`_>=3.8;
* `Click`_>=8.0;
* `Protobuf`_>=24.0;


Goal
****

Embed a standalone version of dart-sass compiler into a Python package, such as it can
be installed from a project Python requirements without to install Dart or Node.


Study
*****

From `Node.js host <https://github.com/sass/embedded-host-node>`_ (which embed
dart-sass to be run from a Node.js library), i understood that:

* Package will need to include a compiled version of Dart sass (with its protocol
  enabled);
* There are multiple plateform builds for a compiled version;
* Seems the Node host build them during its release process or download it from
  https://github.com/sass/dart-sass/releases
* The compiled compiler have to be runned like an executable, we don't have something
  like a Python C module to manage or else;
* Once runned we dialog with compiler using the proctocol through STDIN commands and it
  will answer throught STDOUT, this is the only way to reach and instruct all compiler
  feature;
* Since dialog with protocol is normalized using
  Protocol buffers (see links section below), that is using a ``*.proto`` file to
  descript communication packets;


Protocol buffers links
**********************

* `Wikipedia definition <https://fr.wikipedia.org/wiki/Protocol_Buffers>`_;
* `Protobuf library repository <https://github.com/protocolbuffers/protobuf>`_;
* `Official package on Pypi <https://pypi.org/project/protobuf/>`_ (include precompiled
  protobuf);
* `Python tutorial <https://protobuf.dev/getting-started/pythontutorial/>`_;
* `Python API <https://googleapis.dev/python/protobuf/latest/>`_;
* `Generated code guide <https://protobuf.dev/reference/python/python-generated/>`_;
* `Proto file delivered by Sass <https://github.com/sass/sass/blob/main/spec/embedded_sass.proto>`_;
* `py-dart-sass <https://github.com/dumdoo/py-dart-sass>`_ a package which wrapped
  dart-sass (a version from 2022) without using protobuf (only using command argument).
  Nice but seems outdated and abandoned;

Plan
****

* Get the compiled compiler plateform version for my local system;
* Start a simple script to run the compiler;
* Try a basic way to dialog with compiler to compile a basic Sass source;
* When it's done, we can start to improve dialog to manage feature options and all;
* Look what Boussole will need to properly use this new compiler;
* Ensure everything is possible with Boussole;
* Stop this repository and start porting this science to Boussole to implement
  dart-sass support along libsass;


On-going work notes
*******************

* At first we need to compile ``*.proto`` file to a Python module using ``protoc``
  library that must be installed with system package;
* Current proto file from sass include "optional fields" which is a recent feature that
  seems to required at least a libprotoc>=3.12.x, the first proto compile try did failed
  because of libprotoc==3.6.1 that did not know about this feature;
* In protoc 3.12.x, optional fields is an experimental feature that require flag
  argument ``--experimental_allow_proto3_optional`` to be enabled, don't know if a more
  recent include it on default (protoc is currently in 3.21.x version);
* With downloaded `Proto file <https://github.com/sass/sass/blob/main/spec/embedded_sass.proto>`_,
  the following command succeed to build a Python module: ::

    protoc --experimental_allow_proto3_optional --python_out=. embedded_sass.proto

* I've filled an issue to Sass repo about
  `libprotoc version support <https://github.com/sass/sass/issues/3685>`_;
* [Proposal] Package should include all dart-sass plateform builds;
* [Hint] Python module for proto file don't need to be build on package install, it just
  have to fit to proto file version according to shipped dart-sass build version;
* Just tried to import classes from proto Python module and it fails with: ::

    Traceback (most recent call last):
    File "/home/emencia/Projects/Apps/flechette-insolente/dartsass/sass_version.py", line 2, in <module>
        from dartsass.embedded_sass_pb2 import InboundMessage, OutboundMessage
    File "/home/emencia/Projects/Apps/flechette-insolente/dartsass/embedded_sass_pb2.py", line 33, in <module>
        _descriptor.EnumValueDescriptor(
    File "/home/emencia/Projects/Apps/flechette-insolente/.venv/lib/python3.10/site-packages/google/protobuf/descriptor.py", line 796, in __new__
        _message.Message._CheckCalledFromGeneratedFile()
    TypeError: Descriptors cannot not be created directly.
    If this call came from a _pb2.py file, your generated code is out of date and must be regenerated with protoc >= 3.19.0.
    If you cannot immediately regenerate your protos, some other possible workarounds are:
    1. Downgrade the protobuf package to 3.20.x or lower.
    2. Set PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python (but this will use pure-Python parsing and will be much slower).

* So finally, with package protobuf 24.x, we need to compile proto file with
  protoc>=3.19.0;
* It makes me wonder how hard it will be to maintain this cohesion between
  flechette-insolente, protoc, protobuf and dart-sass. It involves many package
  versions that are not guaranteed to keep long support. Especially, dart-sass that
  seems to preview many breaking changes.
* At least, the basic usage with command arguments seems a possible escape of the hell
  of Protocol buffers, but it would need to checked on performance. Also command and
  popen would be less flexible;

**On hold, i need to find someone with a recent machine which have protoc>=3.19.0 to continue explore.**