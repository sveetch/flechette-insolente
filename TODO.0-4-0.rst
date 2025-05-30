==============
TODO for 0.4.0
==============

A list of on going jobs to complete 0.4.0 tasks from
https://github.com/sveetch/flechette-insolente/issues/1

- [ ] Tests compile CLI effectively on compilation results;
- [ ] Cover dart-sass arguments, only the compatible ones which means they can work
      with the cli from flechette (like option for stdin usage is not compatible since
      we don't support stdin input);

      * [x] Arguments should not be in compiler module anymore;
      * [x] Arguments dicts should be divided from the model;
      * [x] Arguments validator will move along the model;
      * [x] All useful dart-sass options have been defined
      * [ ] Add validation method for all options:

        - [x] source
        - [x] destination
        - [x] charset
        - [ ] embed_sources
        - [ ] embed_source_map
        - [ ] error_css
        - [x] load_path
        - [x] source_map
        - [ ] source_map_urls
        - [ ] stop_on_error
        - [x] style
        - [ ] update

- [ ] Include output from ``sass --help`` as a document somewhere in the repository so
      we can regenerate it on each dart-sass upgrade to quickly watch for possible
      changes;
