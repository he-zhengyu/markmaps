Contents

[Preface](part0004.xhtml)

[1    Introduction](part0005.xhtml)

[1.1     How to use this book](part0005.xhtml#a277)

[2    The Nature of Complexity](part0006.xhtml)

[2.1     Complexity defined](part0006.xhtml#a279)

[2.2     Symptoms of complexity](part0006.xhtml#a27A)

[2.3     Causes of complexity](part0006.xhtml#a27B)

[2.4     Complexity is incremental](part0006.xhtml#a27C)

[2.5     Conclusion](part0006.xhtml#a27D)

[3    Working Code Isn't Enough](part0007.xhtml)

[3.1     Tactical programming](part0007.xhtml#a27F)

[3.2     Strategic programming](part0007.xhtml#a27G)

[3.3     How much to invest?](part0007.xhtml#a27H)

[3.4     Startups and investment](part0007.xhtml#a27J)

[3.5     Conclusion](part0007.xhtml#a27K)

[4    Modules Should Be Deep](part0008.xhtml)

[4.1     Modular design](part0008.xhtml#a27N)

[4.2     What's in an interface?](part0008.xhtml#a27P)

[4.3     Abstractions](part0008.xhtml#a27R)

[4.4     Deep modules](part0008.xhtml#a27S)

[4.5     Shallow modules](part0008.xhtml#a27T)

[4.6     Classitis](part0008.xhtml#a27U)

[4.7     Examples: Java and Unix I/O](part0008.xhtml#a27V)

[4.8     Conclusion](part0008.xhtml#a27W)

[5    Information Hiding (and Leakage)](part0009.xhtml)

[5.1     Information hiding](part0009.xhtml#a27Y)

[5.2     Information leakage](part0009.xhtml#a27Z)

[5.3     Temporal decomposition](part0009.xhtml#a280)

[5.4     Example: HTTP server](part0009.xhtml#a281)

[5.5     Example: too many classes](part0009.xhtml#a282)

[5.6     Example: HTTP parameter handling](part0009.xhtml#a283)

[5.7     Example: defaults in HTTP responses](part0009.xhtml#a284)

[5.8     Information hiding within a class](part0009.xhtml#a285)

[5.9     Taking it too far](part0009.xhtml#a286)

[5.10    Conclusion](part0009.xhtml#a287)

[6    General-Purpose Modules are Deeper](part0010.xhtml)

[6.1     Make classes somewhat general-purpose](part0010.xhtml#a289)

[6.2     Example: storing text for an editor](part0010.xhtml#a28A)

[6.3     A more general-purpose API](part0010.xhtml#a28B)

[6.4     Generality leads to better information hiding](part0010.xhtml#a28C)

[6.5     Questions to ask yourself](part0010.xhtml#a28D)

[6.6     Push specialization upwards (and downwards!)](part0010.xhtml#a28E)

[6.7     Example: editor undo mechanism](part0010.xhtml#a28F)

[6.8     Eliminate special cases in code](part0010.xhtml#a28G)

[6.9     Conclusion](part0010.xhtml#a28H)

[7    Different Layer, Different Abstraction](part0011.xhtml)

[7.1     Pass-through methods](part0011.xhtml#a28K)

[7.2     When is interface duplication OK?](part0011.xhtml#a28M)

[7.3     Decorators](part0011.xhtml#a28N)

[7.4     Interface versus implementation](part0011.xhtml#a28P)

[7.5     Pass-through variables](part0011.xhtml#a28R)

[7.6     Conclusion](part0011.xhtml#a28S)

[8    Pull Complexity Downwards](part0012.xhtml)

[8.1     Example: editor text class](part0012.xhtml#a28U)

[8.2     Example: configuration parameters](part0012.xhtml#a28V)

[8.3     Taking it too far](part0012.xhtml#a28W)

[8.4     Conclusion](part0012.xhtml#a28X)

[9    Better Together Or Better Apart?](part0013.xhtml)

[9.1     Bring together if information is shared](part0013.xhtml#a28Z)

[9.2     Bring together if it will simplify the interface](part0013.xhtml#a290)

[9.3     Bring together to eliminate duplication](part0013.xhtml#a291)

[9.4     Separate general-purpose and special-purpose code](part0013.xhtml#a292)

[9.5     Example: insertion cursor and selection](part0013.xhtml#a293)

[9.6     Example: separate class for logging](part0013.xhtml#a294)

[9.7     Splitting and joining methods](part0013.xhtml#a295)

[9.8     A different opinion: [Clean Code]{.class_s2c}](part0013.xhtml#a296)

[9.9     Conclusion](part0013.xhtml#a297)

[10  Define Errors Out Of Existence](part0014.xhtml)

[10.1   Why exceptions add complexity](part0014.xhtml#a299)

[10.2   Too many exceptions](part0014.xhtml#a29A)

[10.3   Define errors out of existence](part0014.xhtml#a29B)

[10.4   Example: file deletion in Windows](part0014.xhtml#a29C)

[10.5   Example: Java substring method](part0014.xhtml#a29D)

[10.6   Mask exceptions](part0014.xhtml#a29E)

[10.7   Exception aggregation](part0014.xhtml#a29F)

[10.8   Just crash?](part0014.xhtml#a29G)

[10.9   Taking it too far](part0014.xhtml#a29H)

[10.10  Conclusion](part0014.xhtml#a29J)

[11  Design it Twice](part0015.xhtml)

[12  Why Write Comments? The Four Excuses](part0016.xhtml)

[12.1   Good code is self-documenting](part0016.xhtml#a29N)

[12.2   I don't have time to write comments](part0016.xhtml#a29P)

[12.3   Comments get out of date and become misleading](part0016.xhtml#a29R)

[12.4   All the comments I have seen are worthless](part0016.xhtml#a29S)

[12.5   Benefits of well-written comments](part0016.xhtml#a29T)

[12.6   A different opinion: comments are failures](part0016.xhtml#a29U)

[13  Comments Should Describe Things that Aren't Obvious from the Code](part0017.xhtml)

[13.1   Pick conventions](part0017.xhtml#a29W)

[13.2   Don't repeat the code](part0017.xhtml#a29X)

[13.3   Lower-level comments add precision](part0017.xhtml#a29Y)

[13.4   Higher-level comments enhance intuition](part0017.xhtml#a29Z)

[13.5   Interface documentation](part0017.xhtml#a2A0)

[13.6   Implementation comments: what and why, not how](part0017.xhtml#a2A1)

[13.7   Cross-module design decisions](part0017.xhtml#a2A2)

[13.8   Conclusion](part0017.xhtml#a2A3)

[13.9   Answers to questions from Section 13.5](part0017.xhtml#a2A4)

[14  Choosing Names](part0018.xhtml)

[14.1   Example: bad names cause bugs](part0018.xhtml#a2A6)

[14.2   Create an image](part0018.xhtml#a2A7)

[14.3   Names should be precise](part0018.xhtml#a2A8)

[14.4   Use names consistently](part0018.xhtml#a2A9)

[14.5   Avoid extra words](part0018.xhtml#a2AA)

[14.6   A different opinion: Go style guide](part0018.xhtml#a2AB)

[14.7   Conclusion](part0018.xhtml#a2AC)

[15  Write The Comments First](part0019.xhtml)

[15.1   Delayed comments are bad comments](part0019.xhtml#a2AE)

[15.2   Write the comments first](part0019.xhtml#a2AF)

[15.3   Comments are a design tool](part0019.xhtml#a2AG)

[15.4   Early comments are fun comments](part0019.xhtml#a2AH)

[15.5   Are early comments expensive?](part0019.xhtml#a2AJ)

[15.6   Conclusion](part0019.xhtml#a2AK)

[16  Modifying Existing Code](part0020.xhtml)

[16.1   Stay strategic](part0020.xhtml#a2AN)

[16.2   Maintaining comments: keep the comments near the code](part0020.xhtml#a2AP)

[16.3   Comments belong in the code, not the commit log](part0020.xhtml#a2AR)

[16.4   Maintaining comments: avoid duplication](part0020.xhtml#a2AS)

[16.5   Maintaining comments: check the diffs](part0020.xhtml#a2AT)

[16.6   Higher-level comments are easier to maintain](part0020.xhtml#a2AU)

[17  Consistency](part0021.xhtml)

[17.1   Examples of consistency](part0021.xhtml#a2AW)

[17.2   Ensuring consistency](part0021.xhtml#a2AX)

[17.3   Taking it too far](part0021.xhtml#a2AY)

[17.4   Conclusion](part0021.xhtml#a2AZ)

[18  Code Should be Obvious](part0022.xhtml)

[18.1   Things that make code more obvious](part0022.xhtml#a2B1)

[18.2   Things that make code less obvious](part0022.xhtml#a2B2)

[18.3   Conclusion](part0022.xhtml#a2B3)

[19  Software Trends](part0023.xhtml)

[19.1   Object-oriented programming and inheritance](part0023.xhtml#a2B5)

[19.2   Agile development](part0023.xhtml#a2B6)

[19.3   Unit tests](part0023.xhtml#a2B7)

[19.4   Test-driven development](part0023.xhtml#a2B8)

[19.5   Design patterns](part0023.xhtml#a2B9)

[19.6   Getters and setters](part0023.xhtml#a2BA)

[19.7   Conclusion](part0023.xhtml#a2BB)

[20  Designing for Performance](part0024.xhtml)

[20.1   How to think about performance](part0024.xhtml#a2BD)

[20.2   Measure before (and after) modifying](part0024.xhtml#a2BE)

[20.3   Design around the critical path](part0024.xhtml#a2BF)

[20.4   An example: RAMCloud Buffers](part0024.xhtml#a2BG)

[20.5   Conclusion](part0024.xhtml#a2BH)

[21  Decide What Matters](part0025.xhtml)

[21.1   How to decide what matters?](part0025.xhtml#a2BK)

[21.2   Minimize what matters](part0025.xhtml#a2BM)

[21.3   How to emphasize things that matter](part0025.xhtml#a2BN)

[21.4   Mistakes](part0025.xhtml#a2BP)

[21.5   Thinking more broadly](part0025.xhtml#a2BR)

[22  Conclusion](part0026.xhtml)

[Index](part0027.xhtml)

[Summary of Design Principles](part0028.xhtml)

[Summary of Red Flags](part0029.xhtml)
