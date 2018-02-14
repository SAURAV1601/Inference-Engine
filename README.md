# Inference-Engine
An inference engine just like prolog that uses First order logic to solve the query. 

Problem is stated as below:

After the high-profile lawsuit in which you succeeded to bring RealityMan to justice after proving that
distributing his Nintendo emulator was a criminal act, everyone wants to hire you! From disputes over tech
patents, to lawsuits on questions of privacy in social media, to suits on liability issues with self-driving cars, to
disputes between Hollywood celebrities and their agents or producers, you are just running out of time and
energy to run all these cases by hand like we have done in the lectures.
Because of the highly sensitive nature of the cases you handle, and because of the extremely high monetary
amounts involved, you cannot trust any existing. You thus decide to create your own, ultra-optimized
inference engine.
After much debating, you decide that the knowledge bases which you will create to handle each case will
contain sentences with the following defined operators:
NOT X ~X
X OR Y X | Y

Use the First order logic to solve the problem:

Format for input.txt:
<NQ = NUMBER OF QUERIES>
<QUERY 1>
…
<QUERY NQ>
<NS = NUMBER OF GIVEN SENTENCES IN THE KNOWLEDGE BASE>
<SENTENCE 1>
…
<SENTENCE NS>

Assumptions
• Each query will be a single literal of the form Predicate(Constant) or ~Predicate(Constant).
• Variables are all single lowercase letters.
• All predicates (such as Sibling) and constants (such as John) are case-sensitive alphabetical strings that
begin with an uppercase letter.
• Each predicate takes at least one argument. Predicates will take at most 100 arguments. A given
predicate name will not appear with different number of arguments.
• There will be at most 100 queries and 1000 sentences in the knowledge base.
• See the sample input below for spacing patterns.
• You can assume that the input format is exactly as it is described. There will be no syntax errors in the
given input.
• All variables are assumed to be universally quantified. There is no existential quantifier in this
homework. There is no need for Skolem functions or Skolem constants.
• Operator priorities apply (negation has higher priority than disjunction). There will be no parentheses
in the sentences, other than around arguments of predicates.
• The knowledge base that you will be given is consistent. So there are no contracting rules or facts in
the knowledge base.
• If you run into a loop and there is no alternative path you can try, report FALSE. An example for this
would be having two rules (1) ~A(x) | B(x) and (2) ~B(x) | A(x) and wanting to prove A(John). In this
case your program should report FALSE.

Format for output.txt:
For each query, determine if that query can be inferred from the knowledge base or not, one query per line:
<ANSWER 1>
…
<ANSWER NQ>
where
each answer should be either TRUE if you can prove that the corresponding query sentence is true given the
knowledge base, or FALSE if you cannot.

Example 1:
For this input.txt:
6
F(Joe)
H(John)
~H(Alice)
~H(John)
G(Joe)
G(Tom)
14
~F(x) | G(x)
~G(x) | H(x)
~H(x) | F(x)
~R(x) | H(x)
~A(x) | H(x)
~D(x,y) | ~H(y)
~B(x,y) | ~C(x,y) | A(x)
B(John,Alice)
B(John,Joe)
~D(x,y) | ~Q(y) | C(x,y)
D(John,Alice)
Q(Joe)
D(John,Joe)
R(Tom)

output.txt should be:
FALSE
TRUE
TRUE
FALSE
FALSE
TRUE


Example 2:
For this input.txt:
2
Ancestor(Liz,Billy)
Ancestor(Liz,Joe)
6
Mother(Liz,Charley)
Father(Charley,Billy)
~Mother(x,y) | Parent(x,y)
~Father(x,y) | Parent(x,y)
~Parent(x,y) | Ancestor(x,y)
~Parent(x,y) | ~Ancestor(y,z) | Ancestor(x,z)

output.txt should be:
TRUE
FALSE


Example 3:
For this input.txt:
1
Criminal(West)
6
~American(x) | ~Weapon(y) | ~Sells(x,y,z) | ~Enemy(z,America) | Criminal(x)
Owns(Nono,M1)
Missile(M1)
~Missile(x) | ~Owns(Nono,x) | Sells(West,x,Nono)
~Missile(x) | Weapon(x)
Enemy(Nono,America)
American(West)

output.txt should be:
TRUE

