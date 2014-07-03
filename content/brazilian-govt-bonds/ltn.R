# LTN

truncate <- function(x, n=0) {
    k <- 10^n
    trunc(x*k)/k
}

options(digits=8)

session_date <- as.Date('2014-03-21')

tit_pub <- read.table('ms140321.txt', skip=2, sep='@', header=TRUE)
ltn_quotes <- subset(tit_pub, Titulo == 'LTN')
ltn_quotes <- ltn_quotes[, c('Data.Referencia', 'Data.Vencimento', 'Tx..Indicativas', 'PU')]
names(ltn_quotes) <- c('RefDate', 'Maturity', 'Spread', 'SpotPrice')

ltn_quotes <- within(ltn_quotes, {
	Spread <- as.numeric(sub(',', '.', Spread))
	SpotPrice <- as.numeric(sub(',', '.', SpotPrice))
	Maturity <- as.Date(as.character(Maturity), format='%Y%m%d')
})

library(bizdays)
cal <- Calendar(holidaysANBIMA, weekdays=c('saturday', 'sunday'), dib=252, name='ANBIMA')

ltn_quotes <- within(ltn_quotes, {
	MaturityAdj <- adjust.next(Maturity, cal)
	BusinessDays <- bizdays(session_date, MaturityAdj, cal)
	TheoPrice <- truncate(1000/(1+Spread/100)^(BusinessDays/252), 6)
	Diff <- SpotPrice - TheoPrice
})

all(ltn_quotes$Diff == 0)

