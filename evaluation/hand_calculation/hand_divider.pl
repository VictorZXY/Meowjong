:- set_prolog_flag(stack_limit, 100 000 000 000).

koutsu([A, A, A]).
shuntsu([A, B, C]) :- B is A + 1, C is A + 2.
shuntsu([A, C, B]) :- B is A + 1, C is A + 2.
shuntsu([B, A, C]) :- B is A + 1, C is A + 2.
shuntsu([B, C, A]) :- B is A + 1, C is A + 2.
shuntsu([C, A, B]) :- B is A + 1, C is A + 2.
shuntsu([C, B, A]) :- B is A + 1, C is A + 2.

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

remove(Head, [Head | Tail], Tail) :- !.
remove(Element, [Head | List], [Head | Rem]) :- remove(Element, List, Rem).

remove_list([], List, List).
remove_list([X | Xs], List, Rem) :-
    remove(X, List, RemList), !,
    remove_list(Xs, RemList, Rem).

:- dynamic traversed/1.

mentsu_combination([], []).
mentsu_combination(Hand, [Triplet | Rest]) :-
    subset(3, Hand, Triplet),
    mentsu(Triplet),
    remove_list(Triplet, Hand, Rem),
    mentsu_combination(Rem, Rest),
    not(traversed([Triplet | Rest])),
    assertz(traversed([Triplet | Rest])).
