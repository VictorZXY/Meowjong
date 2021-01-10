:- set_prolog_stack(global, limit(100000000000)).
:- set_prolog_stack(trail,  limit(100000000000)).
:- set_prolog_stack(local,  limit(100000000000)).

pair([A, A]).
taatsu([A, B]) :- B < 27, B is A + 1.
taatsu([B, A]) :- B < 27, B is A + 1.
taatsu([A, C]) :- C < 27, C is A + 2.
taatsu([C, A]) :- C < 27, C is A + 2.
koutsu([A, A, A]).
shuntsu([A, B, C]) :- C < 27, B is A + 1, C is A + 2.
shuntsu([A, C, B]) :- C < 27, B is A + 1, C is A + 2.
shuntsu([B, A, C]) :- C < 27, B is A + 1, C is A + 2.
shuntsu([B, C, A]) :- C < 27, B is A + 1, C is A + 2.
shuntsu([C, A, B]) :- C < 27, B is A + 1, C is A + 2.
shuntsu([C, B, A]) :- C < 27, B is A + 1, C is A + 2.

mentsu(Triplet) :- koutsu(Triplet).
mentsu(Triplet) :- shuntsu(Triplet).

remainder(X, [X | Rem], Rem).
remainder(X, [_ | List], Rem) :- remainder(X, List, Rem).

member(Head, [Head | _]).
member(X, [_ | Tail]) :- member(X, Tail).

subset(0, _, []) :- !.
subset(N, List, [X | Xs]) :-
    N > 0,
    NewN is N - 1,
    remainder(X, List, Rem),
    subset(NewN, Rem, Xs).

take(Head, [Head | Tail], Tail).
take(Element, [Head | List], [Head | Rem]) :- take(Element, List, Rem).

remove(Head, [Head | Tail], Tail) :- !.
remove(Element, [Head | List], [Head | Rem]) :- remove(Element, List, Rem).

remove_list([], List, List).
remove_list([X | Xs], List, Rem) :-
    remove(X, List, RemList), !,
    remove_list(Xs, RemList, Rem).

:- dynamic visited/1.

% 0 = 0
combination([], []) :- !.

% 1 = 1
combination([X], [[X]]) :- !.

% 2 = 2 or 1 + 1
combination([A, A], [[A, A]]) :- !.
combination([A, B], [[A, B]]) :- taatsu([A, B]), !.
combination([X, Y], [[X], [Y]]) :- !.

% 3 = 3 or 2 + 1 (1 + 1 + 1 is impossible)
combination([A, B, C], [[A, B, C]]) :- mentsu([A, B, C]), !.
combination([A, B, X], [[A, B], [X]]) :- pair([A, B]), !.
combination([A, X, B], [[A, B], [X]]) :- pair([A, B]), !.
combination([X, A, B], [[A, B], [X]]) :- pair([A, B]), !.
combination([A, B, X], [[A, B], [X]]) :- taatsu([A, B]), !.
combination([A, X, B], [[A, B], [X]]) :- taatsu([A, B]), !.
combination([X, A, B], [[A, B], [X]]) :- taatsu([A, B]), !.

% 4 = 3 + 1 or 2 + 2 (2 + 1 + 1 is impossible)
combination([A, B, C, X], [[A, B, C], [X]]) :- mentsu([A, B, C]), !.
combination([A, B, X, C], [[A, B, C], [X]]) :- mentsu([A, B, C]), !.
combination([A, X, B, C], [[A, B, C], [X]]) :- mentsu([A, B, C]), !.
combination([X, A, B, C], [[A, B, C], [X]]) :- mentsu([A, B, C]), !.

% in the 2 + 2 case, there must be at least one pair
combination([A, B, C, D], [[A, B], [C, D]]) :- pair([A, B]), pair([C, D]), !.
combination([A, B, C, D], [[A, C], [B, D]]) :- pair([A, C]), pair([B, D]), !.
combination([A, B, C, D], [[A, D], [B, C]]) :- pair([A, D]), pair([B, C]), !.

