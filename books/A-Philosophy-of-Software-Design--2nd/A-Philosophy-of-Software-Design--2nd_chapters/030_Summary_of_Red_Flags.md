Summary of Red Flags

Here are a few of of the most important red flags discussed in this book. The presence of any of these symptoms in a system suggests that there is a problem with the system's design:

[Shallow Module]{.class_s2by}: the interface for a class or method isn't much simpler than its implementation (see [pp. 25](part0008.xhtml#a27T), [110](part0017.xhtml#a2D9)).

[Information Leakage]{.class_s2by}: a design decision is reflected in multiple modules (see [p. 31](part0009.xhtml#a2D3)).

[Temporal Decomposition]{.class_s2by}: the code structure is based on the order in which operations are executed, not on information hiding (see [p. 32](part0009.xhtml#a2DA)).

[Overexposure]{.class_s2by}: An API forces callers to be aware of rarely used features in order to use commonly used features (see [p. 36](part0009.xhtml#a2E0)).

[Pass-Through Method]{.class_s2by}: a method does almost nothing except pass its arguments to another method with a similar signature (see [p. 52](part0011.xhtml#a28K)).

[Repetition]{.class_s2by}: a nontrivial piece of code is repeated over and over (see [p. 68](part0013.xhtml#a2D2)).

[Special-General Mixture]{.class_s2by}: special-purpose code is not cleanly separated from general purpose code (see [p. 71](part0013.xhtml#a2CP)).

[Conjoined Methods]{.class_s2by}: two methods have so many dependencies that its hard to understand the implementation of one without understanding the implementation of the other (see [p. 75](part0013.xhtml#a2DD)).

[Comment Repeats Code]{.class_s2by}: all of the information in a comment is immediately obvious from the code next to the comment (see [p. 104](part0017.xhtml#a2CX)).

[Implementation Documentation Contaminates Interface]{.class_s2by}: an interface comment describes implementation details not needed by users of the thing being documented (see [p. 114](part0017.xhtml#a2E5)).

[Vague Name]{.class_s2by}: the name of a variable or method is so imprecise that it doesn't convey much useful information (see [p. 123](part0018.xhtml#a2DW))[]{#page_184}.

[Hard to Pick Name]{.class_s2by}: it is difficult to come up with a precise and intuitive name for an entity (see [p. 125](part0018.xhtml#a2DF)).

[Hard to Describe]{.class_s2by}: in order to be complete, the documentation for a variable or method must be long. (see [p. 133](part0019.xhtml#a2DV)).

[Nonobvious Code]{.class_s2by}: the behavior or meaning of a piece of code cannot be understood easily. (see [p. 150](part0022.xhtml#a2D5)).
