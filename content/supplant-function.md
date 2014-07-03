Title: String interpolation in R
Category: programming
Author: Wilson Freitas
Tags: R, string handling
Date: 2014-04-09
Lang: en
Description: Making string handling in R far easier with a simple string interpolation implementation.




[doug-supplant]: http://javascript.crockford.com/remedial.html "Douglas Crockford"
[doug]: http://www.crockford.com/ "Douglas Crockford"
[stringr]: http://cran.r-project.org/web/packages/stringr/index.html "Hadley Wickham's stringr"

<!-- param = {domain: 'valvion.com', media: 'http://media.valvion.com/'};
url = "{media}logo.gif".supplant(param); -->

String handling in R is hard, there are a few packages that help making that task not so hard, but it is still hard.
In my opinion string handling in R will never be as good as languages like Python or Perl, it looks like the language hasn't been designed to face that problem.
But sincerely speaking, I don't think R realy need that, I can pass without it, I can go fairly well with the packages available, and the most popular is [`stringr`][stringr] developed by Hadley Wickham.
It has several good functions for string handling, but it lacks string interpolation like we do in Python.
That's the reason why I developed `str_supplant`:


```r
str_supplant <- function (string, repl) {
	result <- str_match_all(string, "\\{([^{}]*)\\}")
	if (length(result[[1]]) == 0)
		return(string)
	result <- result[[1]]
	for (i in seq_len(dim(result)[1])) {
		x <- result[i,]
		pattern <- x[1]
		key <- x[2]
		if (!is.null(repl[[key]]))
			string <- gsub(pattern, repl[[key]], string, perl=TRUE)
	}
	string
}
```


Here it follows an example:


```r
parms <- list(media='http://aboutwilson.net', face='wilson')
str_supplant("{media}/logo.gif, {media}/img/ {face}", parms)
```

```
## [1] "http://aboutwilson.net/logo.gif, http://aboutwilson.net/img/ wilson"
```


The first argument is the string to be interpolated and the second a `list` with the keys to be used.
If a key doesn't match it isn't interpolated.


```r
parms <- list()
str_supplant("My name is {name}", parms)
```

```
## [1] "My name is {name}"
```


That implementation was deeply inspired by [Douglas Crockford][doug-supplant]'s `supplant` implementation.
Unfortunately that implementation hasn't been vectorized yet, but I think it is quite useful anyway.
I hope it help others like it's been helping me.

