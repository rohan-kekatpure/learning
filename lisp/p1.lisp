(defun ask-number()
    (format t "please enter number: ")
    (let ((val (read)))
        (if (numberp val)
            val
            (ask-number))))

(defun mylen (lst)
    (if (null lst) 
        0
        (+ (mylen (cdr lst)) 1) ))

(format t "~A" (mylen '(1 2 1 a)))

