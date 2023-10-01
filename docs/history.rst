.. _history_intro:

=======
History
=======

Version 0.3.0 - Unreleased
**************************

Totally changed spirit of this package, we dropped the idea of using *Embedded Host*
since it is very hard to get into working with it (Protobug, expected RPC
communication, etc..).

Instead we move this package as a Python wrapper that will use subprocess to execute
dart-sass binary.


Version 0.2.0 - Unreleased
**************************

It was the attempt to implement dart-sass embedding throught their *Embedded Host*
system with Protobuf. It just didn't make it, the spec does not help very much how
to communicate Protobuf packets with dart-sass executable.


Version 0.1.0 - Unreleased
**************************

* First commit from ookiecutter-sveetch-python==0.4.1.
