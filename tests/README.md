# Unit Tests

This folder contians unit tests for the project.  When making a commit, your code changes should pass any tests left in here.

If you decide to make changes to the test cases, you must justify the reason in your commit for making the change (such as a refactoring or structural change or feature addition).  Here are are further additions:

## All test cases

All tests should **simulate** HTTP requests rather than actually doing them.  This prevents you from encouring quota while developing.  Feel free to include test fixtures that simulate the structure of real API calls.

## Feature Additions

Feature additions should be flagged clearly, and unit tests added or modified for them.  Do not propose a feature to this repository without including a working pytest for it.

## Bug fixes

If your commit may cause a test to fail as it is currently written, please explain why this is the case when modifying a unit test.
