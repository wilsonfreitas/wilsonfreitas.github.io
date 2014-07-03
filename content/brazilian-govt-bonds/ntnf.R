# NTN-F

library(reshape)
library(lubridate)

truncate <- function(x, n=0) {
    k <- 10^n
    trunc(x*k)/k
}

options(digits=8)

session_date <- as.Date('2014-03-21')
tit_pub <- read.table('ms140321.txt', skip=2, sep='@', header=TRUE)

ntnf_quotes <- subset(tit_pub, Titulo == 'NTN-F', select=c('Data.Referencia', 'Data.Vencimento', 'Tx..Indicativas', 'PU'))
ntnf_quotes <- rename(ntnf_quotes, c(Data.Referencia='RefDate', Data.Vencimento='Maturity', Tx..Indicativas='Spread', PU='SpotPrice'))
ntnf_quotes <- within(ntnf_quotes, {
	Yield <- as.numeric(sub(',', '.', Spread))/100
	SpotPrice <- as.numeric(sub(',', '.', SpotPrice))
	Maturity <- as.Date(as.character(Maturity), format='%Y%m%d')
	CouponRate <- (1 + 0.1)^0.5 - 1
	VNA <- 1000
})
ntnf_instr <- lapply(split(ntnf_quotes, ntnf_quotes$Maturity), as.list)

ntnf_diff <- lapply(ntnf_instr, function(instr) {
	instr$Maturity -> mat
	cf <- NULL
	while (mat > session_date) {
		cf <- c(adjust.next(mat, cal), cf)
		mat %m+% months(-6) -> mat
	}
	instr <- within(instr, {
		CashFlowDates <- cf
		CashFlowTimeToMaturity <- truncate(bizyears(session_date, cf, cal), 14)
		CashFlowPayments <- VNA*rep(CouponRate, length(cf))
		CashFlowPayments[length(cf)] <- VNA*(1 + CouponRate)
		TheoValue <- round(CashFlowPayments/(1+Yield)^CashFlowTimeToMaturity, 9)
		TheoValue <- truncate(sum(TheoValue), 6)
		Diff <- TheoValue - SpotPrice
	})
	instr[c('TheoValue', 'SpotPrice', 'Diff')]
})

do.call(rbind, ntnf_diff)


colspan <- xpathApply(doc, "//td[contains(@class, 'tabelaTitulo')]",  function(x) as.numeric(xmlAttrs(x)[[2]][3]) )
