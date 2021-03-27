pair_([A, A]).
taatsu_([A, B]) :- B < 27, B is A + 1.
taatsu_([B, A]) :- B < 27, B is A + 1.
taatsu_([A, C]) :- C < 27, C is A + 2.
taatsu_([C, A]) :- C < 27, C is A + 2.
koutsu_([A, A, A]).
shuntsu_([A, B, C]) :- C < 27, B is A + 1, C is A + 2.
shuntsu_([A, C, B]) :- C < 27, B is A + 1, C is A + 2.
shuntsu_([B, A, C]) :- C < 27, B is A + 1, C is A + 2.
shuntsu_([B, C, A]) :- C < 27, B is A + 1, C is A + 2.
shuntsu_([C, A, B]) :- C < 27, B is A + 1, C is A + 2.
shuntsu_([C, B, A]) :- C < 27, B is A + 1, C is A + 2.

mentsu_(Triplet) :- koutsu_(Triplet).
mentsu_(Triplet) :- shuntsu_(Triplet).

remainder_(X, [X | Rem], Rem).
remainder_(X, [_ | List], Rem) :- remainder_(X, List, Rem).

member_(Head, [Head | _]).
member_(X, [_ | Tail]) :- member_(X, Tail).

subset_(0, _, []) :- !.
subset_(N, List, [X | Xs]) :-
    N > 0,
    NewN is N - 1,
    remainder_(X, List, Rem),
    subset_(NewN, Rem, Xs).

take_(Head, [Head | Tail], Tail).
take_(Element, [Head | List], [Head | Rem]) :- take_(Element, List, Rem).

remove_(Head, [Head | Tail], Tail) :- !.
remove_(Element, [Head | List], [Head | Rem]) :- remove_(Element, List, Rem).

remove_list_([], List, List).
remove_list_([X | Xs], List, Rem) :-
    remove_(X, List, RemList), !,
    remove_list_(Xs, RemList, Rem).

:- dynamic visited/1.

% 0 = 0
combination_([], []) :- !.

% 1 = 1
combination_([X], [[X]]) :- !.

% 2 = 2 or 1 + 1
combination_([A, A], [[A, A]]) :- !.
combination_([A, B], [[A, B]]) :- taatsu_([A, B]), !.
combination_([X, Y], [[X], [Y]]) :- !.

% 3 = 3 or 2 + 1 (1 + 1 + 1 is impossible)
combination_([A, B, C], [[A, B, C]]) :- mentsu_([A, B, C]), !.
combination_([A, B, X], [[A, B], [X]]) :- pair_([A, B]), !.
combination_([A, X, B], [[A, B], [X]]) :- pair_([A, B]), !.
combination_([X, A, B], [[A, B], [X]]) :- pair_([A, B]), !.
combination_([A, B, X], [[A, B], [X]]) :- taatsu_([A, B]), !.
combination_([A, X, B], [[A, B], [X]]) :- taatsu_([A, B]), !.
combination_([X, A, B], [[A, B], [X]]) :- taatsu_([A, B]), !.

% 4 = 3 + 1 or 2 + 2 (2 + 1 + 1 is impossible)
combination_([A, B, C, X], [[A, B, C], [X]]) :- mentsu_([A, B, C]), !.
combination_([A, B, X, C], [[A, B, C], [X]]) :- mentsu_([A, B, C]), !.
combination_([A, X, B, C], [[A, B, C], [X]]) :- mentsu_([A, B, C]), !.
combination_([X, A, B, C], [[A, B, C], [X]]) :- mentsu_([A, B, C]), !.

% in the 2 + 2 case, there must be at least one pair
combination_([A, B, C, D], [[A, B], [C, D]]) :- pair_([A, B]), pair_([C, D]), !.
combination_([A, B, C, D], [[A, C], [B, D]]) :- pair_([A, C]), pair_([B, D]), !.
combination_([A, B, C, D], [[A, D], [B, C]]) :- pair_([A, D]), pair_([B, C]), !.

combination_([A, B, C, D], [[A, B], [C, D]]) :- pair_([A, B]), taatsu_([C, D]), !.
combination_([A, B, C, D], [[A, C], [B, D]]) :- pair_([A, C]), taatsu_([B, D]), !.
combination_([A, B, C, D], [[A, D], [B, C]]) :- pair_([A, D]), taatsu_([B, C]), !.
combination_([A, B, C, D], [[A, B], [C, D]]) :- taatsu_([A, B]), pair_([C, D]), !.
combination_([A, B, C, D], [[A, C], [B, D]]) :- taatsu_([A, C]), pair_([B, D]), !.
combination_([A, B, C, D], [[A, D], [B, C]]) :- taatsu_([A, D]), pair_([B, C]), !.

