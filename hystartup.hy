#!/usr/bin/env hy
(setv ? help)
(defn div [top bottom] (/ bottom (+ top bottom)))
(defn inv [x] (/ 1 x))
(defn parallel [#* z] (inv (sum (map inv z))))
(defn toggle-spy [] (setv _hy-repl.spy (not _hy-repl.spy)))
