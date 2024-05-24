#!/usr/bin/env hy
(defn div [top bottom] (/ bottom (+ top bottom)))
(defn parallel [#* resistors]
	  (/
		1
		(sum (map (fn [r] (/ 1 r))
				  resistors))))
