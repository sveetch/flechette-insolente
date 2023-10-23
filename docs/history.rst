.. _history_intro:

=======
History
=======

Version 0.4.0 - Unreleased
**************************

TODO


Version 0.3.0 - 2023/10/04
**************************

Totally changed spirit of this package, we dropped the idea of using *Embedded Host*
since it is very hard to get into working with it (Protobug, expected RPC
communication, etc..).

Instead we move this package as a Python wrapper that will use subprocess to execute
dart-sass binary.

At this stage, the command line ``compile`` is working correctly but it stills an
alpha prototype since it only support Linux 64bits plateform until we properly. Also
for now only a few set of dart-sass parameters are implemented.

This release won't be released on Pypi since we should implement the right way to get
sub packages for all executable plateforms.


Version 0.2.0 - Unreleased
**************************

It was the attempt to implement dart-sass embedding throught their *Embedded Host*
system with Protobuf. It just didn't make it, the spec does not help very much how
to communicate Protobuf packets with dart-sass executable.


Version 0.1.0 - Unreleased
**************************

* First commit from ookiecutter-sveetch-python==0.4.1.
