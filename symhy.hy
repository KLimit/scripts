#!/usr/bin/env hy -i

;; (setv [a b c] (sympy.symbols "a b c"))
(defmacro setsymb [#* symbols]
  `(setv [~@symbols] (hy.I.sympy.symbols ~(list (map str symbols))))
)
