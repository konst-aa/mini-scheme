(display 1)

(display 2)
(display #t)
(display '(1 2 3))

(display (car '(1)))

(define (fib a b n)
   (if (< n 1)
       a
       (fib b (+ a b) (- n 1))))


(define (f a)
 (lambda (b) (+ a b)))


(define (map f l)
 (if l
     (cons (f (car l)) (map f (cdr l)))
     '()))

(display (map (lambda (item) (* 2 item)) '(1 2 3 4 5)))
(display (fib 0 1 1000))