% 5 = 3 + 2 or (3 + 1 + 1 or 2 + 2 + 1), which is equivalent to
% 5 = 3 + 2 or 4 + 1
combination_([A, B, C, X, Y], [[A, B, C], [X, Y]]) :- mentsu_([A, B, C]), pair_([X, Y]), !.
combination_([A, B, X, C, Y], [[A, B, C], [X, Y]]) :- mentsu_([A, B, C]), pair_([X, Y]), !.
combination_([A, X, B, C, Y], [[A, B, C], [X, Y]]) :- mentsu_([A, B, C]), pair_([X, Y]), !.
combination_([X, A, B, C, Y], [[A, B, C], [X, Y]]) :- mentsu_([A, B, C]), pair_([X, Y]), !.
combination_([A, B, X, Y, C], [[A, B, C], [X, Y]]) :- mentsu_([A, B, C]), pair_([X, Y]), !.
combination_([A, X, B, Y, C], [[A, B, C], [X, Y]]) :- mentsu_([A, B, C]), pair_([X, Y]), !.
combination_([X, A, B, Y, C], [[A, B, C], [X, Y]]) :- mentsu_([A, B, C]), pair_([X, Y]), !.
combination_([A, X, Y, B, C], [[A, B, C], [X, Y]]) :- mentsu_([A, B, C]), pair_([X, Y]), !.
combination_([X, A, Y, B, C], [[A, B, C], [X, Y]]) :- mentsu_([A, B, C]), pair_([X, Y]), !.
combination_([X, Y, A, B, C], [[A, B, C], [X, Y]]) :- mentsu_([A, B, C]), pair_([X, Y]), !.

combination_([A, B, C, X, Y], [[A, B, C], [X, Y]]) :- mentsu_([A, B, C]), taatsu_([X, Y]), !.
combination_([A, B, X, C, Y], [[A, B, C], [X, Y]]) :- mentsu_([A, B, C]), taatsu_([X, Y]), !.
combination_([A, X, B, C, Y], [[A, B, C], [X, Y]]) :- mentsu_([A, B, C]), taatsu_([X, Y]), !.
combination_([X, A, B, C, Y], [[A, B, C], [X, Y]]) :- mentsu_([A, B, C]), taatsu_([X, Y]), !.
combination_([A, B, X, Y, C], [[A, B, C], [X, Y]]) :- mentsu_([A, B, C]), taatsu_([X, Y]), !.
combination_([A, X, B, Y, C], [[A, B, C], [X, Y]]) :- mentsu_([A, B, C]), taatsu_([X, Y]), !.
combination_([X, A, B, Y, C], [[A, B, C], [X, Y]]) :- mentsu_([A, B, C]), taatsu_([X, Y]), !.
combination_([A, X, Y, B, C], [[A, B, C], [X, Y]]) :- mentsu_([A, B, C]), taatsu_([X, Y]), !.
combination_([X, A, Y, B, C], [[A, B, C], [X, Y]]) :- mentsu_([A, B, C]), taatsu_([X, Y]), !.
combination_([X, Y, A, B, C], [[A, B, C], [X, Y]]) :- mentsu_([A, B, C]), taatsu_([X, Y]), !.

combination_([A, B, C, D, X], [[X] | Quad]) :- combination_([A, B, C, D], Quad), !.
combination_([A, B, C, X, D], [[X] | Quad]) :- combination_([A, B, C, D], Quad), !.
combination_([A, B, X, C, D], [[X] | Quad]) :- combination_([A, B, C, D], Quad), !.
combination_([A, X, B, C, D], [[X] | Quad]) :- combination_([A, B, C, D], Quad), !.
combination_([X, A, B, C, D], [[X] | Quad]) :- combination_([A, B, C, D], Quad), !.

% general case
combination_(Hand, [Triplet | Rest]) :-
    subset_(3, Hand, Triplet),
    mentsu_(Triplet),
    remove_list_(Triplet, Hand, Rem),
    combination_(Rem, Rest),
    not(visited([Triplet | Rest])),
    assertz(visited([Triplet | Rest])).
