
;; Test input for propply.py

; 1
(if (and (not R) B) W)

; 2
(not (if (if (or P (not Q)) R) (and P R)))

; 3
(or (not (if P Q)) (if R P))

; 4
(not (not (not (not (not P)))))

; 5
(and A A B C)

; 6
(and P (not P))

; 7
(and (if P Q) (and P (not Q)))