combination([A, B, C, D], [[A, B], [C, D]]) :- pair([A, B]), taatsu([C, D]), !.
combination([A, B, C, D], [[A, C], [B, D]]) :- pair([A, C]), taatsu([B, D]), !.
combination([A, B, C, D], [[A, D], [B, C]]) :- pair([A, D]), taatsu([B, C]), !.
combination([A, B, C, D], [[A, B], [C, D]]) :- taatsu([A, B]), pair([C, D]), !.
combination([A, B, C, D], [[A, C], [B, D]]) :- taatsu([A, C]), pair([B, D]), !.
combination([A, B, C, D], [[A, D], [B, C]]) :- taatsu([A, D]), pair([B, C]), !.

% 5 = 3 + 2 or (3 + 1 + 1 or 2 + 2 + 1), which is equivalent to
% 5 = 3 + 2 or 4 + 1
combination([A, B, C, X, Y], [[A, B, C], [X, Y]]) :- mentsu([A, B, C]), pair([X, Y]), !.
combination([A, B, X, C, Y], [[A, B, C], [X, Y]]) :- mentsu([A, B, C]), pair([X, Y]), !.
combination([A, X, B, C, Y], [[A, B, C], [X, Y]]) :- mentsu([A, B, C]), pair([X, Y]), !.
combination([X, A, B, C, Y], [[A, B, C], [X, Y]]) :- mentsu([A, B, C]), pair([X, Y]), !.
combination([A, B, X, Y, C], [[A, B, C], [X, Y]]) :- mentsu([A, B, C]), pair([X, Y]), !.
combination([A, X, B, Y, C], [[A, B, C], [X, Y]]) :- mentsu([A, B, C]), pair([X, Y]), !.
combination([X, A, B, Y, C], [[A, B, C], [X, Y]]) :- mentsu([A, B, C]), pair([X, Y]), !.
combination([A, X, Y, B, C], [[A, B, C], [X, Y]]) :- mentsu([A, B, C]), pair([X, Y]), !.
combination([X, A, Y, B, C], [[A, B, C], [X, Y]]) :- mentsu([A, B, C]), pair([X, Y]), !.
combination([X, Y, A, B, C], [[A, B, C], [X, Y]]) :- mentsu([A, B, C]), pair([X, Y]), !.

combination([A, B, C, X, Y], [[A, B, C], [X, Y]]) :- mentsu([A, B, C]), taatsu([X, Y]), !.
combination([A, B, X, C, Y], [[A, B, C], [X, Y]]) :- mentsu([A, B, C]), taatsu([X, Y]), !.
combination([A, X, B, C, Y], [[A, B, C], [X, Y]]) :- mentsu([A, B, C]), taatsu([X, Y]), !.
combination([X, A, B, C, Y], [[A, B, C], [X, Y]]) :- mentsu([A, B, C]), taatsu([X, Y]), !.
combination([A, B, X, Y, C], [[A, B, C], [X, Y]]) :- mentsu([A, B, C]), taatsu([X, Y]), !.
combination([A, X, B, Y, C], [[A, B, C], [X, Y]]) :- mentsu([A, B, C]), taatsu([X, Y]), !.
combination([X, A, B, Y, C], [[A, B, C], [X, Y]]) :- mentsu([A, B, C]), taatsu([X, Y]), !.
combination([A, X, Y, B, C], [[A, B, C], [X, Y]]) :- mentsu([A, B, C]), taatsu([X, Y]), !.
combination([X, A, Y, B, C], [[A, B, C], [X, Y]]) :- mentsu([A, B, C]), taatsu([X, Y]), !.
combination([X, Y, A, B, C], [[A, B, C], [X, Y]]) :- mentsu([A, B, C]), taatsu([X, Y]), !.

combination([A, B, C, D, X], [[X] | Quad]) :- combination([A, B, C, D], Quad), !.
combination([A, B, C, X, D], [[X] | Quad]) :- combination([A, B, C, D], Quad), !.
combination([A, B, X, C, D], [[X] | Quad]) :- combination([A, B, C, D], Quad), !.
combination([A, X, B, C, D], [[X] | Quad]) :- combination([A, B, C, D], Quad), !.
combination([X, A, B, C, D], [[X] | Quad]) :- combination([A, B, C, D], Quad), !.

% general case
combination(Hand, [Triplet | Rest]) :-
    subset(3, Hand, Triplet),
    mentsu(Triplet),
    remove_list(Triplet, Hand, Rem),
    combination(Rem, Rest),
    not(visited([Triplet | Rest])),
    assertz(visited([Triplet | Rest])).
