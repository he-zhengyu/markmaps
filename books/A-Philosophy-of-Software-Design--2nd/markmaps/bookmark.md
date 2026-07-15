# Title Page *(p. 2)*
# Copyright *(p. 3)*
# Contents *(p. 4)*
# Preface *(p. 10)*
# 1: Introduction *(p. 14)*
## 1.1 How to use this book *(p. 17)*
# 2: The Nature of Complexity *(p. 19)*
## 2.1 Complexity defined *(p. 19)*
## 2.2 Symptoms of complexity *(p. 21)*
## 2.3 Causes of complexity *(p. 23)*
## 2.4 Complexity is incremental *(p. 25)*
## 2.5 Conclusion *(p. 26)*
# 3: Working Code Isn’t Enough *(p. 27)*
## 3.1 Tactical programming *(p. 27)*
## 3.2 Strategic programming *(p. 28)*
## 3.3 How much to invest? *(p. 29)*
## 3.4 Startups and investment *(p. 31)*
## 3.5 Conclusion *(p. 33)*
# 4: Modules Should Be Deep *(p. 34)*
## 4.1 Modular design *(p. 34)*
## 4.2 What’s in an interface? *(p. 36)*
## 4.3 Abstractions *(p. 36)*
## 4.4 Deep modules *(p. 38)*
## 4.5 Shallow modules *(p. 40)*
## 4.6 Classitis *(p. 41)*
## 4.7 Examples: Java and Unix I/O *(p. 42)*
## 4.8 Conclusion *(p. 43)*
# 5: Information Hiding (and Leakage) *(p. 44)*
## 5.1 Information hiding *(p. 44)*
## 5.2 Information leakage *(p. 45)*
## 5.3 Temporal decomposition *(p. 46)*
## 5.4 Example: HTTP server *(p. 47)*
## 5.5 Example: too many classes *(p. 48)*
## 5.6 Example: HTTP parameter handling *(p. 49)*
## 5.7 Example: defaults in HTTP responses *(p. 51)*
## 5.8 Information hiding within a class *(p. 52)*
## 5.9 Taking it too far *(p. 52)*
## 5.10: Conclusion *(p. 53)*
# 6: General-Purpose Modules are Deeper *(p. 54)*
## 6.1 Make classes somewhat general-purpose *(p. 54)*
## 6.2 Example: storing text for an editor *(p. 56)*
## 6.3 A more general-purpose API *(p. 57)*
## 6.4 Generality leads to better information hiding *(p. 58)*
## 6.5 Questions to ask yourself *(p. 59)*
## 6.6 Push specialization upwards (and downwards!) *(p. 60)*
## 6.7 Example: editor undo mechanism *(p. 61)*
## 6.8 Eliminate special cases in code *(p. 64)*
## 6.9 Conclusion *(p. 65)*
# 7: Different Layer, Different Abstraction *(p. 66)*
## 7.1 Pass-through methods *(p. 67)*
## 7.2 When is interface duplication OK? *(p. 69)*
## 7.3 Decorators *(p. 70)*
## 7.4 Interface versus implementation *(p. 71)*
## 7.5 Pass-through variables *(p. 72)*
## 7.6 Conclusion *(p. 75)*
# 8: Pull Complexity Downwards *(p. 77)*
## 8.1 Example: editor text class *(p. 77)*
## 8.2 Example: configuration parameters *(p. 78)*
## 8.3 Taking it too far *(p. 79)*
## 8.4 Conclusion *(p. 80)*
# 9: Better Together Or Better Apart? *(p. 81)*
## 9.1 Bring together if information is shared *(p. 83)*
## 9.2 Bring together if it will simplify the interface *(p. 83)*
## 9.3 Bring together to eliminate duplication *(p. 84)*
## 9.4 Separate general-purpose and special-purpose code *(p. 84)*
## 9.5 Example: insertion cursor and selection *(p. 87)*
## 9.6 Example: separate class for logging *(p. 89)*
## 9.7 Splitting and joining methods *(p. 90)*
## 9.8 A different opinion: Clean Code *(p. 93)*
## 9.9 Conclusion *(p. 94)*
# 10: Define Errors Out Of Existence *(p. 95)*
## 10.1 Why exceptions add complexity *(p. 95)*
## 10.2 Too many exceptions *(p. 98)*
## 10.3 Define errors out of existence *(p. 99)*
## 10.4 Example: file deletion in Windows *(p. 100)*
## 10.5 Example: Java substring method *(p. 101)*
## 10.6 Mask exceptions *(p. 102)*
## 10.7 Exception aggregation *(p. 103)*
## 10.8 Just crash? *(p. 107)*
## 10.9 Taking it too far *(p. 108)*
## 10.10 Conclusion *(p. 109)*
# 11: Design it Twice *(p. 110)*
# 12: Why Write Comments? The Four Excuses *(p. 114)*
## 12.1 Good code is self-documenting *(p. 115)*
## 12.2 I don’t have time to write comments *(p. 116)*
## 12.3 Comments get out of date and become misleading *(p. 117)*
## 12.4 All the comments I have seen are worthless *(p. 117)*
## 12.5 Benefits of well-written comments *(p. 118)*
## 12.6 A different opinion: comments are failures *(p. 119)*
# 13: Comments Should Describe Things that Aren’t Obvious from the Code *(p. 121)*
## 13.1 Pick conventions *(p. 122)*
## 13.2 Don’t repeat the code *(p. 123)*
## 13.3 Lower-level comments add precision *(p. 125)*
## 13.4 Higher-level comments enhance intuition *(p. 127)*
## 13.5 Interface documentation *(p. 129)*
## 13.6 Implementation comments: what and why, not how *(p. 136)*
## 13.7 Cross-module design decisions *(p. 137)*
## 13.8 Conclusion *(p. 140)*
## 13.9 Answers to questions from Section 13.5 *(p. 140)*
# 14: Choosing Names *(p. 142)*
## 14.1 Example: bad names cause bugs *(p. 142)*
## 14.2 Create an image *(p. 143)*
## 14.3 Names should be precise *(p. 144)*
## 14.4 Use names consistently *(p. 147)*
## 14.5 Avoid extra words *(p. 148)*
## 14.6 A different opinion: Go style guide *(p. 149)*
## 14.7 Conclusion *(p. 150)*
# 15: Write The Comments First *(p. 152)*
## 15.1 Delayed comments are bad comments *(p. 152)*
## 15.2 Write the comments first *(p. 153)*
## 15.3 Comments are a design tool *(p. 154)*
## 15.4 Early comments are fun comments *(p. 155)*
## 15.5 Are early comments expensive? *(p. 156)*
## 15.6 Conclusion *(p. 156)*
# 16: Modifying Existing Code *(p. 157)*
## 16.1 Stay strategic *(p. 157)*
## 16.2 Maintaining comments: keep the comments near the code *(p. 159)*
## 16.3 Comments belong in the code, not the commit log *(p. 160)*
## 16.4 Maintaining comments: avoid duplication *(p. 161)*
## 16.5 Maintaining comments: check the diffs *(p. 162)*
## 16.6 Higher-level comments are easier to maintain *(p. 162)*
# 17: Consistency *(p. 164)*
## 17.1 Examples of consistency *(p. 164)*
## 17.2 Ensuring consistency *(p. 165)*
## 17.3 Taking it too far *(p. 167)*
## 17.4 Conclusion *(p. 167)*
# 18: Code Should be Obvious *(p. 169)*
## 18.1 Things that make code more obvious *(p. 169)*
## 18.2 Things that make code less obvious *(p. 172)*
## 18.3 Conclusion *(p. 174)*
# 19: Software Trends *(p. 176)*
## 19.1 Object-oriented programming and inheritance *(p. 176)*
## 19.2 Agile development *(p. 178)*
## 19.3 Unit tests *(p. 179)*
## 19.4 Test-driven development *(p. 180)*
## 19.5 Design patterns *(p. 181)*
## 19.6 Getters and setters *(p. 182)*
## 19.7 Conclusion *(p. 182)*
# 20: Designing for Performance *(p. 183)*
## 20.1 How to think about performance *(p. 183)*
## 20.2 Measure before (and after) modifying *(p. 185)*
## 20.3 Design around the critical path *(p. 186)*
## 20.4 An example: RAMCloud Buffers *(p. 188)*
## 20.5 Conclusion *(p. 193)*
# 21: Decide What Matters *(p. 194)*
## 21.1 How to decide what matters? *(p. 194)*
## 21.2 Minimize what matters *(p. 195)*
## 21.3 How to emphasize things that matter *(p. 196)*
## 21.4 Mistakes *(p. 196)*
## 21.5 Thinking more broadly *(p. 197)*
# 22: Conclusion *(p. 198)*
# Index *(p. 200)*
# Summary of Design Principles *(p. 206)*
# Summary of Red Flags *(p. 207)*
# About the Author *(p. 209)*
# Back Cover *(p. 210)*
